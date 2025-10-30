from dotenv import dotenv_values
from databases import Database
import urllib.parse

config = dotenv_values(".env")

password = urllib.parse.quote(config['POSTGRES_PASSWORD'])

database_url = (
    f"postgresql://{config['POSTGRES_USER']}:{password}"
    f"@{config['POSTGRES_SERVER']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
)


database = Database(url=database_url)

def get_db():
    return database
