from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.database.db_connection import engine, Base
from app.auth.auth_controller import router as auth_router
from app.users.users_controller import router as users_router
from app.posts.posts_controller import router as posts_router
from app.comments.comments_controller import router as comments_router
from app.social.follow_controller import router as social_router
from app.feed.feed_controller import router as feed_router

app = FastAPI(title="Social Media API", version="1.0.0")

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[WARN] Nu pot crea tabelele (DB off / config greșit): {e}")

@app.get("/")
def home():
    return {"message": "Platforma funcționează!", "docs": "/docs"}

# routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(social_router)
app.include_router(feed_router)
