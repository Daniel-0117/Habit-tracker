from fastapi import FastAPI
from app.api import auth, user, habits

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(habits.router, prefix="/habits", tags=["habits"])