import jwt
from jwt import InvalidTokenError
from typing import Annotated, Union
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from . import schemas
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#Will need a secret key
#Need to provide algorithm -> HS256
#Expiration time of token is also needed

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_TIME = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        email = payload.get("email")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, email=email) 
    except InvalidTokenError:
        # print(e)
    
        raise credentials_exception
 
    return token_data

def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token=token, credentials_exception=credentials_exception)


