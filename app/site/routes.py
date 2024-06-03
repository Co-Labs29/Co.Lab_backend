from flask import Blueprint, request, jsonify
from app.models import Child, Goal, db, Parent
from flask_login import current_user


site = Blueprint('site', __name__)

@site.route('/add_funds', methods=['POST'])
def add_funds():
    try:
        data = request.get_json()
        child_id = data.get("child_id")
        amount = float(data.get("amount"))
        
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "child not found"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Wallet not found for the child"}), 404
        
        wallet.add_amount(amount)
        return jsonify({"message": "Funds added successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@site.route('/transfer/<int:child_id>', methods=['POST'])
def transfer(child_id):
    try:
        data = request.get_json()
        child_id = data.get("child_id")
        amount = float(data.get("amount"))

        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "wallet not found"}), 404
        
        if wallet.transfer_amount(amount):
            return jsonify({"message": "funds transferred successfully"}), 200
        else:
            return jsonify({"error": "Insufficient funds in main account"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@site.route('/balance/<int:child_id>', methods=['GET'])
def get_balance(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404
        
        balance = wallet.get_balance()
        return jsonify({"balance": balance}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


    

@site.route('/goal_balance/<int:child_id>', methods=['GET'])
def goal_balance(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"})
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Amount not found"}), 404
        
        goal_balance = wallet.goal_account
        return jsonify({"balance": goal_balance}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@site.route('/create_goal/<int:child_id>', methods=['POST'])
def create_goal(child_id):
    try:
        data = request.get_json()
        name = data.get("name")
        amount = float(data.get("amount"))
        img = data.get("img")
        link = data.get('link')
        description = data.get('description')

        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Could not find wallet"}), 404
        
        goal = Goal(name=name, amount=amount, img=img, link=link, description=description, wallet_id=wallet.id, child_id=child.id)
        goal.save()

        return jsonify({"message": "Goal created successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@site.route('/update_goal/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    try:
        data = request.get_json()
        new_name = data.get("name")
        new_amount = float(data.get("amount"))
        new_img = data.get("img")
        new_link = data.get("link")
        new_description = data.get("description")

        goal = Goal.query.get(goal_id)
        if not goal:
            return jsonify({"error": "Could not find goal"}), 404
    
        goal.name = new_name
        goal.amount = new_amount
        goal.img = new_img
        goal.link = new_link
        goal.description = new_description
        goal.save()

        return jsonify({"message": "Goal updated successsfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@site.route("/delete_goal/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    try: 
        goal = Goal.query.get(goal_id)
        if not goal:
            return jsonify({"error": "Goal not found"}), 404

        db.session.delete(goal)
        db.session.commit()

        return jsonify({"message": "Goal deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({'Message': str(e)}), 500
    

@site.route('/info', methods=['GET'])
def get_info():
    parent = Parent.query.get(current_user.id)
    if not parent:
        return jsonify({"error": "Parent not found"}), 404
    
    children = Child.query.filter_by(parent_id=current_user.id).all()
    if not children:
        return jsonify({"error": "Children not found"}), 404

    child_info = []
    for child in children:
        child_info.append({
            "child_id": child.id,
            "username": child.username,
            "img": child.img,
            "role": child.role,
            "chores": [chore.name for chore in child.chores],  
            "wallet": {
                "amount": child.wallet.amount
            },
            "goals": [{"id": goal.id, "name": goal.name, "amount": goal.amount, "description": goal.description, "img": goal.img, 
                        "link": goal.link } for goal in child.goals]  
        })

    return jsonify(child_info), 200









@site.route('/child_info/<int:child_id>', methods=['GET'])
def get_child_info(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404

        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        goals = Goal.query.filter_by(child_id=child_id).all()
        goals_info = [
            {
                "id": goal.id,
                "name": goal.name,
                "amount": goal.amount,
                "img": goal.img,
                "link": goal.link,
                "description": goal.description
            } for goal in goals
        ]

        child_info = {
            "child_id": child.id,
            "username": child.username,
            "img": child.img,
            "wallet": {
                "amount": wallet.amount,
                "goal_account": wallet.goal_account
            },
            "goals": goals_info
        }

        return jsonify(child_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

