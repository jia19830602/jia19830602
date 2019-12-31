# config.py
from os import getenv

from dotenv import load_dotenv


load_dotenv()


CHANNEL_ID = getenv('CHANNEL_ID')
assert CHANNEL_ID
CHANNEL_SECRET = getenv('CHANNEL_SECRET')
assert CHANNEL_SECRET
CHANNEL_ACCESS_TOKEN = getenv('CHANNEL_ACCESS_TOKEN')
assert CHANNEL_ACCESS_TOKEN



