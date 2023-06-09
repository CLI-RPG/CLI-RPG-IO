from pymongo import MongoClient
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import json
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

DATABASE = os.environ.get('MONGO_BL_DATABASE')
COLLECTION = os.environ.get('MONGO_SESSIONS_COLLECTION')
client = MongoClient('mongodb://mongo_bl:27017/',
    username=os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
    password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
)


db = client[DATABASE]
collection = db[COLLECTION]

print("Authenthication server connected to database! :)")


@app.route("/session", methods=["POST"])
def create():
    data = request.json
    userID = data.get('userID')
    health = data.get('health')
    attackPwr = data.get('attackPwr')
    shield = data.get('shield')
    level = data.get('level')
    gameMap = data.get('map')
    money = data.get("money")
    scenarioID = data.get('scenarioID')
    currentEnemyHP = data.get('currentEnemyHP')
    name = data.get('name')
    blockTurns = data.get("blockTurnsRemaining")

    session = {
        "userID": userID,
        "health" : health,
        "attackPwr" : attackPwr,
        "shield" : shield,
        "level" : level,
        "money" : money,
        "map" : gameMap,
        "scenarioID" : scenarioID,
        "currentEnemyHP" : currentEnemyHP,
        "name" : name,
        "blockTurnsRemaining" : blockTurns
    }

    print(session, flush=True)

    result = collection.insert_one(session)
    return Response(status=200, response=json.dumps(result.inserted_id.__str__()))

@app.route("/session/<session_id>", methods=["PUT"])
def update(session_id):
    data = request.json
    name = data.get('name')
    userID = data.get('userID')
    health = data.get('health')
    attackPwr = data.get('attackPwr')
    shield = data.get('shield')
    level = data.get('level')
    gameMap = data.get('map')
    money = data.get("money")
    scenarioID = data.get('scenarioID')
    currentEnemyHP = data.get('currentEnemyHP')
    blockTurns = data.get("blockTurnsRemaining")

    session = {
        "name": name,
        "userID": userID,
        "health" : health,
        "attackPwr" : attackPwr,
        "shield" : shield,
        "level" : level,
        "money" : money,
        "map" : gameMap,
        "scenarioID" : scenarioID,
        "currentEnemyHP" : currentEnemyHP,
        "blockTurnsRemaining" : blockTurns
    }
    result = collection.update_one({"_id" : ObjectId(session_id)}, { "$set" : session})
    if result.matched_count == 0:
        return Response(status=404)
    return Response(status=200)


@app.route("/session/<session_id>", methods=["GET"])
def get(session_id):
    result = collection.find_one(ObjectId(session_id))

    if result is None:
        return Response(status=404)
    else:
        session = {
            "name": result["name"],
            "userID": result["userID"],
            "health" : result["health"],
            "attackPwr" : result["attackPwr"],
            "shield" : result["shield"],
            "level" : result["level"],
            "money" : result["money"],
            "map" : result["map"],
            "scenarioID" : result["scenarioID"],
            "currentEnemyHP" : result["currentEnemyHP"],
            "blockTurnsRemaining" : result["blockTurnsRemaining"]
        }
        return Response(status=200, response=json.dumps(session))

@app.route("/session/<session_id>", methods=["DELETE"])
def delete(session_id):
    result = collection.delete_one({"_id":ObjectId(session_id)})
    print(result, flush=True)
    if result.deleted_count == 0:
        return Response(status=404)
    return Response(status=200)

@app.route("/<uid>/sessions", methods=["GET"])
def list(uid):
    result = collection.find({"userID" : uid})

    return Response(status=200, response=json.dumps([{"value" : s["_id"].__str__(), "label" : s["name"]} for s in result]))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
