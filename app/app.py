from flask import Flask
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


from models import db
from auth import auth_bp
from routes import main_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
