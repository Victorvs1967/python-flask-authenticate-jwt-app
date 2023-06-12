from flask import request, make_response, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app


@app.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
  note = create_note(request=request, author=get_jwt_identity())
  response = make_response(
    jsonify({
      'title': note.title,
      'body': note.body,
    }), 201
  )

  response.headers['Content-Type'] = 'application/json'
  return response


from services import create_note
