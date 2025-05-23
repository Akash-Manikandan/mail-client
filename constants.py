SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
DATABASE_URL = "sqlite:///./emails.db"
RULES_FILE = "rule.json"
FIELD_MAP = {"message": "body", "from": "from_"}
REPLACABLE_LABELS = {
    "SENT",
    "DRAFT",
    "TRASH",
    "CATEGORY_PERSONAL",
    "CATEGORY_SOCIAL",
    "CATEGORY_PROMOTIONS",
    "CATEGORY_UPDATES",
    "CATEGORY_FORUMS",
    "CATEGORY_REPORTS"
}
ADD_CATEGORY_LABELS = {
    "PERSONAL",
    "SOCIAL",
    "PROMOTIONS",
    "UPDATES",
    "FORUMS",
    "REPORTS"
}
CATEGORY_PREFIX = "CATEGORY_"
