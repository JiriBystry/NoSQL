import datetime
from flask_login import UserMixin
from bson.objectid import ObjectId
from app import mongo, login_manager


# Načtení usera z DB na základě ID (Flask-login)
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

class User(UserMixin):
    def __init__(self, user):
        self.id = str(user['_id'])
        self.username = user['username']
        self.email = user['email']
        self.password = user['password']

    def get_id(self):
        return self.id

# Novy clanek
def create_article(title, content, user_id):
    article = {
        "title": title,
        "content": content,
        "author_id": user_id,
        "comments": [],
        "timestamp": datetime.datetime.utcnow()
    }
    mongo.db.articles.insert_one(article)

# Comments
def add_comment(article_id, content, user_name, user_id):
    comment = {
        '_id': str(ObjectId()),
        "content": content,
        "author_id": user_id,
        "author_name": user_name,
        "timestamp": datetime.datetime.utcnow()
    }
    mongo.db.articles.update_one(
        {"_id": ObjectId(article_id)},
        {"$push": {"comments": comment}}
    )
