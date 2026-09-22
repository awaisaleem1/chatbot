from sqlalchemy.orm import Session

from models import Admin, User
from schemas import UserCreate


# -------------------------
# ADMIN
# -------------------------

def get_admin_by_email(
    db: Session,
    email: str
):
    return (
        db.query(Admin)
        .filter(Admin.email == email)
        .first()
    )


def create_admin(
    db: Session,
    email: str
):
    admin = Admin(email=email)

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin


# -------------------------
# USER
# -------------------------

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_users(db: Session):
    return db.query(User).all()


def create_user(
    db: Session,
    user_data: UserCreate
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        city=user_data.city
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user_field(
    db: Session,
    user: User,
    field: str,
    value: str
):
    setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):
    db.delete(user)

    db.commit()

    return True