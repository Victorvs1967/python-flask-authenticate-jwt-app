from typing import Optional
from flask import request, make_response, jsonify
from werkzeug.security import check_password_hash

from app import app, db
from models import User


@app.route('/signup', methods=['POST'])
def signup():
  if db.user.find_one({ 'username': request.json['username'] }):
    response = make_response(
      jsonify({
        'message': 'User already exist',
      }), 500
    )
  else:
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

def is_authorized(user: Optional[User]) -> bool:
  credentials = request.headers.get('Authorization')
  username, password = credentials.split(':')

  if not authenticate_user(user=user, password=password):
    return False
  return True

def authenticate_user(user: Optional[User], password: str) -> bool:
  if user is None:
    return None
  return check_password_hash(user.get('password'), password)

def identify_user() -> Optional[User]:
  credentials = request.headers.get('Authorization')
  if not credentials:
    return None

  username, _ = credentials.split(':')
  user = db.user.find_one({ 'username': username })
  return user


from services import create_user
