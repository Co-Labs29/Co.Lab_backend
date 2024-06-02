from app.models import Parent, Child, db, Wallet
from flask import  Blueprint, request, jsonify
import logging
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

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
            
            hashed_password = generate_password_hash(password)
            new_parent = Parent(first_name=first_name, email=email, password=hashed_password, role=role)
            db.session.add(new_parent)
            db.session.commit()

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
            
            print(f"Received data - Email: {email}, Password: {password}, Role: {role}")

            if not email or not password or not role:
                print("Missing email, password, or role")
                return jsonify({"message": "Email, password, and role are required"}), 400

            logged_user = Parent.query.filter_by(email=email, role=role.capitalize()).first()
            print(f"User found: {logged_user.id}")

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)

                print("User logged in successfully")
                print("current USer ==>>>>>>>>>>>>", current_user)
                print(f"current ParentID {current_user.id}")

                return jsonify({"message": "Login successful", "firstName": current_user.first_name, "parentID": logged_user.id}), 200
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
    print("In the child route")
    logging.info(f"Request method: {request.method}")
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")
        if data.get("role") == "Child":
            parent_id = data.get("parent_id")
            username = data.get("username")
            password = data.get("password")
            role = data.get("role")
            print("Got data!")
            print(f"Received data - username: {username}, Password: {password}, Role: {role}")

            if len(password) < 7:
                return jsonify({'message': "Password must be at least 7 characters long"})
            if not username or not password or not role:
                return jsonify({"message": "All fields are required"}), 400
            print("Before creating child!")
            
            child = Child(parent_id=parent_id, username=username, password=password, role=role)
            print("after creating child!")

            child.save()
            print("working ===>", child)

            wallet = Wallet(child_id=child.id, amount=0.0)
            print(f'wallet {wallet.amount}')
            wallet.save()

            return jsonify({"message": f"User account {username} created successfully", "child_id": child.id}), 201

        else:
            return jsonify({"error": "Invalid role"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid form data: {str(e)}"}), 400
    
@auth.route("/child_login", methods=["POST"])
def child_login():
    print("MADE IT")
    if request.method == "POST":
        
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            role = data.get("role")
            print(data)
            if not username or not password or not role:
                print("Missing email, password, or role")
                return jsonify({"message": "Email, password, and role are required"}), 400
            child = Child.query.filter(Child.username == username).first()
            print(child)
            if child and child.password == password:
                login_user(child)
                print("User logged in successfully")
                print("CURRENT CHILD", current_user.id)


                return jsonify({"message": "Login Successful"}), 200

@auth.route("/test")
@login_required
def test():
    return jsonify({"message": "User is logged in!"})
