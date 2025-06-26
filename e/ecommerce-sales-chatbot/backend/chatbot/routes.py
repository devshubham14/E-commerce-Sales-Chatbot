from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .mock_data import products

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@chatbot_bp.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    user_message = request.json.get('message')
    # Here you would implement the logic to process the user message
    # and generate a response. For now, we will return a mock response.
    response = {
        "response": f"You said: {user_message}. How can I assist you with our products?"
    }
    return jsonify(response), 200

@chatbot_bp.route('/api/register', methods=['POST'])
def register():
    # Logic for user registration
    return jsonify({"msg": "User registered successfully."}), 201

@chatbot_bp.route('/api/login', methods=['POST'])
def login():
    # Logic for user login
    return jsonify({"msg": "User logged in successfully."}), 200