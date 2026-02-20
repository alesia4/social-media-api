"""
Seed script: adaugă câțiva users + posts pentru test rapid.

Rulare:
  python -m scripts.seed
"""
import random
from sqlalchemy.orm import Session

from app.database.db_connection import SessionLocal, engine, Base
from app.database.models import User, Post
from app.auth.auth_service import hash_password

Base.metadata.create_all(bind=engine)


def main():
    db: Session = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("DB already has users. Skip seeding.")
            return

        users = []
        for i in range(1, 6):
            u = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password_hash=hash_password("password123"),
                bio=f"Sunt user{i}",
            )
            db.add(u)
            users.append(u)
        db.commit()
        for u in users:
            db.refresh(u)

        posts = []
        for i in range(1, 11):
            u = random.choice(users)
            p = Post(user_id=u.id, content=f"Postarea #{i} de la {u.username}")
            db.add(p)
            posts.append(p)
        db.commit()

        print("Seed done: 5 users, 10 posts.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
