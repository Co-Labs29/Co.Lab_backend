from flask import Blueprint, request, jsonify, current_app
import logging
import jwt
from datetime import datetime, timedelta
from app.models import Parent, Child, db, Wallet
import pytz

auth = Blueprint('auth', __name__)

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
                return jsonify({'message': "Password must be at least 7 characters long"}), 400
            if not first_name or not email or not password or not role:
                return jsonify({"error": "All fields are required"}), 400
            if Parent.query.filter_by(email=email).first():
                return jsonify({"error": "Email already exists"}), 400

            new_parent = Parent(first_name=first_name, email=email, password=password, role=role)
            db.session.add(new_parent)
            db.session.commit()

            token_payload = {
                "sub": new_parent.id,
                "exp": datetime.now(pytz.utc) + timedelta(hours=1)
            }
            jwt_token = jwt.encode(token_payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

            return jsonify({
                "message": f"User account {email} created successfully",
                "token": jwt_token
            }), 201

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

            if not email or not password or not role:
                return jsonify({"message": "Email, password, and role are required"}), 400

            logged_user = Parent.query.filter_by(email=email, role=role.capitalize()).first()

            if logged_user and logged_user.password == password:  # Assuming plain text password for simplicity
                child_ids = [child.id for child in logged_user.children]

                expiration = datetime.now(pytz.utc) + timedelta(hours=1)
                payload = {
                    'sub': logged_user.id,
                    'exp': expiration,
                    'role': logged_user.role
                }
                token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

                return jsonify({
                    "message": "Login successful",
                    "firstName": logged_user.first_name,
                    "parentID": logged_user.id,
                    "childIDs": child_ids,
                    "token": token
                }), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401

        except KeyError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Invalid request method"}), 405

@auth.route('/parent_logout')
def parent_logout():
    return "Logged out"

@auth.route("/child_signup", methods=["POST"])
def child_signup():
    try:
        data = request.get_json()

        if data.get("role") == "Child":
            parent_id = data.get("parent_id")
            username = data.get("username")
            password = data.get("password")
            role = data.get("role")
            img = data.get('img')

            if len(password) < 7:
                return jsonify({'message': "Password must be at least 7 characters long"}), 400
            if not username or not password or not role:
                return jsonify({"message": "All fields are required"}), 400
            existing_child = Child.query.filter_by(username=username).first()
            if existing_child:
                return jsonify({"error": "Username already exists. Please choose a different username."}), 400


            child = Child(parent_id=parent_id, username=username, password=password, role=role, img=img)
            print(f'child: {child}')
            db.session.add(child)
            db.session.commit()

            wallet = Wallet(child_id=child.id, amount=0.0)
            wallet.save()

            expiration = datetime.now(pytz.utc) + timedelta(hours=1)
            payload = {
                'sub': child.id,
                'exp': expiration,
                'role': child.role
            }
            token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

            return jsonify({
                "message": f"User account {username} created successfully",
                "child_id": child.id,
                "token": token
            }), 201

        else:
            return jsonify({"error": "Invalid role"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid form data: {str(e)}"}), 400
    


@auth.route("/child_login", methods=["POST"])
def child_login():
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            role = data.get("role")

            if not username or not password or not role:
                return jsonify({"message": "Username, password, and role are required"}), 400

            child = Child.query.filter_by(username=username).first()
            if child and child.password == password:  # Assuming plain text password for simplicity
                expiration = datetime.now(pytz.utc) + timedelta(hours=1)
                payload = {
                    'sub': child.id,
                    'exp': expiration,
                    'role': child.role
                }
                token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
                id = child.id
                return jsonify({"token": token, "childId": id}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Invalid request method"}), 405




