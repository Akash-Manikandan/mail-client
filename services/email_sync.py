from sqlmodel import Session
from typing import List
from gmail.reader import GmailReader
from db.models import Email, Thread
from sqlalchemy.exc import SQLAlchemyError
from utils.logger import log_method_call
from sqlalchemy.engine import Engine
from email.utils import parseaddr


class EmailSyncService:
    def __init__(self, gmail_reader: GmailReader, engine: Engine):
        self.gmail_reader = gmail_reader
        self.engine = engine

    @log_method_call
    def sync_emails(self, max_results: int = 10) -> List[str]:
        emails: List[Email] = self.gmail_reader.get_emails(max_results=max_results)
        saved_ids: List[str] = []

        for email in emails:
            try:
                self._store_email(email)
                saved_ids.append(email.id)
            except SQLAlchemyError as e:
                print(f"Error saving email {email.id}: {e}")

        return saved_ids

    def _store_email(self, email: Email) -> None:
        from datetime import datetime

        with Session(self.engine) as session:
            try:
                with session.begin():
                    thread = session.get(Thread, email.thread_id)
                    if thread is None:
                        thread = Thread(id=email.thread_id, subject=email.subject)
                        session.add(thread)

                    existing_email = session.get(Email, email.id)
                    if existing_email:
                        return

                    labels_str = ",".join(email.labels) if isinstance(email.labels, list) else email.labels
                    db_email = Email(
                        id=email.id,
                        thread_id=email.thread_id,
                        from_=parseaddr(email.from_)[1],
                        to=parseaddr(email.to)[1],
                        subject=email.subject,
                        date=email.date if isinstance(email.date, datetime) else None,
                        snippet=email.snippet,
                        body=email.body,
                        is_read=email.is_read,
                        labels=labels_str,
                    )
                    session.add(db_email)

            except SQLAlchemyError as e:
                session.rollback()
                print(f"Transaction failed for email {email.id}: {e}")
                raise
