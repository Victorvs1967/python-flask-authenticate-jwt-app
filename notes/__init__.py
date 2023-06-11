from flask import request, make_response, jsonify

from app import app


@app.route('/notes', methods=['POST'])
def create_note():
  note = create_note(request=request)
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


from services import create_note
