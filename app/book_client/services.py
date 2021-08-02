import http
import logging
import threading
import traceback
from typing import List, Dict, Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

GOOGLE_BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
NY_TIMES_BASE_URL = 'https://api.nytimes.com/svc/books/v3/reviews.json'


class ExternalDataClient:
    """
    External client to make request
    """
    def __init__(self):
        self.data = []

    def get_external_data(self, *args):
        google_thread = threading.Thread(target=self.get_books_by_params_from_google, args=(args[0], args[1]))
        ny_time_thread = threading.Thread(target=self.get_books_by_params_from_ny_times, args=(args[0], args[1]))
        google_thread.start()
        ny_time_thread.start()
        google_thread.join()
        ny_time_thread.join()
        return self.data

    def get_books_by_params_from_google(self, search: str, field: str) -> List[Dict[str, Any]]:
        print(f'----------- execution of get_books_by_params_from_google ...')
        try:
            query_params = {
                'q': [f'{search}+in{field}:{search}' if field != 'subject' else f'{search}+{field}:{search}'][0],
                'key': settings.GOOGLE_API_KEY,
                'langRestrict': 'en'
            }
            response = requests.get(GOOGLE_BASE_URL, params=query_params)
            print(f'---------- google URL=> {response.url}')
            if response.status_code == http.HTTPStatus.OK:
                print(f'-- results from google: {len(response.json()["items"])}')
                self.data.append(response.json())
            else:
                logger.error(f'-- google client error response => {response.text}')
                return None
        except Exception:
            logger.error(f'-- Google client generic error => {traceback.format_exc()}')

    def get_books_by_params_from_ny_times(self, search: str, field: str) -> List[Dict[str, Any]]:
        print(f'----------- execution of get_books_by_params_from_ny_times ...')
        try:
            query_params = {
                f'{field}': f'{search}',
                'api-key': settings.NY_TIMES_KEY
            }
            response = requests.get(NY_TIMES_BASE_URL, params=query_params)
            print(f'---------- NY times URL=> {response.url}')
            if response.status_code == http.HTTPStatus.OK:
                print(f'-- results from ny times: {len(response.json()["results"])}')
                self.data.append(response.json())
            else:
                logger.error(f'-- NY times client error response => {response.text}')
                return None
        except Exception:
            logger.error(f'-- NY times client generic error => {traceback.format_exc()}')