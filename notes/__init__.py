from flask import request, make_response, jsonify

from app import app


@app.route('/notes', methods=['POST'])
def create_note():
  user = identify_user()

  if not is_authorized(user=user):
    response = make_response(
      jsonify({
        'message': 'Credentials not valid.'
      }), 401
    )
  else:
    note = create_note(request=request, author=user)
    response = make_response(
      jsonify(
        {
          'title': note.title,
          'body': note.body,
        }
      ), 201
    )
  response.headers['Content-Type'] = 'application/json'
  return response


from auth import identify_user, authenticate_user, is_authorized
from services import create_note
