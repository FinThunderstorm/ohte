from os import getenv, path
from dotenv import load_dotenv

env_location = path.join(path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_location)

database_uri = getenv("DATABASE_URI")
