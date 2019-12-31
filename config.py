# config.py
from os import getenv

from dotenv import load_dotenv

load_dotenv()


CHANNEL_ID = getenv('CHANNEL_ID', None)
assert CHANNEL_ID
CHANNEL_SECRET = getenv('CHANNEL_SECRET', None)
assert CHANNEL_SECRET
CHANNEL_ACCESS_TOKEN = getenv('CHANNEL_ACCESS_TOKEN', None)
assert CHANNEL_ACCESS_TOKEN



