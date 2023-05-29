import os
import httpx

CAST_SERVICE_HOST_URL = 'http://authentication:8010/users/check'
url = os.environ.get('CAST_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL


async def get_user(token):
    r = httpx.get(f'{url}?token={token}')
    return r.json()

