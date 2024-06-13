from flask import Blueprint, jsonify
from app.models import Chores, Wallet


wallet = Blueprint('wallet', __name__)

@wallet.route("/add_funds_to_wallet/<int:child_id>/<int:chore_id>", methods=["PUT"])
def add_funds_to_wallet(child_id: int, chore_id: int,):
    try:
        # Log the child_id and chore_id for debugging
        print("Child_id ====>", child_id)
        print("Chore_id ====>", chore_id)

        # Fetch the chore by ID
        chore = Chores.query.get(chore_id)
        if not chore:
            return jsonify({"message": "Chore not found"}), 404

        # Fetch the wallet by child_id
        wallet = Wallet.query.filter_by(child_id=child_id).first()
        if not wallet:
            return jsonify({"message": "Wallet not found"}), 404

        # Log the chore amount for debugging
        print("Chore amount ====>", chore.amount)

        # Add funds to the wallet and commit the transaction
        wallet.amount += chore.amount
        wallet.save()

        return jsonify({"message": "Funds successfully added to wallet"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



