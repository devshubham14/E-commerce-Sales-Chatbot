# E-commerce Sales Chatbot Backend Documentation

## Overview
The E-commerce Sales Chatbot is a full-stack web application that integrates a chatbot with an e-commerce platform. The backend is built using Python Flask, providing RESTful API endpoints for user authentication, product queries, and chatbot interactions.

## Project Structure
```
ecommerce-sales-chatbot/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── mock_data.py
│   └── README.md
└── frontend/
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-sales-chatbot/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   The backend will be running on `http://localhost:5000`.

## API Endpoints

### User Authentication
- **POST /api/register**: Register a new user.
- **POST /api/login**: Authenticate a user and return a JWT token.

### Product Queries
- **GET /api/products**: Retrieve a list of products.
- **GET /api/products/<product_id>**: Retrieve details of a specific product.

### Chatbot Interaction
- **POST /api/chat**: Send a message to the chatbot and receive a response.

## Architectural Decisions
- The application uses Flask for its simplicity and flexibility in building RESTful APIs.
- SQLite is chosen as the database for its lightweight nature, making it suitable for development and testing.

## Challenges Faced
- Integrating the chatbot with the e-commerce product database required careful planning of the API endpoints.
- Ensuring secure user authentication with JWT tokens was crucial for protecting user data.

## Solutions Implemented
- Implemented a modular structure for the chatbot functionality to keep the code organized.
- Used Flask-JWT-Extended for secure user authentication and session management.

## Future Improvements
- Implement a more robust database solution for production.
- Enhance the chatbot's capabilities with machine learning for better user interaction.

## License
This project is licensed under the MIT License.