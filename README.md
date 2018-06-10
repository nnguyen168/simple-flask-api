# Deploy a simple RESTful API Flask application with Docker

## Prerequisite
* Docker: [Install Docker](https://docs.docker.com/install/)
* That's all

## Usage
* Clone the git repository

```
git clone https://github.com/nnguyen168/simple-flask-api.git
```

* Explore the Dockerfile
```
FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
```

* The requirements.txt to install Flask
```
Flask==0.10.1
```

* Our simple Flask app.py
```
from flask import Flask, request, jsonify, abort
from flask import make_response

app = Flask(__name__)

users = [
	{
		'id': 1,
		'name': u'John Doe',
		'email': u'john.doe@example.com'
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
```

* Build the docker image
```
docker build -t simple-flask:latest .
```
Don't forget the period at the end

* Run the image
```
docker run -p 5000:5000 simple-flask:latest
```

* Locate to your browser and type `localhost:5000`

## RESTful API

* Get all users
```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i http://localhost:5000/simple-flask/api/v1.0/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 212
Server: Werkzeug/0.14.1 Python/2.7.15rc1
Date: Sun, 10 Jun 2018 15:33:12 GMT

{
  "users": [
    {
      "email": "john.doe@example.com", 
      "id": 1, 
      "name": "John Doe"
    }, 
    {
      "email": "nam.nguyen@example.com", 
      "id": 2, 
      "name": "Nam Nguyen"
    }
  ]
}
```

* Get user by ID
```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i http://localhost:5000/simple-flask/api/v1.0/users/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 94
Server: Werkzeug/0.14.1 Python/2.7.15rc1
Date: Sun, 10 Jun 2018 16:18:06 GMT

{
  "user": {
    "email": "john.doe@example.com", 
    "id": 1, 
    "name": "John Doe"
  }
}
```

```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i http://localhost:5000/simple-flask/api/v1.0/users/3
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 26
Server: Werkzeug/0.14.1 Python/2.7.15rc1
Date: Sun, 10 Jun 2018 16:18:31 GMT

{
  "error": "Not found"
}
```

* Create new user
```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Hans Solo", "email": "hanssolo@example.com"}' http://localhost:5000/simple-flask/api/v1.0/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 96
Server: Werkzeug/0.12.2 Python/2.7.15
Date: Sun, 10 Jun 2018 15:25:15 GMT

{
  "user": {
    "email": "hanssolo@example.com", 
    "id": 3, 
    "name": "Hans Solo"
  }
}
```

* Update user
```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i -H "Content-Type: application/json" -X PUT -d '{"email": "hanssolo@gmail.com"}' http://localhost:5000/simple-flask/api/v1.0/users/3
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 94
Server: Werkzeug/0.12.2 Python/2.7.15
Date: Sun, 10 Jun 2018 15:25:18 GMT

{
  "user": {
    "email": "hanssolo@gmail.com", 
    "id": 3, 
    "name": "Hans Solo"
  }
}
```

* Delete user
```
MacBook-Pro-de-NGUYEN:~ namnguyen$ curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/simple-flask/api/v1.0/users/3
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 21
Server: Werkzeug/0.12.2 Python/2.7.15
Date: Sun, 10 Jun 2018 15:25:48 GMT

{
  "result": true
}
```
