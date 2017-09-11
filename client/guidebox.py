import os
import json
from hashlib import md5
import aiohttp
from time import sleep
from urllib.parse import urlencode

GUIDEBOX_CACHE_DIR = 'cache'
GUIDEBOX_BASE_URL = 'http://api-public.guidebox.com/v2'
API_KEY = 'd9e416220b84065087afbcc22bdbec21e274011c'


async def fetch(url_path, params={}):
    """Fetch a guidebox record and parse it as json"""
    if url_path.startswith('/'):
        # truncate '/' character to standardize
        url_path = url_path[1:]
    headers = {'Authorization': API_KEY}
    print("Fetching url {}".format(url_path))
    if params:
        url_path = "?".join([url_path, urlencode(params)])
    cached_path = '/'.join([GUIDEBOX_CACHE_DIR, md5(bytes(url_path, 'utf8')).hexdigest()])
    url = "/".join([GUIDEBOX_BASE_URL, url_path])
    if os.path.exists(cached_path):
        print("Returning cached object for %s" % url_path)
        with open(cached_path) as f:
            return json.loads(f.read())

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            if data.get('error', '').startswith('You are sending API requests too quickly.'):
                # rate limited
                print("Sleeping...")
                sleep(30)
                return (await fetch(url_path, params))
            with open(cached_path, 'w+') as f:
                f.write(json.dumps(data))
            return data
