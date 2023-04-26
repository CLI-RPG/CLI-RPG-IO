from pymongo import MongoClient
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DATABASE = os.environ.get('MONGO_BL_DATABASE')
COLLECTION = os.environ.get('MONGO_SESSIONS_COLLECTION')
client = MongoClient('mongodb://mongo:27017/',
    username=os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
    password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
)

print("Authenthication server connected to database! :)")

db = client[DATABASE]
collection = db[COLLECTION]

@app.route("/save_session", methods=["POST"])
def register():
    data = request.json
    userId = data.get('userId')
    health = data.get('health')
    attackPwr = data.get('attackPwr')
    shield = data.get('shield')
    level = data.get('level')
    enemiesPos = data.get('enemiesPos')
   
    session = {
        "userId": userId,
        "health" : health,
        "attackPwr" : attackPwr,
        "shield" : shield,
        "level" : level,
        "enemiesPos" : enemiesPos
    }
    result = collection.insert_one(session)
    return Response(status=200)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
