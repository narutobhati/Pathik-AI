from flask import Blueprint, jsonify

campaigns_bp = Blueprint("campaigns", __name__)

@campaigns_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "Campaigns service running"}), 200
