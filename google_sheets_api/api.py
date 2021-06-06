from datetime import datetime
from googleapiclient.discovery import build


class GoogleTrelloDataSheet():
    def __init__(self, document_id) -> None:
        self._sheets = build('sheets', 'v4').spreadsheets()
        self._document_id = document_id

    def get_column_names(self, sheet_name):
        result = self._sheets.values().get(
            spreadsheetId=self._document_id,
            range=f'{sheet_name}!A1:1',
            majorDimension='ROWS').execute()
        return result['values'][0]

    def append_column_values(self, sheet_name, columns):
        column_values = [
            preprocess_column_value(column['value']) for column in columns
        ]

        body = {
            'values': [column_values]
        }
        print(body)

        return self._sheets.values().append(
            spreadsheetId=self._document_id,
            range=f"{sheet_name}!A:D",
            valueInputOption="USER_ENTERED",
            body=body).execute()


def preprocess_column_value(value):
    if isinstance(value, datetime):
        return sheets_date(value)

    return value


def sheets_date(date: datetime):
    epoch_start = datetime(1899, 12, 30)
    delta = date - epoch_start
    return float(delta.days) + (float(delta.seconds) / 86400)
