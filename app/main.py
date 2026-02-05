from app.router import post, user, authentication, votes
from fastapi import FastAPI
from app import models
from app.database import engine
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
# we have alembic setup so no need to add below line
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins domain , or specify ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "hello world"}