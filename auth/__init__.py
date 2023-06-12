from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from flask import request, make_response, jsonify

from app import app, db
from services import create_user


# secret string generated with: node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
app.config['JWT_SECRET_KEY'] = 'yFFMnRnwPcDMyLLLSZF24/GN8SBqUu2dQCVpCirNVtP33EYWxgbL4OBKLFRHSosUGJSqb4ja9kZBP8WQ7HqXYjkdlUKFmSUlXGYXVZgiNS56l+uFLhKpfxThwfyuxIyyDYjYhm+FytTeOTuLo9K46sYg9D9qLT1rkphoPL152brOWecVBb+ExKKlmCoXSSiabOPJzSy/h6jZkBGQm4mVvrQ+HdDaevtTmEWJpc+oCDlIZYk5C5q/mEXglTMiPCqRQPXvE1GT+HeWtIWgJtj2fGnJudHmvYRBKmWJIp5mPVrvka447lKcW3GLI5FGVJdCQ1u3srOjcw/+62tqPKyUbw=='
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
  username = request.json['username']
  password = request.json['password']
  user = authenticate(username, password)
  if user:
    access_token = create_access_token(identity=username, expires_delta=False)
    result = jsonify(token=access_token)
    return result
  return jsonify(error='Invalid username and password')

@app.route('/signup', methods=['POST'])
def signup():
  if db.user.find_one({ 'username': request.json['username'] }):
    response = make_response(jsonify(message='User already exist'), 500)
  elif db.user.find_one({ 'email': request.json['email'] }):
    response = make_response(jsonify(message='Email already exist'), 500)
  else:
    user = create_user(request=request)
    response = make_response(
      jsonify(username=user.username, password=user.password, email=user.email), 201
    )
  response.headers['Content-Type'] = 'application/json'
  return response

def authenticate(username, password):
  user = db.user.find_one({ 'username': username })
  if user:
    if user.get('username') == username and check_password_hash(user.get('password'), password):
      return user
