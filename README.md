# AI User Management Chatbot

An AI-powered user management chatbot built with **FastAPI, React, SQLite, SQLAlchemy, and a local open-source LLM**.

The application allows an authorized admin to manage users through natural-language chat commands instead of traditional forms.

## Features

* Admin email-based login
* Natural-language user management
* Create users
* Update user information
* Delete users
* Get individual user information
* List all users
* React-based chat interface
* SQLite database
* SQLAlchemy ORM
* Local AI model using Hugging Face Transformers
* No external AI API key required
* Automatic user list refresh after operations
* REST API built with FastAPI
* CORS support for local frontend/backend development

## Example Commands

### Create a user

```text
Add a user named John Smith with email john.smith@xyz.com,
phone +923321234567 and city Lahore
```

### Update a user

```text
Update John's city to Islamabad
```

Or:

```text
Update this user "john.smith@xyz.com" phone to "+923331234567"
```

### Delete a user

```text
Remove the user "john.smith@xyz.com"
```

### Get user information

```text
Show information about John Smith
```

### List users

```text
Show all users
```

## Architecture

```text
┌──────────────────────────────┐
│          React UI            │
│                              │
│ Login + Chat + User List     │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│                              │
│ /auth/login                  │
│ /chat                        │
│ /users                       │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌────────────────┐
│ AI Parser    │  │ Command        │
│              │  │ Executor       │
│ Qwen 0.5B    │  │                │
│ Transformers │  │ Business Logic │
└──────────────┘  └───────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ SQLite Database │
                  │                 │
                  │ Admins          │
                  │ Users           │
                  └─────────────────┘
```

## How It Works

The application separates **AI interpretation** from **database operations**.

### 1. User enters a natural-language command

For example:

```text
Add Awais with email awais@example.com,
phone 03123456789 and city Lahore
```

### 2. AI parses the command

The local Qwen model converts the message into structured JSON:

```json
{
  "action": "create_user",
  "email": "awais@example.com",
  "identifier": null,
  "name": "Awais",
  "phone": "03123456789",
  "city": "Lahore",
  "field": null,
  "value": null
}
```

### 3. Pydantic validates the command

The generated JSON is validated against the application's `UserCommand` schema.

### 4. Python executes the operation

The command executor determines what database operation needs to happen.

The LLM does **not** directly execute SQL or modify the database.

### 5. SQLAlchemy updates SQLite

The application performs the required database operation through SQLAlchemy.

### 6. Result is returned to React

The frontend displays the operation result in the chat interface and refreshes the user list.

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

### AI

* Hugging Face Transformers
* PyTorch
* Qwen2.5-0.5B-Instruct

### Frontend

* React
* Vite
* JavaScript
* CSS

## Project Structure

```text
chatbot-task/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── ai_service.py
│   ├── command_executor.py
│   ├── seed.py
│   └── chatbot.db
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Login.jsx
│   │   ├── Chat.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

# Installation

## Prerequisites

Make sure the following are installed:

* Python 3.10+
* Node.js 18+
* npm

## 1. Clone the project

```bash
git clone <your-repository-url>
cd chatbot-task
```

## 2. Create Python virtual environment

From the project root:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install backend dependencies

```bash
cd backend
pip install -r ../requirements.txt
```

## 4. Create the admin account

Run:

```bash
python seed.py
```

You should see:

```text
Admin created successfully: admin@example.com
```

The default admin email is:

```text
admin@example.com
```

If the admin already exists, you may see:

```text
Admin already exists: admin@example.com
```

That is also fine.

## 5. Start the backend

Make sure you are inside the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 6. Start the frontend

Open another terminal.

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

Open the URL in your browser.

## Login

Use the seeded admin email:

```text
admin@example.com
```

No password is required for this simplified assignment implementation.

## API Endpoints

### Login

```http
POST /auth/login
```

Request:

```json
{
  "email": "admin@example.com"
}
```

Response:

```json
{
  "success": true,
  "message": "Login successful."
}
```

### Chat

```http
POST /chat
```

Example:

```text
Add John with email john@example.com and city Lahore
```

The backend returns the operation result and the parsed command.

### Get Users

```http
GET /users
```

Returns all users currently stored in the database.

## Database

The application uses SQLite.

Database file:

```text
backend/chatbot.db
```

### Admin table

Stores authorized admin email addresses.

### Users table

Stores:

* ID
* Name
* Email
* Phone
* City
* Created timestamp
* Updated timestamp

## AI Design

The LLM is used specifically for **natural-language command extraction**.

It does not directly control the database.

The processing pipeline is:

```text
Natural Language
       ↓
Qwen2.5-0.5B-Instruct
       ↓
Structured JSON
       ↓
Pydantic Validation
       ↓
Command Executor
       ↓
SQLAlchemy
       ↓
SQLite
```

This separation keeps database operations deterministic and prevents the LLM from directly generating or executing SQL.

## Why a Local Model?

The application uses:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The model is downloaded from Hugging Face and runs locally using PyTorch.

Advantages:

* No OpenAI API key
* No paid API
* No external inference service
* Better privacy for user data
* Easy local development
* Suitable for this narrow command-extraction task

## Error Handling

The application handles common cases such as:

* Missing email during user creation
* Duplicate email addresses
* User not found
* Missing update field
* Missing update value
* Invalid AI output
* Invalid command structure

Pydantic is used to validate AI-generated structured commands before they reach the command executor.

## Security Notes

This project intentionally uses a simple email-based authentication mechanism because the assignment specifies simple auto-login behavior.

For a production application, authentication should be extended with:

* Password authentication or OAuth
* JWT/session-based authentication
* Role-based authorization
* HTTPS
* Rate limiting
* Audit logging
* CSRF protection where applicable
* Stronger command validation
* Confirmation before destructive operations such as deletion

## Future Improvements

Possible improvements include:

* JWT authentication
* Admin dashboard
* User search and filtering
* Pagination
* Delete confirmation
* Multiple-field updates in a single command
* Conversation history
* Audit logs
* Better structured-output enforcement
* Larger instruction-tuned model for improved natural-language understanding
* Docker deployment
* PostgreSQL support
* Automated tests
* Production deployment

## Development

Backend:

```bash
cd backend
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

## Assignment Goal

The purpose of this project is to demonstrate how an AI-powered natural-language interface can be connected to deterministic backend business logic and a database.

The key design principle is:

> **AI interprets the user's intent; application code executes the operation.**

## Author

**Awais Aleem**

Computer Science Graduate
AI/ML & Python Developer

GitHub: `awaisaleem1`
