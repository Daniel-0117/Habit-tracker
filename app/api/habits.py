from fastapi import APIRouter, Depends, HTTPException
import logging
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.security import get_current_user
from app.db.crud import create_habit, get_habit, delete_habit_by_id, get_all_habits 
from app.db.schemas import HabitCreate, HabitUpdate, Habit
from app.db.models import User

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@router.post("/habits/", response_model=Habit, status_code=201)
def habit_create(
        habit: HabitCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_habit(db, habit, user_id=current_user.id)

@router.get("/", response_model=List[Habit])
def list_user_habits(
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_habits(db, user_id=current_user.id)

@router.delete("/{habit_id}", status_code=204)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Attempting to delete habit with ID: {habit_id} for user ID: {current_user.id}")

    db_habit = get_habit(db, habit_id=habit_id, user_id=current_user.id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return delete_habit_by_id(db, habit_id, current_user.id)



@router.patch("/habits/{habit_id}", response_model=Habit)
def update_habit_by_id(
    habit_id: int,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_habit = get_habit(db, habit_id=habit_id, user_id=current_user.id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit_data.name is not None:
        db_habit.name = habit_data.name

    db.commit()
    db.refresh(db_habit)
    return db_habit