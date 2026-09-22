from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.academy_models import UserPermission
from datetime import datetime


def create_super_admin():
    db: Session = SessionLocal()
    try:
        existing_user = db.query(UserPermission).first()
        if existing_user:
            print("SuperAdmin already exists, skipping...")
            return

        super_admin = UserPermission(
            user_name="superadmin",
            password="12345",  # You should hash this password in production
            user_role="admin",
            mobile_number="9999999999",
            edit=True,
            delete=True,
            upload=True
        )
        db.add(super_admin)
        db.commit()
        print("SuperAdmin created successfully!")
        print("Username: superadmin")
        print("Password: 12345")
        print("Role: admin")

    except Exception as e:
        db.rollback()
        print("Error creating SuperAdmin:", e)
    finally:
        db.close()


def create_sumit_user():
    db: Session = SessionLocal()
    try:
        existing_sumit = db.query(UserPermission).filter(UserPermission.user_name == "sumit").first()
        if existing_sumit:
            print("Sumit user already exists, skipping...")
            return

        sumit_user = UserPermission(
            user_name="sumit",
            password="12345",  # You should hash this password in production
            user_role="admin",
            mobile_number="1234567890",
            edit=True,
            delete=True,
            upload=True
        )
        db.add(sumit_user)
        db.commit()
        print("Sumit user created successfully!")
        print("Username: sumit")
        print("Password: 12345")
        print("Role: admin")

    except Exception as e:
        db.rollback()
        print("Error creating Sumit user:", e)
    finally:
        db.close()