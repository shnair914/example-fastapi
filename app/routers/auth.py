from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import UserLogin, Token
from ..utils import verify
from ..oath2 import create_access_token

router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    access_token = create_access_token(data={'user_id' : user.id, 'email': user.email})
    return {"access_token": access_token, 'token_type': 'bearer'}


