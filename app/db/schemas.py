from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime  



class HabitBase(BaseModel):
    """Base model for a habit"""
    name: str

class HabitCreate(HabitBase):
    """Used when creating a new habit"""
    pass

class Habit(HabitBase):
    """Habit returned from the database with owners info"""
    id: int
    owner_id: int  

    model_config: dict = {
        "from_attributes": True
    }


class UserBase(BaseModel):
    """Base model for a user"""
    email: str

class UserCreate(UserBase):
    """Used when creating a new user"""
    password: str

class User(UserBase):
    """A user with an ID and associated habits"""
    id: int
    habits: List[Habit] = []  

    model_config: dict = {
        "from_attributes": True
    }

class HabitUpdate(BaseModel):
    """Used when updating a habit"""
    name: Optional[str] = None

    model_config: dict = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    """Data extracted from the JWT token, often just the user's email"""
    email: Optional[str] = None

    model_config: dict = {
        "from_attributes": True
    }