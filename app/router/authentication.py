from fastapi import APIRouter, status, HTTPException, Depends
from app.database import get_db
from app import models, schemas
import app.utils as utils
from sqlalchemy.orm import Session
from app.router import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
router = APIRouter(
    tags=["Authentication"]
)
# we will check user password with stored hash password if true then only give token (login the user)
# now because we used oauth2password request form we need to pass username from form of postman
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# it only returns following fiels so we cant access email if sent 
# {
#   'username':'emailvalue',
#   'passwrod'
# }
  user =db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
  
  is_verify = utils.verify(user_credentials.password, user.password)

  if not is_verify:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
  
  #create jwt token
  #return token
  access_token = oauth2.create_access_token(data ={"user_id": user.id})
  return {"access_token":  access_token, "token_type": "bearer"}
  
  