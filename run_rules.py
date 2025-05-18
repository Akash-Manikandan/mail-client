from sqlmodel import Session
from constants import RULES_FILE
from services.rule_evaluator import RuleEvaluatorService
from utils.json_utils import JSONUtils
from sqlalchemy.engine import Engine
import logging


def run_apply(engine: Engine):
    try:
        data = JSONUtils.read(RULES_FILE)
        parsed_rule = JSONUtils.parse_rules(data)

        with Session(engine) as session:
            for rule in parsed_rule:
                try:
                    logging.info(f"Rule: {rule.description}")
                    evaluator = RuleEvaluatorService(rule)
                    matched_emails = evaluator.execute(session)
                    logging.info(
                        f"Matched Emails: {[{'id': email.id, 'subject': email.subject} for email in matched_emails]}"
                    )
                except Exception as e:
                    logging.error(f"Error applying rule '{rule.description}': {e}")
    except Exception as e:
        logging.error(f"Failed to apply rules: {e}")
