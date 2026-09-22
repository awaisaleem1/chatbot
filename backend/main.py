from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
from ai_service import parse_command
from command_executor import execute_command
from database import Base, engine, get_db
from schemas import LoginRequest, LoginResponse


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="AI User Management Chatbot",
    description="Natural language user management chatbot",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI User Management Chatbot API is running"
    }


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.post(
    "/auth/login",
    response_model=LoginResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    admin = crud.get_admin_by_email(
        db,
        login_data.email
    )

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Email is not authorized."
        )

    return LoginResponse(
        success=True,
        message="Login successful."
    )


# --------------------------------------------------
# CHAT
# --------------------------------------------------

@app.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db)
):
    try:

        # Step 1:
        # Convert natural language into structured command
        command = parse_command(message)

        # Step 2:
        # Execute the structured command
        result = execute_command(
            db,
            command
        )

        return {
            "success": result["success"],
            "message": result["message"],
            "command": command.model_dump()
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }


# --------------------------------------------------
# GET USERS
# --------------------------------------------------

@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = crud.get_users(db)

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "city": user.city,
        }
        for user in users
    ]