import base64
from typing import Optional
from functools import wraps
from werkzeug.security import check_password_hash
from flask import request, make_response, jsonify

from models import User
from app import app, db


@app.route('/signup', methods=['POST'])
def signup():
  if db.user.find_one({ 'username': request.json['username'] }):
    response = make_response(
      jsonify({
        'message': 'User already exist',
      }), 500
    )
  elif db.user.find_one({ 'email': request.json['email'] }):
    response = make_response(
      jsonify({
        'message': 'Email already exist',
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

# Middleware

def is_authorized(user: Optional[User]) -> bool:
  scheme, credentials = request.headers.get('Authorization').split()
  decoded_credentials = base64.b64decode(credentials).decode()
  _, password = decoded_credentials.split(':')

  if not authenticate_user(user=user, password=password):
    return False
  return True

def authenticate_user(user: Optional[User], password: str) -> bool:
  if user is None:
    return None
  return check_password_hash(user.get('password'), password)

def identify_user() -> Optional[User]:
  scheme, credentials = request.headers.get('Authorization').split()
  if not credentials:
    return None

  decoded_credentials = base64.b64decode(credentials).decode()
  username, _ = decoded_credentials.split(':')
  user = db.user.find_one({ 'username': username })
  return user

def authenticated_only(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    user = identify_user()
    scheme, credentials = request.headers.get('Authorization').split()
    decoded_credentials = base64.b64decode(credentials).decode()
    username, password = decoded_credentials.split(':')
    is_authenticated = authenticate_user(user=user, password=password)

    if not is_authenticated:
      response = make_response(
        jsonify({
          'message': 'Credentials not valid',
        }), 401
      )
      response.headers['Content-Type'] = 'application/json'
      response.haders['WWW-Authenticate'] = 'Basic realm=notes_api'
      return response

    request.user = user
    return f(*args, **kwargs)

  return wrapper


from services import create_user
