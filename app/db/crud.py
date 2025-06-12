# Used to manage and maintain database sessions for interacting with the PostgreSQL database
from sqlalchemy.orm import Session

# Imports your database table classes (User, Habit) from the models file to use in CRUD operations
from app.db.models import models

# Imports your Pydantic schema classes (UserCreate, HabitCreate, etc.) to validate request and response data
from app.db.schemas import schemas

# A password hashing utility provided by PassLib; used to hash user passwords securely
from passlib.context import CryptContext

# Allows you to catch and handle database-related errors, like constraint violations or connection issues
from sqlalchemy.exc import SQLAlchemyError

# FastAPI's built-in way to return meaningful HTTP error responses (e.g., 404 Not Found, 500 Internal Server Error)
from fastapi import HTTPException



pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


# Create a user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create User")

# find a single user by id
def read_users(db: Session, user_id: int):
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Could not find User by id")
    
# Find single User by email
def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Could not create User by email")
    
# Delete a User by id
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Delete a User by id
def delete_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"success": True, "message": "User destroyed"}
        return {"success": False, "message": "User not found"}
    except SQLAlchemyError:
        db.rollback()  
        raise HTTPException(status_code=500, detail="An error occurred while trying to delete the user.")

# Create a habit
def create_habit(db: Session, habit:schemas.HabitCreate, user_id = int):
    db_habit = models.Habit(name=habit.name, owner_id=user_id)
    db.add(db_habit)
    try:
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create habit")

# Read a single habit 
def read_habit(db: Session, name: str, user_id: int):
    try:
        return db.query(models.Habit).filter(models.Habit.name == name, models.Habit.owner_id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Could not find habit")

# Read all habits for a single user and sorted alphabetically
def read_all_habits(db: Session, user_id: int):
    try:
        return db.query(models.Habit).filter(models.Habit.owner_id == user_id).order_by(models.Habit.name).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Could not find Users habits")
    
# Delete a habit
def delete_habit_by_id(db: Session, habit_id: int, user_id: int):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id).first()
    try:
        if habit:
            db.delete(habit)
            db.commit()
            return {"success": True, "message": "Habit deleted successfully"}
        return {"success": False, "message": "Habit not found or does not belong to the user"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error in deleting User's habit")

# Update a habit
def update_habit(db: Session, habit_id: int, user_id: int, new_name: str):
    #Finds the habit within the users habits
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user_id).first()
    #if statement to update the name if found and returns not found if the habit is not in the users list
    try:
        if habit:
            habit.name = new_name  
            db.commit()
            db.refresh(habit)
            return {"success": True, "message": "Habit updated", "habit": habit}
        
        return {"success": False, "message": "Habit not found or unauthorized"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error in updating User's habit")
