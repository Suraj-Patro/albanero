import os
import unittest


class DBTestCase(unittest.TestCase):
    def setUp(self):
        import pymongo

        self._client = pymongo.MongoClient( os.getenv("MONGO_CONN_STR", default="mongodb://localhost:27017/") )
        self._db = os.getenv("MONGO_DB_NAME", default="jira")
        self._cU = os.getenv("MONGO_USERS_COLL_NAME", default="users")
        self._cT = os.getenv("MONGO_TASKS_COLL_NAME", default="tasks")
        self._cC = os.getenv("MONGO_COMMENTS_COLL_NAME", default="comments")

    
    def test_list_databases(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN lists the databases in the MongoDB Server
        """
        print(self._client.list_database_names())


    def test_database(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN connect to database in the MongoDB Server
        """
        assert self._db in self._client.list_database_names()


    def test_list_collections(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN lists the collections in database in the MongoDB Server
        """
        print(self._client[self._db].list_collection_names())


    def test_collection_users(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN connect to users collections in database in the MongoDB Server
        """
        assert self._cU in self._client[self._db].list_collection_names()


    def test_collection_tasks(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN connect to tasks collections in database in the MongoDB Server
        """
        assert self._cT in self._client[self._db].list_collection_names()


    def test_collection_comments(self):
        """
        GIVEN a MongoDB
        WHEN a new mongodb client is connected to MongoDB Server
        THEN connect to comments collections in database in the MongoDB Server
        """
        assert self._cC in self._client[self._db].list_collection_names()
