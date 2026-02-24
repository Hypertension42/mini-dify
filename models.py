
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    filename = db.Column(db.String(255), nullable = False)

    storage_path = db.Column(db.String(512), nullable = False)

    status = db.Column(db.String(50), default = 'PENDING')

