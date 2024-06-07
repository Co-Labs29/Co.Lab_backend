from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Child, Goal, db, Parent, Wallet


site = Blueprint('site', __name__)

@site.route('/add_funds', methods=['POST'])
@jwt_required()
def add_funds():
    try:
        data = request.get_json()
        child_id = data.get("child_id")
        amount = float(data.get("amount"))
        
        current_user_id = get_jwt_identity()
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({"error": "Child not found or does not belong to the logged-in parent"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Wallet not found for the child"}), 404
        
        wallet.add_amount(amount)
        return jsonify({"message": "Funds added successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@site.route('/transfer/<int:child_id>', methods=['POST'])
@jwt_required()
def transfer(child_id):
    try:
        data = request.get_json()
        paid = float(data.get("paid"))
        goal_id = int(data.get("goal_id"))

        if paid <= 0:
            return jsonify({"error": "Transfer amount must be positive"}), 400

        current_user_id = get_jwt_identity()

        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({"error": "Child not found or does not belong to the logged-in parent"}), 404

        goal = Goal.query.filter_by(id=goal_id, child_id=child.id).first()
        if not goal:
            return jsonify({"error": "Goal not found"}), 404

        wallet = Wallet.query.filter_by(id=child.wallet.id).first()
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        if goal.paid >= goal.amount:
            return jsonify({"error": "Goal has already been fully paid"}), 400

        if wallet.amount < paid:
            return jsonify({"error": "Insufficient funds in wallet"}), 400
        
        if goal.paid + paid > goal.amount:
            return jsonify({"error": "Transfer amount exceeds the goal amount"}), 400
        

        goal.paid += paid
        wallet.amount -= paid
        db.session.commit()
        print(f'goal.paid{goal.paid} wallet.amount{wallet.amount} goal.amount{goal.amount}')
        
        return jsonify({"message": "Funds transferred successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@site.route('/goal_balance/<int:child_id>', methods=['GET'])
@jwt_required()
def goal_balance(child_id):
    try:
       
        current_user_id = get_jwt_identity()

   
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({"error": "Child not found or does not belong to the logged-in parent"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404
        
        goal_balance = wallet.goal_account
        return jsonify({"balance": goal_balance}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@site.route('/create_goal/<int:child_id>', methods=['POST'])
@jwt_required()
def create_goal(child_id):
    try:
        data = request.get_json()
        name = data.get("name")
        amount = float(data.get("amount"))
        img = data.get("img")
        link = data.get('link')
        description = data.get('description')

       
        current_user_id = get_jwt_identity()

       
        child = Child.query.filter_by(id=child_id, parent_id=current_user_id).first()
        if not child:
            return jsonify({"error": "Child not found or does not belong to the logged-in parent"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Could not find wallet"}), 404
        
        goal = Goal(name=name, amount=amount, img=img, link=link, description=description, wallet_id=wallet.id, child_id=child.id)
        goal.save()

        return jsonify({"message": "Goal created successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



    
@site.route('/update_goal/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    try:
        data = request.get_json()
        new_name = data.get("name")
        new_amount = float(data.get("amount"))
        new_paid = float(data.get('paid'))
        new_img = data.get("img")
        new_link = data.get("link")
        new_description = data.get("description")
        current_user_id = get_jwt_identity()

        
        goal = Goal.query.filter_by(id=goal_id).first()
        if not goal or goal.child.parent_id != current_user_id:
            return jsonify({"error": "Could not find goal or unauthorized access"}), 404
    
        goal.name = new_name
        goal.amount = new_amount
        goal.paid = new_paid
        goal.img = new_img
        goal.link = new_link
        goal.description = new_description
        goal.save()

        return jsonify({"message": "Goal updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@site.route("/delete_goal/<int:goal_id>", methods=["DELETE"])
@jwt_required()
def delete_goal(goal_id):
    try: 
        
        current_user_id = get_jwt_identity()

        goal = Goal.query.filter_by(id=goal_id).first()
        if not goal or goal.child.parent_id != current_user_id:
            return jsonify({"error": "Goal not found or unauthorized access"}), 404

        db.session.delete(goal)
        db.session.commit()

        return jsonify({"message": "Goal deleted successfully"}), 200
    except Exception as e:
        return jsonify({'Message': str(e)}), 500

@site.route('/info', methods=['GET'])
@jwt_required()
def get_info():
    try:
        current_user_id = get_jwt_identity()
        print(f'current_user_id {current_user_id}')
        parent = Parent.query.get(current_user_id)
        if parent:
           
            children = Child.query.filter_by(parent_id=current_user_id).all()
        else:
            
            child = Child.query.get(current_user_id)
            if not child:
                return jsonify({"error": "Child not found"}), 404
            parent = Parent.query.get(child.parent_id)
            if not parent:
                return jsonify({"error": "Parent not found"}), 404
           
            children = Child.query.filter_by(parent_id=parent.id).all()

        
        if not children:
            return jsonify({"error": "Children not found"}), 404

        child_info = []
        for child in children:
            child_info.append({
                "parent_id": child.parent.id,
                "child_id": child.id,
                "username": child.username,
                "img": child.img,
                "role": child.role,
                "chores": [{"name": chores.name, "amount":chores.amount} for chores in child.chores],  
                "wallet": {
                    "amount": child.wallet.amount
                },
                "goals": [{"id": goal.id, "name": goal.name, "amount": goal.amount, "paid": goal.paid, "description": goal.description, "img": goal.img, 
                            "link": goal.link } for goal in child.goals]  
            })

        return jsonify(child_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
    


