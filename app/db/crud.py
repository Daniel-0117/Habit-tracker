from sqlalchemy.orm import Session
from app.db.models import models
from app.db.schemas import schemas
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


# Create a user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# find a single user by id
def read_users(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Find single User by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Delete a User by id
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"success": True, "message": "User destroyed"}
    return {"success": False, "message": "User not found"}

#Create a habit
def create_habit(db: Session, habit:schemas.HabitCreate, user_id = int):
    db_habit = models.Habit(name=habit.name, owner_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

# Read a single habit 
def read_habit(db: Session, name: str, user_id: int):
    return db.query(models.Habit).filter(models.Habit.name == name, models.Habit.owner_id == user_id).first()

# Read all habits for a single user and sorted alphabetically
def read_all_habits(db: Session, user_id: int):
    return db.query(models.Habit).filter(models.Habit.owner_id == user_id).order_by(models.Habit.name).all()

# Delete a habit
def delete_habit_by_id(db: Session, habit_id: int, user_id: int):
    habit = db.query(models.Habit).filter(
        models.Habit.id == habit_id,
        models.Habit.owner_id == user_id).first()

    if habit:
        db.delete(habit)
        db.commit()
        return {"success": True, "message": "Habit deleted successfully"}
    return {"success": False, "message": "Habit not found or does not belong to the user"}

# Update a habit
def update_habit(db: Session, habit_id: int, user_id: int, new_name: str):
    #Finds the habit within the users habits
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.owner_id == user_id).first()
    #if statement to update the name if found and returns not found if the habit is not in the users list
    if habit:
        habit.name = new_name  
        db.commit()
        db.refresh(habit)
        return {"success": True, "message": "Habit updated", "habit": habit}
    
    return {"success": False, "message": "Habit not found or unauthorized"}
