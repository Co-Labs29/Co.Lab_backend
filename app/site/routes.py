from flask import Blueprint, request, jsonify
from app.models import Child


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

        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404
        
        wallet = child.wallet
        if not wallet:
            return jsonify({"error": "Could not find wallet"}), 404
        
        goals = Goals(name=name, amount=amount, wallet_id=wallet.id, child_id=child.id)
        goals.save()

        return jsonify({"message": "Goal created successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500