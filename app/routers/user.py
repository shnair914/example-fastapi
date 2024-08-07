from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models
from ..utils import hash_password
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} was not found')
    return user.first()
