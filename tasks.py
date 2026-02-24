import time
from celery import Celery
from models import db, Document
from flask import Flask

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db.init_app(flask_app)

@celery_app.task
def process_document_task(doc_id):
    with flask_app.app_context():
        doc = Document.query.get(doc_id)
        if not doc:
            return "Document not found"
        
        doc.status = 'PROCESSING'
        db.session.commit()

        print(f"---Starting work on: {doc.filename}---")
        time.sleep(10)

        doc.status = 'COMPLETED'
        db.session.commit()
        print(f"---Finished:{doc.filename}---")

        return f"Processed {doc.filename}"