from flask import Flask, jsonify, request


app = Flask(__name__)


# GET -> hello world
# POST -> returns the data that we send
@app.route('/', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):

		data = "hello world"
		return jsonify({'data': data})

# GET -> square of number
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
	return jsonify({'data': num**2})


# driver function
if __name__ == '__main__':
	app.run(debug = True)
