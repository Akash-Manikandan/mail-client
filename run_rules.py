from sqlmodel import Session
from constants import RULES_FILE, LABEL_EDIT_SCOPES
from services.rule_evaluator import RuleEvaluatorService
from oauth.auth import GoogleAuthenticator
from gmail.writer import GmailWriter
from utils.json_utils import JSONUtils
from sqlalchemy.engine import Engine
import logging



def run_apply(engine: Engine):
    try:
        data = JSONUtils.read(RULES_FILE)
        parsed_rule = JSONUtils.parse_rules(data)
        authenticator = GoogleAuthenticator(scopes=LABEL_EDIT_SCOPES, credentials_file="credentials.json", token_file="write_token.json")
        gmail_service = authenticator.get_service(api="gmail", version="v1")
        writer = GmailWriter(service=gmail_service)
        
        with Session(engine) as session:
            for idx, rule in enumerate(parsed_rule):
                try:
                    logging.info(f"{idx + 1}. Rule: {rule.description}")
                    evaluator = RuleEvaluatorService(rule, writer)
                    matched_emails = evaluator.execute(session)
                    logging.info(
                        f"Matched Emails: {[{'id': email.id, 'subject': email.subject} for email in matched_emails]} \n\n"
                    )
                except Exception as e:
                    logging.error(f"Error applying rule '{rule.description}': {e}")
    except Exception as e:
        logging.error(f"Failed to apply rules: {e}")
