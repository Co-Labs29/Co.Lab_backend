from flask import Blueprint, request, jsonify
from app.models import Child, Parent

parents = Blueprint("parent", __name__)


@parents.route("/my_children/<parent_id>", methods=['GET'])
def get_all_children(parent_id):
    try:
        
        all_children = Child.query.filter_by(parent_id=parent_id).all() 
        print(all_children)
        return jsonify({"children": all_children})
    except Exception as e:
        print(f"ERROR GETTING CHILDREN: {e}")
    return jsonify([child.to_dict() for child in all_children]), 200

@parents.route("/parent_info/<parent_id>", methods=["GET"])
def get_parent_info_by_id(parent_id):
    try:
        print("IM INNNNNn")
        parent = Parent.query.filter_by(id=parent_id).first()
        print(parent.to_dict())
        if not parent:
            return jsonify({"message": "Parent not found"})
        return jsonify({"parent": parent.to_dict()})

    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

