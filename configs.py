from os import getenv
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

CHANNEL_ID = getenv('CHANNEL_ID')
CHANNEL_SECRET = getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = getenv('CHANNEL_ACCESS_TOKEN')

SQLALCHEMY_DATABASE_URI = getenv('CLEARDB_DATABASE_URL')
print(CHANNEL_ACCESS_TOKEN)
