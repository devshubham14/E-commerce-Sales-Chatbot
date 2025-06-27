from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from models import db, bcrypt
from chatbot.routes import register_routes
from chatbot_logic import ChatbotLogic

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-this-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # For development, set to False. In production, set to timedelta
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize chatbot logic
    chatbot_logic = ChatbotLogic()
    app.chatbot_logic = chatbot_logic
    
    # Register routes
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize with sample data if database is empty
        from models import Product, User
        if not Product.query.first():
            from chatbot.mock_data import products
            for product_data in products:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    category=product_data['category'],
                    stock_quantity=50,
                    image_url=product_data.get('image_url', '')
                )
                db.session.add(product)
            db.session.commit()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)