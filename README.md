# E-commerce-Sales-Chatbot
E-commerce Sales Chatbot
This project is a full-stack web application that integrates a chatbot for e-commerce sales. The application is built using React.js for the frontend and Python Flask for the backend. The chatbot assists users in finding products, answering queries, and facilitating a seamless shopping experience.

Project Structure
ecommerce-sales-chatbot
├── backend
│   ├── app.py
│   ├── requirements.txt
│   ├── chatbot
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── mock_data.py
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components
│   │   │   ├── Chatbot.js
│   │   │   └── ProductList.js
│   │   └── mockData.js
│   ├── package.json
│   └── README.md
└── README.md
Getting Started
Prerequisites
Python 3.x
Node.js and npm
Backend Setup
Navigate to the backend directory:

cd backend
Install the required Python packages:

pip install -r requirements.txt
Run the Flask application:

python app.py
Frontend Setup
Navigate to the frontend directory:

cd frontend
Install the required npm packages:

npm install
Start the React application:

npm start
Features
User authentication (registration and login)
Chatbot interface for product queries
Display of product listings
Mock data for testing purposes
API Endpoints
POST /api/register: Register a new user
POST /api/login: Authenticate a user
GET /api/products: Retrieve a list of products
POST /api/chat: Send a message to the chatbot and receive a response
Architectural Decisions
The backend is built using Flask for its simplicity and ease of use in creating RESTful APIs.
The frontend is developed with React.js to provide a dynamic and responsive user interface.
Mock data is utilized for both backend and frontend to facilitate testing without requiring a live database.
Challenges Faced
Integrating the chatbot with the product database required careful planning of the API endpoints.
Ensuring smooth communication between the frontend and backend necessitated thorough testing of API responses.
Solutions Implemented
Used Flask-JWT-Extended for secure user authentication.
Implemented error handling in API routes to provide meaningful feedback to the frontend.
Acknowledgments
Special thanks to the open-source community for providing libraries and tools that made this project possible.
