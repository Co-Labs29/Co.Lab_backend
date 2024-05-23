from app.models import Parent, Child, db
from flask import  Blueprint, request, jsonify, redirect, url_for
import logging
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/parent_signup', methods=['POST'])
def parent_signup():
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




@auth.route('/parent_signin', methods=['POST'])
def parent_signin():
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")
            print("current user =>>>", current_user)

            
            print(f"Received data - Email: {email}, Password: {password}, Role: {role}")

            if not email or not password or not role:
                print("Missing email, password, or role")
                return jsonify({"message": "Email, password, and role are required"}), 400

            
            logged_user = Parent.query.filter_by(email=email, role=role.capitalize()).first()
            print(f"User found: {logged_user.id}")


            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print("current USer ==>>>>>>>>>>>>", current_user.id)

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
    
@auth.route('/parent_logout')
def parent_logout():
    logout_user()
    return "Logged out"

@auth.route("/child_signup", methods= ["POST"])
def child_signup():
    logging.info(f"Request method: {request.method}")
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")
        print("current user =>>>", current_user)
        if data.get("role") == "child":
            parent_id = current_user.id
            username = data.get("username")
            password = data.get("password")
            role = data.get("role")
            if len(password) < 7:
                return jsonify({'message': "Password must be at least 7 characters long"})
            if not username or not password or not role:
                return jsonify({"error": "All fields are required"}), 400
            child = Child(parent_id=parent_id, username=username, password=password, role=role)

            child.save()
            print("working ===>", child)
            return jsonify({"message": f"User account {username} created successfully"}), 201

        else:
            return jsonify({"error": "Invalid role"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid form data: {str(e)}"}), 400
    
#  stores the parent_id whenever the user is logged in


@auth.route("/test")
@login_required
def test():
    return jsonify({"message": "User is logged in!"})
