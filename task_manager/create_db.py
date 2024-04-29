# File: create_db.py

from app import app, db

def create_database():
    with app.app_context():#we ensure that the necessary application context is set up before calling db.create_all()
        try:
            db.create_all()
            print("Database created successfully.")
        except Exception as e:
            print("Error creating database:", e)

if __name__ == "__main__":
    create_database()
