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

    def authenticate_user(self, uname, password):
        user = self.db.users.find({'user_name': uname})
        if user.count() > 0:
            for u in user:
                if u['password'] == password:
                    return user
                else:
                    return None
        else:
            return None
