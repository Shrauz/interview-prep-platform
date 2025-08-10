from flask import Flask,jsonify
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore

from werkzeug.security import generate_password_hash

from application.config import LocalDevelopmentConfig
from application.models import db, User, Role

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    # api.init_app(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app,datastore)
    app.app_context().push()
    return app

app = create_app()

with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name="admin", description="superuser")
    app.security.datastore.find_or_create_role(name="user", description="general user")
    
    if not app.security.datastore.find_user(email="admin@gmail.com"):
        app.security.datastore.create_user(email = "admin@gmail.com",
                                 password = generate_password_hash("1234"),
                                 roles = ['admin'])
    
    db.session.commit()


from application.routes import *

if __name__ == "__main__":
    app.run()