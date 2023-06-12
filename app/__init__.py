from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api

from db import Connection


app = Flask(__name__)
api = Api(app)
CORS(app)
db = Connection('notes_db')

@app.route('/')
def index():
  return render_template('index.html')


from auth import *
from notes import *