from app.models import Parent,db
from flask import  Blueprint, request, jsonify, redirect, url_for
import logging
from flask_login import login_user, logout_user, LoginManager
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=['POST'])
def signup():
    logging.info(f"Request method: {request.method}")
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")

        if data.get("role") == "Parent":
            first_name = data.get("first_name")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")
            if len(password) < 7:
                return jsonify({'message': "Password must be at least 7 characters long"})
            if not first_name or not email or not password or not role:
                return jsonify({"error": "All fields are required"}), 400
            parent = Parent(first_name=first_name, email=email, password=password, role=role)

            parent.save()

            return jsonify({"message": f"User account {email} created successfully"}), 201

        else:
            return jsonify({"error": "Invalid role"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid form data: {str(e)}"}), 400



login_manager = LoginManager()
login_manager.login_view = 'auth.signin'  
login_manager.login_message = "Please login to access this page"

@auth.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")

            
            print(f"Received data - Email: {email}, Password: {password}, Role: {role}")

            if not email or not password or not role:
                print("Missing email, password, or role")
                return jsonify({"message": "Email, password, and role are required"}), 400

            
            logged_user = Parent.query.filter_by(email=email, role=role.capitalize()).first()
            print(f"User found: {logged_user}")

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print("User logged in successfully")
                return "User logged in"
            else:
                print("Invalid credentials")
                return jsonify({"message": "Invalid credentials"}), 401

        except KeyError as e:
            
            print(f"KeyError: {e}")
            return jsonify({"message": "Invalid form data: Missing key"}), 400
        except Exception as e:
            
            print(f"Exception: {e}")
            return jsonify({"message": "An error occurred"}), 500

    return jsonify({"message": "Invalid request method"}), 405
    
@auth.route('/logout')
def logout():
    logout_user()
    return "Logged out"