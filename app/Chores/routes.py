from flask import Blueprint, request, jsonify
from app.models import Child, Chores


chores = Blueprint("chores", __name__)

@chores.route("/add_chore/<child_id>/<parent_id>", methods=["POST"])
def add_chore(child_id, parent_id):
    try:
        data = request.get_json()
        print("data ======>", data)
        print("child_id ======>", child_id)
        name = data.get("name")
        frequency = data.get("frequency")
        due_date = data.get("due_date")
        amount = data.get("amount")
        print(name, frequency, due_date, type(amount))

        if not name or not frequency or not due_date:
            return jsonify({"message": "Missing required fields"}), 400
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"message": "Child not found"}), 404
        
        new_chore = Chores(name=name, frequency=frequency, due_date=due_date, child_id=child_id, amount=amount, parent_id=parent_id)

        new_chore.save()

        if not new_chore:
            return jsonify({"message": "Failed to create chore"}), 400
        else:
            return jsonify({"message": "Chore created successfully"}), 200

    except:
        return jsonify({"message": "Error creating chore"}), 500
    
def add_child_details_to_chore(chore):
    chore_dict = chore.to_dict()
    child = Child.query.filter_by(id=chore.child_id).first()
    if child:
        chore_dict.update({
            "child_id": child.id,
            "child_username": child.username,
            "child_role": child.role,
            "child_img": child.img
        })
        return chore_dict
    else:
        return False



@chores.route("/all_chores/<parent_id>", methods=["GET"])
def get_all_chores_by_parent_id(parent_id):
    try:
        if not parent_id:
            return jsonify({"message": "Parent not found"})
        print("Parent_id ===>",parent_id)
        all_chores = Chores.query.filter_by(parent_id=parent_id).all()
        chores_list = [add_child_details_to_chore(chore) for chore in all_chores]

        return jsonify({"all_chores": chores_list}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error getting chores"}), 500
    
@chores.route("/get_chores/<int:child_id>/<string:due_date>")
def get_chores_by_child_and_due_date(child_id, due_date):
    try:
        # Assuming child_id and due_date are valid and correctly formatted
        if not child_id:
            return jsonify({"message": "Please select a child"})
        if not due_date:
            return jsonify({"message": "Please select a date"})
        chores = Chores.query.filter_by(child_id=child_id, due_date=due_date).all()
        if not chores:
            return jsonify({"message": "No chores found"}), 404  # Use 404 for "Not Found"
        else:
            chore_list = [chore.to_dict() for chore in chores]
            return jsonify({"chores": chore_list}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error getting chores"}), 500
    
@chores.route("/update_chore_status/<int:chore_id>", methods=["PUT"])
def update_chore_status_by_id(chore_id):
    try:
        data = request.json
        chore = Chores.query.get(chore_id)
        if not chore:
            return jsonify({"message": "Chore not found"}), 404
        if "status" in data:
            chore.status = data['status']
            chore.save()
            return jsonify({"message": "Chore status updated successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error updating chore"}), 500
    
    
