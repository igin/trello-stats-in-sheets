import requests

TRELLO_API_URL = 'https://api.trello.com/1/'


class TrelloAPIClient():
    def __init__(self, api_key, api_oauth_token) -> None:
        self.api_key = api_key
        self.api_auth_token = api_oauth_token

    def _get_authenticated(self, endpoint):
        return requests.get(f'{TRELLO_API_URL}/{endpoint}', headers={
            'Authorization': f'OAuth oauth_consumer_key="{self.api_key}", oauth_token="{self.api_auth_token}"'
        })

    def getListsOfBoard(self, board_id):
        response = self._get_authenticated(f'boards/{board_id}/lists')
        trello_lists = response.json()
        lists_by_name = {
            trello_list['name'].lower().strip(): trello_list
            for trello_list in trello_lists
        }
        return lists_by_name

    def getCardsOfList(self, list_id):
        print('get cards of list with id ')
        print(list_id)
        response = self._get_authenticated(f'lists/{list_id}/cards')
        return response.json()
