from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.schemas import User
from app.api.dependencies import get_db
from app.db.crud import delete_user

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/token-test", response_model=User)
def test_token(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/me", status_code=204)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = delete_user(db, current_user.id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return