import threading
import time
from flask import Flask, request, jsonify
from app import Session_manager

app = Flask(__name__)

sm = Session_manager()

@app.route('/login', methods=['POST'])
async def login():

    user = request.json.get('user')
    password = request.json.get('password')
    if not all([user, password]):
        return jsonify({"error": "Missing user or password"}), 400
    
    session_id = await sm.add_user_session(user, password)

    if not session_id:
        return jsonify({"error": "Invalid user or password"}), 401
    
    return jsonify({"session_id": session_id}), 302


if __name__ == '__main__':
    app.run(debug=True)
