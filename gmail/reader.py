import base64
from typing import List, Optional, Dict, Any
from db.models import Email
from datetime import datetime
from dateutil import parser
import pytz
from googleapiclient.discovery import Resource
from utils.logger import log_method_call


class GmailReader:
    def __init__(self, service: Resource):
        self.service = service

    @log_method_call
    def get_emails(self, max_results: int = 10) -> List[Email]:
        response = (
            self.service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"], maxResults=max_results)
            .execute()
        )

        emails: List[Email] = []
        for msg in response.get("messages", []):
            msg_data = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="full")
                .execute()
            )
            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])
            header_map = {h["name"]: h["value"] for h in headers}
            email = Email(
                id=msg_data["id"],
                thread_id=msg_data["threadId"],
                from_=header_map.get("From"),
                to=header_map.get("To"),
                subject=header_map.get("Subject"),
                date=self._parse_date(header_map.get("Date")),
                snippet=msg_data.get("snippet"),
                body=self._extract_body(payload),
                is_read="UNREAD" not in msg_data.get("labelIds", []),
                labels=",".join(msg_data.get("labelIds", []) or []),
            )
            emails.append(email)
        return emails

    def _extract_body(self, payload: Dict[str, Any]) -> Optional[str]:
        def decode_body(part):
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data.encode("utf-8")).decode(
                    "utf-8", errors="replace"
                )
            return ""

        if payload.get("mimeType") == "text/plain":
            return decode_body(payload)

        for part in payload.get("parts", []):
            if part.get("mimeType") == "text/plain":
                return decode_body(part)

        return ""

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            dt = parser.parse(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=pytz.UTC)
            else:
                dt = dt.astimezone(pytz.UTC)
            return dt
        except Exception:
            return None
