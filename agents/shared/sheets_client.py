"""
Google Sheets client for writing data
"""

import os
from typing import Dict, List
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class SheetsClient:
    """Client for interacting with Google Sheets"""

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(
        self,
        credentials_file: str = None,
        spreadsheet_id: str = None,
        testing: bool = None
    ):
        """
        Initialize Sheets client

        Args:
            credentials_file: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
            testing: If True, skip credential initialization (for testing)
        """
        # Check if in test mode
        self.testing = testing if testing is not None else (
            os.getenv("TESTING") == "true"
        )

        self.credentials_file = credentials_file or os.getenv("CREDENTIALS_FILE")
        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")

        if not self.testing:
            if not self.spreadsheet_id:
                raise ValueError("spreadsheet_id must be provided")

            # Use default credentials in Cloud Functions, file-based elsewhere
            if self.credentials_file and self.credentials_file != "default":
                # Local development with service account file
                creds = Credentials.from_service_account_file(
                    self.credentials_file, scopes=self.SCOPES
                )
            else:
                # Cloud Functions - use Application Default Credentials
                from google.auth import default
                creds, _ = default(scopes=self.SCOPES)

            self.service = build('sheets', 'v4', credentials=creds)
        else:
            # In test mode, don't initialize credentials
            self.service = None

    def append_row(
        self,
        values: List[List],
        sheet_name: str = "Sheet1"
    ) -> Dict:
        """
        Append a row to the spreadsheet

        Args:
            values: List of rows to append
            sheet_name: Name of the sheet

        Returns:
            Response from Sheets API
        """
        if self.testing:
            return {"updates": {"updatedRows": len(values)}}

        range_name = f"{sheet_name}!A:Z"
        body = {'values': values}

        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return result

    def append_rows(
        self,
        sheet_name: str,
        rows: List[List]
    ) -> Dict:
        """
        Append multiple rows to the spreadsheet

        Args:
            sheet_name: Name of the sheet
            rows: List of rows (each row is a list of values)

        Returns:
            Response from Sheets API
        """
        return self.append_row(rows, sheet_name)

    def batch_append(
        self,
        data: List[Dict],
        sheet_name: str = "Sheet1"
    ) -> Dict:
        """
        Batch append multiple rows

        Args:
            data: List of dicts representing rows
            sheet_name: Name of the sheet

        Returns:
            Response from Sheets API
        """
        if self.testing:
            return {"totalUpdatedRows": len(data)}

        values = [[str(v) for v in row.values()] for row in data]
        return self.append_row(values, sheet_name)

    def read_sheet(
        self,
        range_name: str = "Sheet1!A:Z"
    ) -> List[List]:
        """
        Read data from a sheet

        Args:
            range_name: A1 notation of the range to read

        Returns:
            List of rows
        """
        if self.testing:
            return []

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()

        return result.get('values', [])

    def check_duplicate(
        self,
        sheet_name: str,
        column: str,
        value: str
    ) -> bool:
        """
        Check if a value already exists in a specific column

        Args:
            sheet_name: Name of the sheet
            column: Column letter (e.g., 'A', 'B', 'E')
            value: Value to check for

        Returns:
            True if duplicate exists, False otherwise
        """
        if self.testing:
            return False

        try:
            # Read the specific column
            range_name = f"{sheet_name}!{column}:{column}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])

            # Check if value exists in the column
            for row in values:
                if row and len(row) > 0 and row[0] == value:
                    return True

            return False

        except Exception as e:
            # If there's an error reading, assume not a duplicate
            print(f"Error checking duplicate: {e}")
            return False
