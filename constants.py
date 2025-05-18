SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DATABASE_URL = "sqlite:///./emails.db"
RULES_FILE = "rule.json"
FIELD_MAP = {"message": "body", "from": "from_"}