from app.db.database import SessionLocal
from app.db.models import User, Habit
from app.core.security import get_pwd_hashed

db = SessionLocal()

seed_data = [
    {
        "email": "Animelover@example.com",
        "password": "Tibia0987",
        "habits": ["Eat Ramen", "Watch Anime", "Maybe Workout"]
    },
    {
        "email": "Doughguy@example.com",
        "password": "Cake7767",
        "habits": ["Practice new recipe", "Workout", "Drink water"]
    },
    {
        "email": "Primarch@example.com",
        "password": "Sanguiny32",
        "habits": ["Read a book", "Discuss planetary operations", "Oversee combat logs"]
    }
]

users_to_add = []

for data in seed_data:
    user = User(
        email=data["email"],
        hashed_password=get_pwd_hashed(data["password"])
    )
    user.habits = [Habit(name=habit_name) for habit_name in data["habits"]]
    users_to_add.append(user)

# Add all users (with their habits)
db.add_all(users_to_add)
db.commit()

# Refresh to load IDs
for user in users_to_add:
    db.refresh(user)

print("Seeded all users and their habits")