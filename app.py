from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from app.models import *
from app.routes import *
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
