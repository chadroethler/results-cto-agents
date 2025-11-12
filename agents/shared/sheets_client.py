"""
Google Sheets client for agent interactions
"""

import logging
import os
from typing import Dict, List
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class SheetsClient:
    """Client for interacting with Google Sheets"""

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, credentials_file: str = None, spreadsheet_id: str = None):
        """
        Initialize Sheets client

        Args:
            credentials_file: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_file = credentials_file or os.getenv("CREDENTIALS_FILE")
        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")

        if not self.credentials_file or not self.spreadsheet_id:
            raise ValueError("credentials_file and spreadsheet_id must be provided")

        # Authenticate
        creds = Credentials.from_service_account_file(self.credentials_file, scopes=self.SCOPES)

        self.service = build("sheets", "v4", credentials=creds)
        self.sheets = self.service.spreadsheets()

        logger.info(f"Initialized Sheets client for spreadsheet: {spreadsheet_id}")

    def append_rows(self, sheet_name: str, rows: List[List]):
        """
        Append rows to a sheet

        Args:
            sheet_name: Name of the sheet tab
            rows: List of rows to append
        """
        try:
            body = {"values": rows}

            result = (
                self.sheets.values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{sheet_name}!A:Z",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )

            updated_rows = result.get("updates", {}).get("updatedRows", 0)
            logger.info(f"Appended {updated_rows} rows to {sheet_name}")
            return result

        except HttpError as error:
            logger.error(f"Error appending to sheet: {error}")
            raise

    def read_range(self, range_name: str) -> List[List]:
        """
        Read data from a range

        Args:
            range_name: Range in A1 notation (e.g., 'Sheet1!A1:D10')

        Returns:
            List of rows
        """
        try:
            result = self.sheets.values().get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()

            values = result.get("values", [])
            logger.info(f"Read {len(values)} rows from {range_name}")
            return values

        except HttpError as error:
            logger.error(f"Error reading from sheet: {error}")
            raise

    def update_range(self, range_name: str, values: List[List]):
        """
        Update a range with new values

        Args:
            range_name: Range in A1 notation
            values: New values to write
        """
        try:
            body = {"values": values}

            result = (
                self.sheets.values()
                .update(spreadsheetId=self.spreadsheet_id, range=range_name, valueInputOption="USER_ENTERED", body=body)
                .execute()
            )

            updated_cells = result.get("updatedCells", 0)
            logger.info(f"Updated {updated_cells} cells in {range_name}")
            return result

        except HttpError as error:
            logger.error(f"Error updating sheet: {error}")
            raise

    def batch_update(self, updates: List[Dict]):
        """
        Perform batch updates

        Args:
            updates: List of update requests
        """
        try:
            body = {"requests": updates}

            result = self.sheets.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

            logger.info(f"Completed batch update with {len(updates)} requests")
            return result

        except HttpError as error:
            logger.error(f"Error in batch update: {error}")
            raise

    def check_duplicate(self, sheet_name: str, column: str, value: str) -> bool:
        """
        Check if a value exists in a column

        Args:
            sheet_name: Name of the sheet
            column: Column letter (e.g., 'E')
            value: Value to check

        Returns:
            True if duplicate found
        """
        try:
            range_name = f"{sheet_name}!{column}:{column}"
            existing = self.read_range(range_name)
            values = [row[0] for row in existing if row]
            return value in values
        except Exception as e:
            logger.error(f"Error checking duplicate: {e}")
            return False
