from app.models import Parent,db
from flask import  Blueprint, request, jsonify,flash, redirect, url_for
import logging

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

            # Check if all required fields are present
            if not first_name or not email or not password or not role:
                flash("All fields are required.", "Error")
                return jsonify({"error": "All fields are required"}), 400

            # Create a new Parent instance
            parent = Parent(first_name=first_name, email=email, password=password, role=role)

            # Add to the database session and commit
            db.session.add(parent)
            db.session.commit()

            flash(f"You have successfully created a user account {email}", "User-Created")
            return jsonify({"message": f"User account {email} created successfully"}), 201

        else:
            flash("Invalid role", "Error")
            return jsonify({"error": "Invalid role"}), 400

    except KeyError as e:
        flash(f"Missing key: {e.args[0]}", "Error")
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400
    except Exception as e:
        flash(f"Invalid form data: {str(e)}", "Error")
        return jsonify({"error": f"Invalid form data: {str(e)}"}), 400


# @auth.route('/signin', methods = ['GET', 'POST'])
# def signin():
#     try:
#         data = request.get_json()
#         if request.method == 'POST':
#             email = data.get("email")
#             password = data.get("password")
#             role = data.get("role")

#             logged_user = Parent.query.filter