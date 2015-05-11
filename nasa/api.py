import requests

from nasa.apod import Apod

DEMO_KEY = 'DEMO_KEY'

class NasaApiException(Exception):
    """Raised for any exception caused by a call to the Nasa API"""

class RateLimitException(NasaApiException):
    """Raised when you have exceeded your rate limit"""

class Api(object):
    """Build an API wrapper for the NASA data API with the given API key"""
    def __init__(self, api_key=DEMO_KEY):
        super(Api, self).__init__()
        self.api_key = api_key
        if api_key is DEMO_KEY:
            print 'Using default API key. This is not recommended.'
        self.ratelimit_limit = None
        self.ratelimit_remaining = None

    def __repr__(self):
        return '<NasaAPI api_key="%s">' % self.api_key

    @property
    def apod(self):
        return type('Apod', (Apod,), dict(api=self))

    def _get(self, url, payload):
        payload['api_key'] = self.api_key
        response = requests.get(url, params=payload)
        self.ratelimit_limit = int(response.headers['x-ratelimit-limit'])
        self.ratelimit_remaining = int(response.headers['x-ratelimit-remaining'])
        if response.status_code == 429:
            raise RateLimitException('You have exceeded your rate limit')
        response.raise_for_status()
        body = response.json()
        if 'error' in body:
            raise NasaApiException(body['error'])
        return body
