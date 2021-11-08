from datetime import datetime
from pymongo import MongoClient
from app.exceptions.exceptions import InvalidIdError, InvalidUpdateDataError, MissingKeyError

client = MongoClient("mongodb://localhost:27017/")

db = client["kenzie"]
collection = db["posts"]
id_count = 1

class Post():

    def __init__(self, title, author, tags, content):
        self.created_at = str(datetime.utcnow())
        self.updated_at = str(datetime.utcnow())
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content

    @staticmethod
    def get_all_posts():
        posts_list = list(db.collection.find())
        if len(posts_list) > 0:
            for post in posts_list:
                del post["_id"]
            return {"data": posts_list}, 200
        return {"data": []}, 200

    @staticmethod
    def get_specific_post(id):
        one_post = list(db.collection.find({"id": id}))
        if one_post == []:
            raise InvalidIdError
        del one_post[0]['_id']
        return {"data": one_post[0]}, 200
    
    @staticmethod
    def remove_post(id):
        one_post = list(db.collection.find({"id": id}))
        if one_post == []:
            raise InvalidIdError
        db.collection.delete_one({"id": id})
        return "", 202

    def new_post(self):
        global id_count
        data = self.__dict__

        data["id"] = id_count
        db.collection.insert_one(data)
        del data["_id"]
        id_count += 1
        return data, 201
    
    def update_specific_post(id, **data):
        requested_args = ["title", "author", "tags", "content", "created_at", "updated_at"]
        print(data)
        one_post = list(db.collection.find({"id": id}))

        if one_post == []:
            raise InvalidIdError

        for key in data.keys():
            if key not in requested_args:
                raise InvalidUpdateDataError
           
        data["updated_at"] = str(datetime.utcnow())
        db.collection.update_one({"id": id}, {"$set": data})
        updated_post = list(db.collection.find({"id": id})) 
        del updated_post[0]["_id"]       
        return {"data": updated_post[0]}, 200
        