from flask import Blueprint, request, jsonify, session, abort
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from models import db, User

auth = Blueprint("auth", __name__)
GOOGLE_CLIENT_ID = "308103150308-afqb0066h1kqvivi3hthbunohj7sb58l.apps.googleusercontent.com"

@auth.route("/api/auth/google", methods=["POST"])
def google_auth():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400
    try:
        id_info = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(google_id=id_info["sub"]).first()
    if not user:
        user = User(
            google_id=id_info["sub"],
            name=id_info["name"],
            email=id_info["email"],
            role="patient"
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["role"] = user.role
    session["name"] = user.name

    return jsonify({
        "message": "Login successful",
        "user": {"id": user.id, "name": user.name, "role": user.role}
    })


#Login endpoint for testing purposes
@auth.route("/api/test-login", methods=["POST"])
def test_login():
    user = User.query.first()
    if not user:
        user = User(
            google_id="test123",
            name="Test User",
            email="test@test.com",
            role="patient"
        )
        db.session.add(user)
        db.session.commit()
    
    session["name"] = user.name
    session["user_id"] = user.id
    session["role"] = user.role

    return {"message": "Test login successful"}


@auth.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})
