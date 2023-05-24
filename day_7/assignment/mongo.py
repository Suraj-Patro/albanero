from pymongo import MongoClient
import datetime


client = MongoClient(connectTimeoutMS=2000, retryWrites=True)
# client = MongoClient()  # will connect on the default host and port
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')  # MongoDB URI format:


db = client['test-database']
# db = client.test_database


collection = db['test-collection']
# collection = db.test_collection


post = {"author": "Mike",
        "text": "My first blog post!",
        "type": "new",
        "duration": 10,
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}


posts = [
    {
        "author": "Mike",
        "text": "My Second blog post!",
        "type": "old",
        "duration": 11,
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
    },
    {
        "author": "Mike",
        "text": "My Third blog post!",
        "type": "latest",
        "duration": 15,
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
    },
]


postsC = db.posts
post_id = postsC.insert_one(post).inserted_id
print(post_id)


postsC.insert_many(posts)


filter = { 'type': 'old' }
newvalues = { "$set": { 'type': "old_changed_to_new" } }
postsC.update_one(filter, newvalues)


filter = {"duration": { "$gt": "12" } }
newvalues = { "$set": { "duration" : 12 } }
postsC.update_many(filter, newvalues)


print(db.list_collection_names())


cursor = postsC.find()
for record in cursor:
    print(record)

# postsC.aggregate( [ { "$match": { "type": "new" } }, { "$group": { student_id: "student_id", total: {"$sum": "$course_fee" }}} ])
# Single monolith aggregation
cursor = postsC.aggregate( [ { "$match": { "type": "new" } } ] )

for record in cursor:
    print(record)


# Store a big aggregate intermediate result to be used later without recompute into a seperate document
postsC.aggregate( [ { "$match": { "type": "new" } }, { "$out" : "stage_1" } ] )
