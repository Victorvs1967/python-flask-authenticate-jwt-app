from uuid import uuid1
from werkzeug.security import generate_password_hash


class User:
  def __init__(self, username, password, email):
    self._id = str(uuid1().hex)
    self.username = username
    self.password = generate_password_hash(password)
    self.email = email

class Note:
  def __init__(self, title, body, author: User):
    self._id = str(uuid1().hex)
    self.title = title
    self.body = body
    self.author = author
