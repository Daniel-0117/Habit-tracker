from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.schemas import User

router = APIRouter()

@router.get("/users/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/token-test", response_model=User)
def test_token(current_user: User = Depends(get_current_user)):
    return current_user


