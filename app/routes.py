from flask import Blueprint, jsonify, session, abort

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "<a href='/auth/login'>Login</a>"

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        abort(401)
    return jsonify({
        "user_id": session["user_id"],
        "name": session.get("name"),
        "role": session.get("role")
    })
