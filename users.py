from pymongo import MongoClient
import re


class User:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.tvbamazon

    def save_user(self, user):
        self.db.users.insert_one(user)

    def search_by_uname(self, uname):
        query = {
            'user_name': re.compile(uname, re.IGNORECASE)
        }
        result = self.db.users.find(query)
        matches = []
        for user in result:
            matches.append(user)
        return matches
