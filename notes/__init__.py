from flask import request, make_response, jsonify

from auth import authenticated_only
from app import app


@app.route('/notes', methods=['POST'])
@authenticated_only
def create_note():
  note = create_note(request=request, author=request.user)
  response = make_response(
    jsonify({
      'title': note.title,
      'body': note.body,
    }), 201
  )

  response.headers['Content-Type'] = 'application/json'
  return response


from services import create_note
