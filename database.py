from dotenv import dotenv_values
from databases import Database
config = dotenv_values(".env")



database_url = f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@{config['POSTGRES_SERVER']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
database = Database(url=database_url)

def get_db():
    return database



