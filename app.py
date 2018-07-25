from flask import Flask, request, jsonify, abort
from flask import make_response

app = Flask(__name__)

users = [
	{
		'id': 1,
		'name': u'My Nguyen',
		'email': u'my.nguyen@example.com'
	},
	{
		'id': 2,
		'name': u'Nam Nguyen',
		'email': u'nam.nguyen@example.com'
	}
]

@app.route('/')
def hello_world():
	return 'This is a simple RESTful API Flask application back with Docker'

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

# Get all users
@app.route('/simple-flask/api/v1.0/users', methods=['GET'])
def get_users():
	return jsonify({'users': users})

# Get a user by id
@app.route('/simple-flask/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = [user for user in users if user['id'] == user_id]
	if len(user) == 0:
		abort(404)
	return jsonify({'user': user[0]})

# Create a new user
@app.route('/simple-flask/api/v1.0/users', methods=['POST'])
def add_user():
	if not request.json or not 'name' in request.json:
		abort(400)
	user = {
		'id': users[-1]['id'] + 1,
		'name': request.json['name'],
		'email': request.json.get('email', "")
	}
	users.append(user)
	return jsonify({'user': user}), 201

# Update a user
@app.route('/simple-flask/api/v1.0/users/<int:user_id>', methods=['PUT'])
def user_update(user_id):
	user = [user for user in users if user['id'] == user_id]
	if len(user) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json and type(request.json['name']) != unicode:
		abort(400)
	if 'email' in request.json and type(request.json['email']) != unicode:
		abort(400)
	user[0]['name'] = request.json.get('name', user[0]['name'])
	user[0]['email'] = request.json.get('email', user[0]['email'])
	return jsonify({'user': user[0]})

# Delete a user
@app.route('/simple-flask/api/v1.0/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	user = [user for user in users if user['id'] == user_id]
	if len(user) == 0:
		abort(404)
	users.remove(user[0])
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
