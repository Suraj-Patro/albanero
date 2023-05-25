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


Aggregation Pipeline
https://www.mongodb.com/basics#aggregation-pipelines
https://www.mongodb.com/basics/aggregation-pipeline


https://www.mongodb.com/community/forums/t/memory-allocated-per-connection/12526

https://www.mongodb.com/blog/post/mongodb-atlas-best-practices-part-1
https://www.mongodb.com/blog/post/mongodb-atlas-best-practices-part-2
https://www.mongodb.com/blog/post/mongodb-atlas-best-practices-part-3
https://www.mongodb.com/blog/post/mongodb-atlas-best-practices-part-4

https://www.mongodb.com/blog


https://stackoverflow.com/questions/30715836/architecture-multiple-mongo-databasesconnections-vs-multiple-collections-with

https://stackoverflow.com/questions/16916903/mongodb-performance-having-multiple-databases

https://groups.google.com/g/mongodb-user/c/UBkJKoeM6Tw

