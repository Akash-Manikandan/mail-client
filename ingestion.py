from gmail.reader import GmailReader
from services.email_sync import EmailSyncService
from sqlalchemy.engine import Engine
from oauth.auth import GoogleAuthenticator
from constants import READONLY_SCOPES
import logging

def run_ingestion(engine: Engine):
    authenticator = GoogleAuthenticator(scopes=READONLY_SCOPES)
    gmail_service = authenticator.get_service(api="gmail", version="v1")
    reader = GmailReader(service=gmail_service)

    email_sync = EmailSyncService(gmail_reader=reader, engine=engine)
    try:
        saved_ids = email_sync.sync_emails(max_results=30)
        logging.info(f"Successfully saved emails: {saved_ids}")
    except Exception as e:
        logging.error(f"Failed to sync emails: {e}")