import os
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleAuthenticator:
    def __init__(
        self,
        scopes: List,
        credentials_file: str = 'credentials.json',
        token_file: str = 'token.json',
    ):
        self.scopes = scopes
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds: Optional[Credentials] = None

    def authenticate(self):
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

    def get_service(self, api: str, version: str):
        if not self.creds:
            self.authenticate()
        return build(api, version, credentials=self.creds)
