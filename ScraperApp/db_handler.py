"""
This is the data base handler which connect, fetch, and update cloud database
"""
import pymongo
from EnvironmentalVariable import constant


class DbHandler:
    """
    class for data base handler
    connecting to mongoDB database and do insertion, updating, and fetching
    """
    def __init__(self):
        """
        constructor for database handler
        """
        self.client = pymongo.MongoClient(constant.MONGODB_URL)
        self.db = self.client["webscraping"]
        self.collection = None

    def insert_book(self, post):
        """
        insert book post to database
        :param post: the post to be updated
        :return: none
        """
        self.collection = self.db["Book"]
        return self.collection.update_one({"_id": post["book_id"]}, {"$set": post}, upsert=True)

    def insert_books(self, post):
        """
        insert books post to database
        :return:
        """
        self.collection = self.db["Book"]
        return self.collection.insert_many(post)

    def insert_author(self, post):
        """
        insert author post to database
        :param post: the post to be updated
        :return: none
        """
        self.collection = self.db["Author"]
        return self.collection.update_one({"_id": post["author_id"]}, {"$set": post}, upsert=True)

    def insert_authors(self, post):
        """
        insert many authors in one time
        :param post:
        :return:
        """
        self.collection = self.db["Author"]
        return self.collection.insert_many(post)

    def delete_book(self, post):
        """
        delete a book from database
        :param post:
        :return:
        """
        self.collection = self.db["Book"]
        return self.collection.delete_one(post)

    def delete_author(self, post):
        """
        delete a author from database
        :param post:
        :return:
        """
        self.collection = self.db["Author"]
        return self.collection.delete_one(post)

    def fetch_books(self):
        """
        Tutorial from https://hevodata.com/learn/mongodb-export-to-json/#meth1
        fetch the books from database
        :return: retrived exported MongoDB data from database
        """
        self.collection = self.db["Book"]
        cursor = self.collection.find()
        docs = list(cursor)
        return docs

    def fetch_author(self):
        """
        Tutorial from https://hevodata.com/learn/mongodb-export-to-json/#meth1
        fetch the author from database
        :return: retrived exported MongoDB data from database
        """
        self.collection = self.db["Author"]
        cursor = self.collection.find()
        docs = list(cursor)
        return docs
