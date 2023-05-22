Flask RESTful


# Minimal API
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)


# Flask Debugging
    - code reloading
    - Better Debugging
    - shouldn't used in PROD


# Resourceful Routing

Resources
    - main building block provided by Flask-RESTful
    - built on top of Flask pluggable views
        - giving you easy access to multiple HTTP methods just by defining methods on your resource


from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)


Flask-RESTful
    understands multiple kinds of return values from view methods
    Similar to Flask
        can return any iterable
        will be converted into a response
            including raw Flask response objects
    
    support setting the response code response headers using multiple return values

class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}


# Endpoints
resource will have multiple URLs
    can pass multiple URLs to the add_resource() method on the Api object
    Each one will be routed to your Resource

api.add_resource(HelloWorld,
    '/',
    '/hello')

    can also match parts of the path as variables to your resource methods

api.add_resource(Todo,
    '/todo/<int:todo_id>', endpoint='todo_ep')



# Argument Parsing
While Flask provides easy access to request data (i.e. querystring or POST form encoded data)
    pain to validate form data
    Flask-RESTful has built-in support for request data validation using a library similar to argparse
        reqparse


from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate to charge for this resource')
args = parser.parse_args()


Unlike the argparse module
    reqparse.RequestParser.parse_args()
    returns a Python dictionary
    instead of a custom data structure
    

Using the reqparse module also gives you sane error messages for free

If an argument fails to pass validation
    respond with a 400 Bad Request
    response highlighting the error


inputs module
    provides a number of included common conversion functions
    - inputs.date()
    - inputs.url()


Calling parse_args
    with strict=True
    ensures that an error is thrown
    if the request includes arguments your parser does not define
    args = parser.parse_args(strict=True)


# Data Formatting
By default, all fields in your return iterable will be rendered as-is

works great when dealing with Python data structures
very frustrating when working with objects

    provides the fields module
    marshal_with() decorator
    
similar Django ORM and WTForm
    fields module to describe the structure of your response



from flask_restful import fields, marshal_with

resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')



takes a python object
    prepares it to be serialized

marshal_with() decorator
    apply the transformation
    described by resource_fields
    
only field extracted from the object is task

fields.Url field
    special field that takes an endpoint name
    generates a URL for that endpoint in the response


