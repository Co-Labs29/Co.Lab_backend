from flask import Blueprint, request, jsonify
from app.models import Child, Chores

chores = Blueprint("chores", __name__)

@chores.route("/add_chore/<child_id>", methods=["POST"])
def add_chore(child_id):
    try:
        data = request.get_json()
        name = data.get("name")
        frequency = data.get("frequency")
        due_date = data.get("due_date")
        if not name or not frequency or not due_date:
            return jsonify({"message": "Missing required fields"}), 400

        child = Child.query.get(child_id)
        if not child:
            return jsonify({"message": "Child not found"}), 404
        
        new_chore = Chores(name=name, frequency=frequency, due_date=due_date, child_id=child_id)

        new_chore.save()

        if not new_chore:
            return jsonify({"message": "Failed to create chore"}), 400
        else:
            return jsonify({"message": "Chore created successfully"}), 200

    except:
        return jsonify({"message": "Error creating chore"}), 500