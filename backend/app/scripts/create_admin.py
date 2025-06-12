from app.database import SessionLocal
from app.models.user import User
from passlib.hash import bcrypt

def run():
    db = SessionLocal()
    try:
        email = "admin@example.com"
        password = "admin123"
        username = "admin"

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("Admin już istnieje – pomijam")
            return

        user = User(
            username=username,
            email=email,
            password=bcrypt.hash(password),
            is_admin=True
        )
        db.add(user)
        db.commit()
        print(f"Admin utworzony: {email}")
    finally:
        db.close()

if __name__ == "__main__":
    run()