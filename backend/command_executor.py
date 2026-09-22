from sqlalchemy.orm import Session

from crud import (
    create_user,
    delete_user,
    get_user_by_email,
    get_users,
    update_user_field,
)
from schemas import UserCommand, UserCreate


def find_user(
    db: Session,
    command: UserCommand
):
    """
    Find a user using email or identifier/name.
    """

    # First try email
    if command.email:
        user = get_user_by_email(db, command.email)

        if user:
            return user

    # Then try identifier
    if command.identifier:
        identifier = command.identifier.strip()

        # Try email first in case identifier contains an email
        user = get_user_by_email(db, identifier)

        if user:
            return user

        # Search by name
        user = (
            db.query(__import__("models").User)
            .filter(
                __import__("models").User.name.ilike(identifier)
            )
            .first()
        )

        if user:
            return user

    return None


def execute_command(
    db: Session,
    command: UserCommand
):
    """
    Execute a validated UserCommand.
    """

    # --------------------------------
    # CREATE USER
    # --------------------------------

    if command.action == "create_user":

        if not command.email:
            return {
                "success": False,
                "message": "Email is required to create a user."
            }

        existing_user = get_user_by_email(
            db,
            command.email
        )

        if existing_user:
            return {
                "success": False,
                "message": "A user with this email already exists."
            }

        user_data = UserCreate(
              name=command.name,
              email=command.email,
              phone=command.phone,
               city=command.city
            )

        user = create_user(
            db,
            user_data
        )

        return {
            "success": True,
            "message": f"User {user.email} was created successfully."
        }

    # --------------------------------
    # FIND USER
    # --------------------------------

    user = find_user(
        db,
        command
    )

    # --------------------------------
    # UPDATE USER
    # --------------------------------

    if command.action == "update_user":

        if not user:
            return {
                "success": False,
                "message": "I couldn't find that user."
            }

        if not command.field:
            return {
                "success": False,
                "message": "Which user field would you like to update?"
            }

        if command.value is None:
            return {
                "success": False,
                "message": "Please provide the new value."
            }

        # Prevent duplicate email addresses
        if command.field == "email":

            existing_user = get_user_by_email(
                db,
                command.value
            )

            if existing_user and existing_user.id != user.id:
                return {
                    "success": False,
                    "message": "Another user already has this email."
                }

        updated_user = update_user_field(
            db,
            user,
            command.field,
            command.value
        )

        return {
            "success": True,
            "message": (
                f"User {updated_user.email} was updated successfully. "
                f"{command.field} is now {command.value}."
            )
        }

    # --------------------------------
    # DELETE USER
    # --------------------------------

    if command.action == "delete_user":

        if not user:
            return {
                "success": False,
                "message": "I couldn't find that user."
            }

        email = user.email

        delete_user(
            db,
            user
        )

        return {
            "success": True,
            "message": f"User {email} was deleted successfully."
        }

    # --------------------------------
    # GET USER
    # --------------------------------

    if command.action == "get_user":

        if not user:
            return {
                "success": False,
                "message": "I couldn't find that user."
            }

        return {
            "success": True,
            "message": (
                f"Name: {user.name or 'Not provided'}\n"
                f"Email: {user.email}\n"
                f"Phone: {user.phone or 'Not provided'}\n"
                f"City: {user.city or 'Not provided'}"
            )
        }

    # --------------------------------
    # LIST USERS
    # --------------------------------

    if command.action == "list_users":

        users = get_users(db)

        if not users:
            return {
                "success": True,
                "message": "There are no users in the system."
            }

        user_list = []

        for user in users:
            user_list.append(
                f"{user.name or 'Unknown'} - {user.email}"
            )

        return {
            "success": True,
            "message": "\n".join(user_list)
        }

    return {
        "success": False,
        "message": "I don't understand that command."
    }