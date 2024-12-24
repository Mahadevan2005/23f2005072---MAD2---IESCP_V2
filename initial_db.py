from app import app,create_app
# from application.database import db, datastore
from models import *
from flask_security import hash_password
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    user_datastore.find_or_create_role(name="admin", description = "User is an admin")
    user_datastore.find_or_create_role(name = "sponsor", description = "User is an sponsor")
    user_datastore.find_or_create_role(name = "influencer", description = "User is an influencer")
    db.session.commit()
    if not user_datastore.find_user(username="admin"):
        user_datastore.create_user(username="admin", password = generate_password_hash("admin"), email="admin@gmail.com", roles=["admin"])
        admin = Admin(username="admin", password="admin", email="admin@gmail.com", admin_id=0)
        db.session.add(admin)
    db.session.commit()
