from app.models import Parent,db
from flask import  Blueprint, request, jsonify, redirect, url_for
import logging
from flask_login import login_user, logout_user

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


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    try:
        data = request.get_json()
        if request.method == 'POST':
            email = data.get("email")
            password = data.get("password")
            role = data.get("role")

            logged_user = Parent.query.filter(Parent.email == email, password == password, role == role).first()
            if logged_user(logged_user.password):
                login_user(logged_user)
                return redirect(url_for('site.profile'))
    except:
        raise Exception("Invalid form data: Please check your form")
    return("Invalid")
    
@auth.route('/logout')
def logout():
    logout_user()
    return "Logged out"