from os import getenv
from dotenv import (load_dotenv, find_dotenv)
from pathlib import Path

# env_path = Path('.') / '.env'
load_dotenv(find_dotenv())  # dotenv_path=env_path
# line bot
CHANNEL_ID = getenv('CHANNEL_ID')
CHANNEL_SECRET = getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = getenv('CHANNEL_ACCESS_TOKEN')
# selenium
CHROMEDRIVER_PATH = getenv('CHROMEDRIVER_PATH')
GOOGLE_CHROME_BIN = getenv('GOOGLE_CHROME_BIN')
# imgur
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
REFRESH_TOKEN = getenv('REFRESH_TOKEN')


SQLALCHEMY_DATABASE_URI = getenv('CLEARDB_DATABASE_URL')

