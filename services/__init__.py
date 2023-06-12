from flask import Request

from app import db
from models import Note, User


def create_user(request: Request):
  user = User(
    username=request.json['username'],
    password=request.json['password'],
    email=request.json['email']
  )
  db.user.insert_one(user.__dict__)
  return user


def create_note(request: Request, author: str):
  user = db.user.find_one({ 'username': author })
  note = Note(
    title=request.json['title'],
    body=request.json['body'],
    author=user
  )
  db.note.insert_one(note.__dict__)
  return note

def get_notes():
  notes = db.note.find({})
  return list(notes)

def get_note(id):
  note = db.note.find_one({ '_id': id })
  return note

def delete_note(id):
  note = db.note.delete_one({ '_id': id })
  return note.deleted_count
