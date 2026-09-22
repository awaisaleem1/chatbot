from database import Base, SessionLocal, engine
from models import Admin


def seed_admin():
    # Create database tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        admin_email = "admin@example.com"

        existing_admin = (
            db.query(Admin)
            .filter(Admin.email == admin_email)
            .first()
        )

        if existing_admin:
            print(f"Admin already exists: {admin_email}")
            return

        admin = Admin(email=admin_email)

        db.add(admin)
        db.commit()

        print(f"Admin created successfully: {admin_email}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()