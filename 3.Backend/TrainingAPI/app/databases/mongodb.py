from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.models.user import User
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            # connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'
            connection_url = f'mongodb://{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'
        self.connection_url = connection_url.split('@')[-1]

        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]
        self._users_col = self.db[MongoCollections.users]
        self._books_col = self.db[MongoCollections.books]

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            # cursor = self._books_col.find()
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []
    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    # TODO: write functions CRUD with books
    def update_book(self, id_, updated_data):
        try:
            result = self._books_col.update_one({"_id": id_}, {"$set": updated_data})
            return result.modified_count > 0
        except Exception as ex:
            logger.exception(ex)
        return False

    def delete_book(self, id_):
        try:
            result = self._books_col.delete_one({"_id": id_})
            return result.deleted_count > 0
        except Exception as ex:
            logger.exception(ex)
        return False

    def get_user_by_username(self, username: str):
        try:
            query = {'username': username}
            print("query: ", query)
            cursor = self._users_col.find(query)
            print("cursor: ", cursor)
            return User().from_dict(cursor[0])
        except Exception as ex:
            logger.exception(ex)
        return None

    def add_user(self, user: User):
        try:
            inserted_doc = self._users_col.insert_one(user.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
