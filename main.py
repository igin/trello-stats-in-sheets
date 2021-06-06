from datetime import datetime, timedelta
from google_sheets_api.api import GoogleTrelloDataSheet
import os
from flask import Flask, request, redirect, render_template
from googleapiclient.discovery import build
import json
import requests
from trello_api.api import TRELLO_API_URL, TrelloAPIClient

app = Flask(__name__)

entries = []


TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_OAUTH_TOKEN = os.environ.get('TRELLO_OAUTH_TOKEN')

trello_api_client = TrelloAPIClient(TRELLO_API_KEY, TRELLO_OAUTH_TOKEN)


@app.route("/push_trello_data")
def push_trello_data():
    trello_board_id = request.args.get('trello_board_id')
    google_sheets_document_id = request.args.get('google_sheets_document_id')
    sheet_name = request.args.get('sheet_name')

    assert trello_board_id
    assert google_sheets_document_id
    assert sheet_name

    sheets_api_client = GoogleTrelloDataSheet(
        document_id=google_sheets_document_id)
    column_names = sheets_api_client.get_column_names(sheet_name=sheet_name)

    columns = [
        {
            'name': name,
            'value': None
        } for name in column_names
    ]

    trello_lists_by_name = trello_api_client.getListsOfBoard(
        board_id=trello_board_id)

    for column in columns:
        column_name = column['name'].lower().strip()
        if column_name == 'date':
            column['value'] = datetime.now()
            continue

        trello_list = trello_lists_by_name.get(column_name, None)
        if trello_list is None:
            column['value'] = 0
            continue

        response = trello_api_client.getCardsOfList(list_id=trello_list['id'])
        column['value'] = len(response)

    sheets_api_client.append_column_values(
        sheet_name=sheet_name, columns=columns)

    return "Trello data pushed"


if __name__ == '__main__':
    # this is run when clicking the run button in VSCode
    app.run(host='127.0.0.1', port=8080, debug=True)
