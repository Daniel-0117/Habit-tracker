from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.security import get_current_user
from app.db.crud import create_habit, read_habit, delete_habit, get_all_habits 
from app.db.schemas import HabitCreate, HabitUpdate, Habit, User
from app.db.models import User

router = APIRouter()

@router.post("/habits/")
def habit_create(
        habit: HabitCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_habit(db, habit, user_id=current_user.id)

@router.get("/habits/", response_model=List[Habit])
def list_user_habits(
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