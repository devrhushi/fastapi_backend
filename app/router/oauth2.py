from jose import JWTError, jwt
from datetime import datetime, timedelta
import app.schemas as schemas 
from fastapi import Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.database  import get_db
from sqlalchemy.orm import Session
from app import models
from app.config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# three piece of info for token
#SECRET_KEY
#Alogrithm sh256
#Expiration time without this user logged in forver lol jk
# give random string long
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

# have to pass our info that we use for token creation
def create_access_token(data: dict):
  to_encode = data.copy() # dont want to accidently change original object so copying into variable so it will be new rather than reference same
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode.update({"exp": expire})# added extra property
  encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
  
  return encoded_jwt


def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    id = payload.get("user_id")

    if id is None:
      raise credentials_exception

    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credentials_exception
  return token_data
  
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f'could not validate credentials', headers={'www-Authenticate': 'Bearer'})

  token = verify_access_token(token, credentials_exception)
  user = db.query(models.Users).filter(models.Users.id == token.id).first()
  return user
