from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, Order, OrderItem, CartItem, ChatMessage
from chatbot_logic import ChatbotLogic
import re

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize chatbot logic
chatbot_logic = ChatbotLogic()

@chatbot_bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token,
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({"error": "Missing username or password"}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter(Product.category.ilike(f'%{category}%'))
        
        if search:
            query = query.filter(
                (Product.name.ilike(f'%{search}%')) |
                (Product.description.ilike(f'%{search}%'))
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        products = query.all()
        
        return jsonify([product.to_dict() for product in products]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = db.session.query(Product.category).distinct().all()
        return jsonify([category[0] for category in categories]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Fetch chat history for the current user"""
    try:
        user_id = get_jwt_identity()
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.asc()).all()
        return jsonify([msg.to_dict() for msg in messages]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/chat/reset', methods=['POST'])
@jwt_required()
def reset_chat_history():
    """Delete all chat history for the current user"""
    try:
        user_id = get_jwt_identity()
        ChatMessage.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return jsonify({"message": "Chat history reset."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    """Process chatbot messages and persist chat history"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        user_message = data['message']
        # Save user message
        user_msg = ChatMessage(user_id=user_id, message=user_message, sender='user')
        db.session.add(user_msg)
        db.session.commit()
        # Generate response using chatbot logic
        response = chatbot_logic.generate_response(user_message, user_id)
        # Save bot response
        bot_msg = ChatMessage(user_id=user_id, message=response, sender='bot')
        db.session.add(bot_msg)
        db.session.commit()
        return jsonify({
            "response": response,
            "user_id": user_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart items"""
    try:
        user_id = get_jwt_identity()
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        cart_data = []
        total = 0
        
        for item in cart_items:
            product = item.product
            item_total = product.price * item.quantity
            total += item_total
            
            cart_data.append({
                'id': item.id,
                'product': product.to_dict(),
                'quantity': item.quantity,
                'total': item_total
            })
        
        return jsonify({
            "items": cart_data,
            "total": total,
            "item_count": len(cart_data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        if not product.is_active:
            return jsonify({"error": "Product is not available"}), 400
        
        if product.stock_quantity < quantity:
            return jsonify({"error": "Insufficient stock"}), 400
        
        # Check if item already in cart
        existing_item = CartItem.query.filter_by(
            user_id=user_id, 
            product_id=product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({"message": "Item added to cart successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/cart/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        quantity = data.get('quantity')
        
        if quantity is None or quantity < 1:
            return jsonify({"error": "Valid quantity is required"}), 400
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=user_id
        ).first()
        
        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404
        
        # Check stock availability
        if cart_item.product.stock_quantity < quantity:
            return jsonify({"error": "Insufficient stock"}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({"message": "Cart item updated successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        user_id = get_jwt_identity()
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=user_id
        ).first()
        
        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({"message": "Item removed from cart successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/cart/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        user_id = get_jwt_identity()
        
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({"message": "Cart cleared successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        shipping_address = data.get('shipping_address')
        
        if not shipping_address:
            return jsonify({"error": "Shipping address is required"}), 400
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400
        
        # Calculate total and validate stock
        total_amount = 0
        order_items = []
        
        for cart_item in cart_items:
            product = cart_item.product
            
            if product.stock_quantity < cart_item.quantity:
                return jsonify({
                    "error": f"Insufficient stock for {product.name}"
                }), 400
            
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            # Create order item
            order_item = OrderItem(
                product_id=product.id,
                quantity=cart_item.quantity,
                price_at_time=product.price
            )
            order_items.append(order_item)
            
            # Update stock
            product.stock_quantity -= cart_item.quantity
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add order items
        for order_item in order_items:
            order_item.order_id = order.id
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            "message": "Order created successfully",
            "order": order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify([order.to_dict() for order in orders]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get specific order details"""
    try:
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify(order.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def register_routes(app):
    """Register all routes with the Flask app"""
    app.register_blueprint(chatbot_bp)