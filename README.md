# Gmail Rule-Based Email Processor

This is a standalone Python application that interacts with the Gmail API to fetch, process and manage emails based on user-defined rules. The application uses OAuth 2.0 for authentication and stores email data in a relational database.

The main features include:

- Fetching emails from Gmail using the Gmail REST API.
- Storing emails in a relational database (SQLite3).
- Processing emails based on user-defined rules stored in a JSON file.
- Performing actions on emails based on the rules.

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Akash-Manikandan/mail-client
   cd mail-client
   ```

2. **Install dependencies:**

   ```bash
   uv run main.py
   ```

3. **Set up Gmail API credentials:**

   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Gmail API.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place `credentials.json` in the project root directory.

4. **Database setup:**

   - By default, the script uses SQLite3. For Postgres/MySQL, update the connection string in the script.

5. **Prepare rules:**

   - Create a `rules.json` file in the project root.

## Running the App

- **Fetch emails:** Authenticates with Gmail, fetches emails and stores them in the database.

  ```bash
  uv run main.py ingestion
  ```

- **Process emails with rules:** Loads rules from `rules.json`, applies them to emails and performs actions using the Gmail API.

  ```bash
  uv run main.py apply
  ```

## Working of the App

- `ingestion.py`: Authenticates using OAuth, fetches emails from Gmail REST API, parses fields (From, To, Subject, Date, Message) and stores them in a relational database.
- `run_rules.py`: Reads rules from `rules.json`, evaluates each email against the rules and performs actions via Gmail API.
- `rules.json`: Stores a list of rules. Each rule has a field name, predicate, value and actions. The ruleset can use an overall predicate.

## Feature Overview

- **Gmail API Access**: The app uses the Gmail API for all interactions with the user's mailbox, ensuring compliance with Google's security standards.
- **OAuth 2.0 Authentication**: User credentials are never stored or handled directly by the app. OAuth 2.0 tokens are used for authentication, providing a secure way to access Gmail data.
- **Modular Script Design**: The functionality is divided into distinct scripts for fetching and processing emails, making the codebase modular and easier to maintain.
- **Database Integration**: Fetched emails are stored in a database, allowing for efficient querying and processing. The default database is SQLite3, which requires no additional setup.
- **Rule-Based Processing**: The app supports complex rule-based processing of emails, allowing users to define custom rules for managing their inbox.
- **Flexible Configuration**: Most settings, including database connection strings and rule definitions, are configurable via external files (`rules.json`, `constants.py`), allowing users to customise the app without modifying the code.
- **Extensible Architecture**: The app is designed to be easily extensible, allowing for the addition of new features or modifications to existing functionality without significant refactoring.

## Script Workflow

1. **Authentication**:

   - Uses OAuth 2.0 for secure access to the Gmail API.
   - Credentials are stored in `credentials.json`.

2. **Email Fetching** (`ingestion.py`):

   - Connects to Gmail API.
   - Fetches emails based on predefined criteria.
   - Stores fetched emails in the database.

3. **Email Processing** (`run_rules.py`):

   - Loads email data from the database.
   - Loads rules from `rules.json`.
   - For each email, evaluates it against the rules:
     - If an email matches a rule, the specified actions are performed.
   - Updates the email status in the database and Gmail.

4. **Rule Definition** (`rules.json`):
   - Users define rules in a JSON format.
   - Each rule specifies:
     - A field to evaluate.
     - A predicate for the condition.
     - A value for the condition.
     - Actions to perform if the condition is met.
