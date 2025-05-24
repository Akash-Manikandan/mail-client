from typing import List
from sqlalchemy import and_, or_, not_, func
from sqlmodel import Session, select
from datetime import datetime, timedelta
from constants import FIELD_MAP, REPLACABLE_LABELS, ADD_CATEGORY_LABELS, CATEGORY_PREFIX
from db.models import Email
from utils.types import Rule, Condition, RelativeTime
from gmail.writer import GmailWriter

class RuleEvaluatorService:
    def __init__(self, rule: Rule, gmail_writer: GmailWriter):
        self.rule = rule
        self.gmail_writer = gmail_writer

    def _relative_time_to_datetime(self, rel: RelativeTime, operator: str) -> datetime:
        now = datetime.now()
        unit = rel.unit.lower()
        quantity = rel.quantity

        if "day" in unit:
            delta = timedelta(days=quantity)
        elif "month" in unit:
            delta = timedelta(days=30 * quantity)
        elif "hour" in unit:
            delta = timedelta(hours=quantity)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

        return now - delta if "less" in operator else now - delta

    def _build_filter(self, condition: Condition):
        field = condition.field.lower().replace(" ", "_").replace("/", "_")
        operator = condition.operator.lower()
        value = condition.value

        # Normalize to list
        values = value if isinstance(value, list) else [value]
        values = [v.strip().lower() if isinstance(v, str) else v for v in values]

        if field == "to":
            column = getattr(Email, "to", None)
            if not column:
                raise AttributeError("Email model must have a 'to' field")

            formatted_col = func.lower(func.concat(",", column, ","))

            def build_like_clause(v):
                return formatted_col.like(f"%,{v},%")

            if operator == "equals" or operator == "contains":
                return or_(*[build_like_clause(v) for v in values])
            elif operator == "does not contain":
                return and_(*[~build_like_clause(v) for v in values])
            else:
                raise ValueError(f"Unsupported operator for 'to' field: {operator}")

        # Date-time handling
        if field == "received_date_time" and isinstance(value, RelativeTime):
            dt_value = self._relative_time_to_datetime(value, operator)
            if "less" in operator:
                return Email.date >= dt_value
            elif "greater" in operator:
                return Email.date <= dt_value
            else:
                raise ValueError("Unsupported date/time operator")

        # Fallback for all other fields
        column = getattr(Email, FIELD_MAP.get(field, field), None)
        if not column:
            raise AttributeError(f"Invalid field: {field}")

        if operator == "equals":
            return column == value
        elif operator == "does not equal":
            return column != value
        elif operator == "contains":
            return column.contains(value)
        elif operator == "does not contain":
            return not_(column.contains(value))
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _apply_actions(self, email: Email):
        label_ids_to_add = []
        label_ids_to_remove = []

        for action in self.rule.actions:
            if action.type == "Mark":
                status = action.parameters.status
                if status == "read":
                    label_ids_to_remove.append("UNREAD")
                    email.is_read = True
                elif status == "unread":
                    label_ids_to_add.append("UNREAD")
                    email.is_read = False

            elif action.type == "Move Message":
                destination = action.parameters.destination.upper()
                if CATEGORY_PREFIX not in destination and destination in ADD_CATEGORY_LABELS:
                    destination = f"{CATEGORY_PREFIX}{destination}"

                label_ids_to_add.append(destination)
                for l in REPLACABLE_LABELS:
                    if l != destination:
                        label_ids_to_remove.append(l)

        label_ids_to_add = list(set(label_ids_to_add))
        label_ids_to_remove = list(set(label_ids_to_remove))
        print(f"="*40)
        print(f"Adding labels: {label_ids_to_add}, Removing labels: {label_ids_to_remove}")
        print(f"="*40)
        self.gmail_writer.modify_labels(
            message_id=email.id,
            add_labels=label_ids_to_add,
            remove_labels=label_ids_to_remove,
        )

        final_labels = set(email.labels.split(",")) if email.labels else set()
        final_labels.update(label_ids_to_add)
        final_labels.difference_update(label_ids_to_remove)
        email.labels = ",".join(final_labels)

    def execute(self, session: Session) -> List[Email]:
        filters = [self._build_filter(cond) for cond in self.rule.conditions]
        logic = self.rule.logic.lower()

        if logic == "all":
            query = select(Email).where(and_(*filters))
        elif logic == "any":
            query = select(Email).where(or_(*filters))
        else:
            raise ValueError(f"Invalid logic: {logic}")

        results = session.exec(query).all()
        for email in results:
            self._apply_actions(email)
            session.add(email)

        session.commit()
        return results
