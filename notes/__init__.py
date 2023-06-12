from flask import request, make_response, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app


@app.route('/notes', methods=['GET', 'POST'])
@jwt_required()
def notes():
  if request.method == 'POST':
    note = create_note(request=request, author=get_jwt_identity())
    response = make_response(jsonify(title=note.title, body=note.body), 201)
  elif request.method == 'GET':
    response = make_response(jsonify(notes=get_notes()), 200)
  response.headers['Content-Type'] = 'application/json'
  return response

@app.route('/notes/<note_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def note(note_id):
  if request.method == 'GET':
    note = get_note(note_id)
    response = make_response(jsonify(data=note), 200)
  elif request.method == 'PUT':
    note
    response = make_response(jsonify(data=''), 200)
  elif request.method == 'DELETE':
    result = delete_note(note_id)
    response = make_response(jsonify(result=result), 200)
  response.headers['Content-Type'] = 'application/json'
  return response




from services import create_note, delete_note, get_note, get_notes
