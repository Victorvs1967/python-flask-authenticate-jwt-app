from pymongo import MongoClient


config = {
  'host': 'localhost',
  # 'host': 'mongo_db_host',
  'port': 27017,
  'username': '',
  'password': ''
}

class Connection:
  def __new__(cls, database):
    connection = MongoClient(**config)
    return connection[database]