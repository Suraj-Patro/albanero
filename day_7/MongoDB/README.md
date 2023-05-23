https://www.mongodb.com/docs/manual/tutorial/

https://pymongo.readthedocs.io/en/stable/tutorial.html
https://www.mongodb.com/languages/python/pymongo-tutorial


import pymongo


from pymongo import MongoClient

client = MongoClient()  # will connect on the default host and port
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')  # MongoDB URI format:

# Getting a Database
db = client.test_database
db = client['test-database']

# Getting a Collection
collection
    group of documents stored in MongoDB
    equivalent of a table in a relational database

collection = db.test_collection
collection = db['test-collection']


collections
databases
    created lazily
    none of the above commands have actually performed any operations on the MongoDB server
    
Collections and databases are created
    when the first document is inserted into them


