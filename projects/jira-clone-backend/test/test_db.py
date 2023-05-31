import unittest


class DBTestCase(unittest.TestCase):
    def setUp(self):
        import pymongo

        self._client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = "jira"
        self._cU = "users"
        self._cT = "tasks"
        self._cC = "comments"

    
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
