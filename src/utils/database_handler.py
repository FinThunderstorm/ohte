from pymongo import MongoClient
from utils.config import database_uri

client = MongoClient(database_uri)
database = client.muistio


def get_database():
    return database
