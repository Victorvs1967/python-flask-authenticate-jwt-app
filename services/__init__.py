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


def create_note(request: Request, author: User):
  note = Note(
    title=request.json['title'],
    body=request.json['body'],
    author=author
  )
  db.note.insert_one(note.__dict__)
  return note
