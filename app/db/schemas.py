from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime  



class HabitBase(BaseModel):
    name: str

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    owner_id: int  

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    habits: List[Habit] = []  

    class Config:
        orm_mode = True

class HabitUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True