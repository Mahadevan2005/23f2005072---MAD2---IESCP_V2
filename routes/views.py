from flask import current_app as app, jsonify, request, render_template
from flask.json import dump
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
import uuid

@app.get('/')
def home():
    return render_template("index.html")

#admin-login
@app.post('/admin_login')
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username or Password not provided"}), 400

    user = user_datastore.find_user(username=username)

    if not user:
        return jsonify({"message": "Admin Not Found"}), 404

    # Check if user has the 'admin' role
    if not any(role.name == "admin" for role in user.roles):
        return jsonify({"message": "User is not an Admin"}), 403

    if check_password_hash(user.password, password):
        # Serialize only the role name(s) for JSON
        role_names = [role.name for role in user.roles]
        return jsonify({"token": user.get_auth_token(), "username": user.username, "roles": role_names})
    else:
        return jsonify({"message": "Wrong Password"}), 400
    

#sponsor-login
@app.post('/sponsor_login')
def sponsor_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username or Password not provided"}), 400

    user = user_datastore.find_user(username=username)

    if not user:
        return jsonify({"message": "Sponsor Not Found"}), 404

    # Check if user has the 'admin' role
    if not any(role.name == "sponsor" for role in user.roles):
        return jsonify({"message": "User is not an sponsor"}), 403

    if check_password_hash(user.password, password):
        # Serialize only the role name(s) for JSON
        role_names = [role.name for role in user.roles]
        return jsonify({"token": user.get_auth_token(), "username": user.username, "roles": role_names})
    else:
        return jsonify({"message": "Wrong Password"}), 400
    

@app.post('/sponsor_register')
def sponsor_register():
    data = request.get_json()
    company_name = data.get('company_name')
    username = data.get('username')
    password = data.get('password')
    company_budget = data.get('company_budget')
    industry = data.get('industry')

    # Validate required fields
    if not username:
        return jsonify({"message": "Username not provided"}), 400
    if not password:
        return jsonify({"message": "Password not provided"}), 400
    if not industry:
        return jsonify({"message": "Industry not provided"}), 400
    if not company_name:
        return jsonify({"message": "Company name not provided"}), 400
    if company_budget is None or company_budget <= 0:
        return jsonify({"message": "Company budget must be greater than 0"}), 400

    # Check if username already exists
    sponsor_exists = Sponsor.query.filter_by(username=username).count()
    if sponsor_exists:
        return jsonify({"message": "Username already taken, use another username"}), 401

    # Create new user
    new_user = user_datastore.create_user(
        username=username,
        password=generate_password_hash(password),
        active=False,
        roles=["sponsor"]
    )
    db.session.add(new_user)
    db.session.commit()

    # Create new sponsor
    sponsor = Sponsor(
        company_name=company_name,
        username=username,
        password=generate_password_hash(password),
        company_budget=company_budget,
        industry=industry,
        flagged=0,  # Default value
        approved=0,  # Default value
        sponsor_id=new_user.id
    )
    db.session.add(sponsor)
    db.session.commit()

    return jsonify({"message": "Registration successful", "username": sponsor.username}), 201



#influencer-login
@app.post('/influencer_login')
def influencer_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username or Password not provided"}), 400

    user = user_datastore.find_user(username=username)

    if not user:
        return jsonify({"message": "Influencer Not Found"}), 404

    # Check if user has the 'influencer' role
    if not any(role.name == "influencer" for role in user.roles):
        return jsonify({"message": "User is not an influencer"}), 403

    if check_password_hash(user.password, password):
        # Serialize only the role name(s) for JSON
        role_names = [role.name for role in user.roles]
        return jsonify({"token": user.get_auth_token(), "username": user.username, "roles": role_names})
    else:
        return jsonify({"message": "Wrong Password"}), 400


#influencer-register
@app.post('/influencer_register')
def influencer_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    category = data.get('category')
    niche = data.get('niche')
    platform = data.get('platform')
    reach = data.get('reach')

    # Validate required fields
    if not username:
        return jsonify({"message": "Username not provided"}), 400
    if not password:
        return jsonify({"message": "Password not provided"}), 400
    if not category:
        return jsonify({"message": "Category not provided"}), 400
    if not niche:
        return jsonify({"message": "Niche not provided"}), 400
    if not platform:
        return jsonify({"message": "Platform not provided"}), 400
    if reach is None or reach <= 0:
        return jsonify({"message": "Reach must be a positive number"}), 400

    # Check if username already exists
    influencer_exists = Influencer.query.filter_by(username=username).count()
    if influencer_exists:
        return jsonify({"message": "Username already taken, use another username"}), 401

    # Create new user
    new_user = user_datastore.create_user(username=username, password=generate_password_hash(password), active=False, roles=["influencer"])
    db.session.add(new_user)
    db.session.commit()

    # Create new influencer
    new_influencer = Influencer(
        name=username,
        category=category,
        reach=reach,
        niche=niche,
        platform=platform,
        username=username,
        password=password,
        flagged=0,
        influencer_id=new_user.id
    )
    db.session.add(new_influencer)
    db.session.commit()

    return jsonify({"message": "Registration successful", "username": new_influencer.username}), 201
