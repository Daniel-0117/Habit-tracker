from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.security import verify_pwd, create_access_token, authenticate_user, get_current_user
from app.db.crud import get_user_by_email, create_user, read_habit, delete_habit, create_habit
from app.db.schemas import UserCreate, User, HabitCreate, HabitUpdate, Habit
from app.db.models import User

router = APIRouter()

@router.get("/token-test", response_model=User)
def test_token(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, user_data)
    return user

@router.post("/habits/")
def habit_create(
        habit: HabitCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_habit(db, habit, user_id=current_user.id)

@router.get("/users/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("habits/", response_model=User)
def get_all_habits(
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_habits(db, user_id=current_user.id)


@router.delete("/habits/{habit_id}", status_code=204)
def delete_habit_by_id(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_habit = read_habit(db, habit_id=habit_id, user_id=current_user.id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return delete_habit(db, habit_id)

from app.db.schemas import HabitUpdate  

@router.patch("/habits/{habit_id}", response_model=Habit)
def update_habit_by_id(
    habit_id: int,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_habit = read_habit(db, habit_id=habit_id, user_id=current_user.id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit_data.name is not None:
        db_habit.name = habit_data.name

    db.commit()
    db.refresh(db_habit)
    return db_habit
