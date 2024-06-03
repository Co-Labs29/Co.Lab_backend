from flask import Blueprint, request, jsonify
from app.models import Child

parents = Blueprint("parent", __name__)


@parents.route("/my_children/<parent_id>", methods=['GET'])
def get_all_children(parent_id):
    try:
        all_children = Child.query.filter_by(parent_id=parent_id).all()  # Fixed line
        print(all_children)
        return jsonify({"children": all_children})
    except Exception as e:
        print(f"ERROR GETTING CHILDREN: {e}")
    return jsonify([child.to_dict() for child in all_children]), 200  # Optionally return the children as JSON
