from pymongo import MongoClient
from bson.objectid import ObjectId
import re, json


class User:

    def __init__(self):
        config = json.load(open("./config.json", "r"))
        client = MongoClient(config['mongo_host'], config['mongo_port'])
        self.db = client[config['mongo_dbname']]

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
        if len(matches) > 0:
            return matches[0]
        else:
            return None


    def search_by_id(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        result = self.db.users.find(query)
        matches = []
        for user in result:
            matches.append(user)
        return matches[0]

    def authenticate_user(self, uname, password):
        user = self.db.users.find({'user_name': uname, 'password': password})
        if user.count() > 0:
            for u in user:
                if u['password'] == password:
                    return user
                else:
                    return None
        else:
            return None

    def add_product_to_cart(self, user_id, prd_id):
        condition = {'_id': ObjectId(user_id)}
        cursor = self.db.users.find(condition)

        user_data = cursor[0] if cursor.count() > 0 else None

        if user_data is None:
            return False

        if 'cart' not in user_data:
            user_data['cart'] = []

        if ObjectId(prd_id) not in user_data['cart']:
            user_data['cart'].append(ObjectId(prd_id))
            self.db.users.update_one(filter=condition, update={'$set': user_data})
            return True
        else:
            return False

    def get_products_from_userid(self, user_id):
        condition = {'_id': ObjectId(user_id)}
        user = self.db.users.find(condition)
        return user[0].get('cart') if user.count() > 0 else None

    def remove_product_from_cart(self, user_id, product_id):
        cart = self.get_products_from_userid(user_id)
        success = None
        if len(cart) > 0:
            cart.remove(ObjectId(product_id))
            condition = {}
            condition['_id'] = ObjectId(user_id)
            self.db.users.update_one(condition, {"$set": {'cart': cart}})
            success = True
        else:
            pass
        return success

    def create_user(self, name, user_name, password):
        self.db.users.insert_one({'name':name,'user_name':user_name,'password':password})