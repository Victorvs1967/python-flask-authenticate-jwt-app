from flask import request, make_response, jsonify

from app import app


@app.route('/signup', methods=['POST'])
def signup():
  user = create_user(request=request)
  response = make_response(
    jsonify({
      'username': user.username,
      'password': user.password,
      'email': user.email
    }), 201
  )
  response.headers['Content-Type'] = 'application/json'
  return response


from services import create_user
