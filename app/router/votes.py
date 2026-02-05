from fastapi import APIRouter, status, HTTPException, Depends
from app.database import get_db
from app import models, schemas
from sqlalchemy.orm import Session
from app.router import oauth2

router = APIRouter(
    prefix= "/vote",
    tags=["Votes"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Votes, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id{vote.post_id} does not exist")
  vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)

  found_vote = vote_query.first()
  if(vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has already voted on post {vote.post_id}")

    new_vote = models.Votes(user_id=current_user.id, post_id = vote.post_id)
    db.add(new_vote)
    db.commit()
    return {"message": "successfully added vote"}
  
  else:
    if not found_vote:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"vote does not exist")
    
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted vote"}