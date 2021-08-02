from abc import ABC, abstractmethod

import traceback
from typing import List, Dict, Any

import requests
from django.conf import settings


class GoogleClient:
    """
    A Google API implementation
    """
    def __init__(self):
        self.BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

    def  get_books_by_params(self, search: str, terms: str) -> List[Dict[str, Any]]:
        try:
            query_params = {
                'q': f'{search}+{terms}:{search}',
                'key': settings.GOOGLE_API_KEY
            }
            response = requests.get(self.BASE_URL, params=query_params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'== Google client error => {response.text}')
        except Exception:
            print(f'----------- Generic exception => {traceback.format_exc()}')