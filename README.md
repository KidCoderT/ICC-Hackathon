This repository contains both frontend and backend code for the ICC website project.

# Backend
The backend is built with Python and uses the FastAPI framework. It provides an API that can be consumed by the frontend. To run the backend, follow these steps:

Navigate to the backend directory in the terminal.
Run pip install -r requirements.txt to install the required Python packages.
Run python main.py to start the server.
Open a web browser and go to http://localhost:8000/docs to view the API documentation.

You are required to create a .env file with this
```
# DATABASE
DATABASE_URL = "<MYSQL DB>"

# EMAIL
SENDER_EMAIL_PASSWORD = "<EMAIL_PASSWORD>"
SENDER_EMAIL = "<EMAIL>"
```


# Frontend
The frontend is built with JavaScript using the React.js framework. To run the frontend, follow these steps:

Navigate to the frontend directory in the terminal.
Run npm install to install the required dependencies.
Run npm run dev to start the development server.
Open a web browser and go to http://localhost:3000 to view the website.
Note: The frontend is currently unfinished and may not function properly.

The main page -> shows the matches
/seats/:id -> allows for booking & seat viewing
/book -> actual booking of the seat