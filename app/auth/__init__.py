from flask import Blueprint, request, jsonify, session, redirect, abort
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from cachecontrol import CacheControl
import requests
import os
import pathlib

from models import db, User
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET_FILE, GOOGLE_REDIRECT_URI

auth_bp = Blueprint("auth", __name__)


client_secret_file = os.path.join(pathlib.Path(__file__).parent.parent, GOOGLE_CLIENT_SECRET_FILE)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri=GOOGLE_REDIRECT_URI
)

def login_is_required(f):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@auth_bp.route("/")
def health():
    return {"status": "ok"}, 200

@auth_bp.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

#Login endpoint for testing purposes
@auth_bp.route("/api/test-login", methods=["POST"])
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

@auth_bp.route("/api/auth/google", methods=["POST"])
def google_auth():

    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )
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
        "user": {
            "id": user.id,
            "name": user.name,
            "role": user.role
        }
    })

@auth_bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if session.get("state") != request.args.get("state"):
        abort(500)

    credentials = flow.credentials
    request_session = requests.Session()
    cached_session = CacheControl(request_session)
    token_request = GoogleRequest(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
    )

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

    session["google_id"] = user.google_id
    session["name"] = user.name
    session["user_id"] = user.id
    session["role"] = user.role

    return redirect("/routes/api/dashboard")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
