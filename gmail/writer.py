from typing import List
from googleapiclient.discovery import Resource
from utils.logger import log_method_call


class GmailWriter:
    def __init__(self, service: Resource):
        self.service = service

    @log_method_call
    def modify_labels(
        self,
        message_id: str,
        add_labels: List[str] = [],
        remove_labels: List[str] = []
    ) -> None:
        """
        Modify the labels of a Gmail message.

        :param message_id: The ID of the message to modify.
        :param add_labels: List of label IDs to add.
        :param remove_labels: List of label IDs to remove.
        """
        body = {
            "addLabelIds": list(set(add_labels)),
            "removeLabelIds": list(set(remove_labels)),
        }

        self.service.users().messages().modify(
            userId="me",
            id=message_id,
            body=body
        ).execute()
        print(f"Modified labels for message ID: {message_id}")