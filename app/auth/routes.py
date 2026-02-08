from flask import Blueprint, request, jsonify, session, abort

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    # login logic here
    pass

@auth_bp.route("/logout")
def logout():
    # logout logic here
    pass

@auth_bp.route("/callback")
def callback():
    # oauth callback logic here
    pass

@auth_bp.route("/api/test-login", methods=["POST"])
def test_login():
    # test login
    pass
