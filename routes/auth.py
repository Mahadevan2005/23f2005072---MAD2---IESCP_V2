from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_security import verify_password, login_user, current_user, hash_password
from models import *
from werkzeug.security import check_password_hash, generate_password_hash

class AdminLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']

            # Find user in the database
            user = user_datastore.find_user(email=email)

            # Use check_password_hash to verify the password
            if user and check_password_hash(user.password, password) and user.has_role("admin"):
                login_user(user)
                db.session.commit()
                return make_response(jsonify({
                    'message': 'Admin login successful',
                    'role': 'admin',
                    'email': user.email,
                    'admin_id': user.id,
                    'token': user.get_auth_token()  # Ensure this method is valid
                }), 200)
            else:
                return make_response(jsonify({'message': 'Invalid username or password'}), 401)
        except Exception as e:
            print(f"Error during login: {e}")
            return make_response(jsonify({'message': 'An error occurred during login.'}), 500)



# Sponsor - register
class SponsorRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        sponsor_details = data.get('sponsor_details', {})

        # Validate required fields
        if not username:
            return make_response(jsonify({"message": "Username is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "Password is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "Email is required"}), 400)

        # Check if the user already exists by username
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({"message": "Email already exists"}), 400)
        
        if sponsor_details.get('company_budget', 0) <= 0:
            return make_response(jsonify({"message": "Company budget must be greater than zero"}), 400)


        # Create user
        user = user_datastore.create_user(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.flush()  # Ensure user ID is generated

        # Add sponsor details
        sponsor = Sponsor(
            sponsor_id=user.id,  # Use sponsor_id for the foreign key
            company_name=sponsor_details.get('company_name', ''),
            company_budget=sponsor_details.get('company_budget', 0),
            industry=sponsor_details.get('industry', ''),
            username=sponsor_details.get('username', ''),
            password=sponsor_details.get('password', ''),
            email=sponsor_details.get('email', ''),
            flagged=sponsor_details.get('flagged', 0),
            approved=sponsor_details.get('approved', 0)
        )
        db.session.add(sponsor)

        # Assign role to user
        user_datastore.add_role_to_user(user, 'sponsor')

        db.session.commit()

        token = user.get_auth_token()

        return make_response(jsonify({
            "message": "Sponsor created successfully",
            "user_id": user.id,
            "email": sponsor.email,
            "sponsor_id": sponsor.id,
            "username": user.username,
            "company_name": sponsor.company_name,
            "company_budget": sponsor.company_budget,
            "industry": sponsor.industry,
            "flagged": sponsor.flagged,
            "approved": sponsor.approved,
            "token": token,
            "role": "sponsor"
        }), 201)


# Sponsor - login
class SponsorLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']

            user = user_datastore.find_user(email=email)

            if user and check_password_hash(user.password, password):
                if user.has_role('sponsor'):
                    sponsor = Sponsor.query.filter_by(sponsor_id=user.id).first()

                    # Check if the sponsor is flagged
                    if sponsor.flagged == 1:
                        return make_response(jsonify({'message': 'Your account is flagged.'}), 403)

                    # Check if the sponsor is approved
                    if sponsor.approved == 1:
                        login_user(user)

                        return make_response(jsonify({
                            'message': 'Sponsor login successful',
                            'sponsor_id': sponsor.id,
                            'email': sponsor.email,
                            'company_name': sponsor.company_name,
                            'company_budget': sponsor.company_budget,
                            'industry': sponsor.industry,
                            'role': 'sponsor',
                            'token': user.get_auth_token(),
                        }), 200)
                    else:
                        return make_response(jsonify({'message': 'Your account is pending approval from the admin.'}), 403)

                return make_response(jsonify({'message': 'User is not a sponsor'}), 404)

            return make_response(jsonify({'message': 'Invalid email or password'}), 401)

        except Exception as e:
            print(f"Error during login: {e}")
            return make_response(jsonify({'message': 'An error occurred during login.'}), 500)


# Influencer - register
class InfluencerRegister(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        influencer_details = data.get('influencer_details', {})

        # Validate required fields
        if not username:
            return make_response(jsonify({"message": "Username is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "Password is required"}), 400)
        if not email:
            return make_response(jsonify({"message": "E-mail is required"}), 400)

        # Check if the user already exists by username
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({"message": "E-mail already exists"}), 400)
        
        if influencer_details.get('reach', 0) <= 0:
            return make_response(jsonify({"message": "Reach must be greater than zero"}), 400)

        # Create user
        user = user_datastore.create_user(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.flush()  # Ensure user ID is generated

        # Add influencer details
        influencer = Influencer(
            influencer_id=user.id,  # Use influencer_id for the foreign key
            name=influencer_details.get('name', ''),  # Corrected to get name
            category=influencer_details.get('category', ''),
            reach=influencer_details.get('reach', 0),
            niche=influencer_details.get('niche', ''),
            platform=influencer_details.get('platform', ''),
            username=influencer_details.get('name',''),
            password=influencer_details.get('password',''),
            email=influencer_details.get('email', ''),
            flagged=influencer_details.get('flagged',0)
        )
        db.session.add(influencer)

        # Assign role to user
        user_datastore.add_role_to_user(user, 'influencer')

        db.session.commit()

        token = user.get_auth_token()

        return make_response(jsonify({
            "message": "Influencer created successfully",
            "user_id": user.id,
            "influencer_id": influencer.id,  # Corrected to use influencer.id
            "username": user.username,
            "email": user.email,
            "name": influencer.name,  # Use influencer.name
            "category": influencer.category,
            "niche": influencer.niche,
            "reach": influencer.reach,
            "platform": influencer.platform,
            "token": token,
            "role": "influencer"
        }), 201)
    

# Influencer - login
class InfluencerLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']

            # Find user in the database
            user = user_datastore.find_user(email=email)

            if user and check_password_hash(user.password, password):
                # Check if the user has the 'influencer' role
                if user.has_role('influencer'):
                    # Retrieve the influencer using the foreign key (user.id)
                    influencer = Influencer.query.filter_by(influencer_id=user.id).first()

                    # Check if the influencer's account is flagged
                    if influencer.flagged == 1:
                        return make_response(jsonify({'message': 'Your account is flagged.'}), 403)

                    # Log the user in and return the necessary details
                    login_user(user)
                    return make_response(jsonify({
                        'message': 'Influencer login successful',
                        'influencer_id': influencer.id,
                        'email': influencer.email,
                        'category': influencer.category,
                        'reach': influencer.reach,
                        'niche': influencer.niche,
                        'platform': influencer.platform,
                        'flagged': influencer.flagged,
                        'token': user.get_auth_token(),
                    }), 200)

                return make_response(jsonify({'message': 'User is not an influencer'}), 403)

            return make_response(jsonify({'message': 'Invalid email or password'}), 401)

        except Exception as e:
            print(f"Error during login: {e}")
            return make_response(jsonify({'message': 'An error occurred during login.'}), 500)
