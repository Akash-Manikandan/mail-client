READONLY_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
LABEL_EDIT_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
DATABASE_URL = "sqlite:///./emails.db"
RULES_FILE = "rule.json"
FIELD_MAP = {"message": "body", "from": "from_"}
REPLACABLE_LABELS = {
    "CATEGORY_SOCIAL",
    "CATEGORY_PROMOTIONS",
    "CATEGORY_UPDATES",
    "CATEGORY_FORUMS",
}
ADD_CATEGORY_LABELS = {
    "SOCIAL",
    "UPDATES",
    "PROMOTIONS",
    "FORUMS"
}
CATEGORY_PREFIX = "CATEGORY_"
