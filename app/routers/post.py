from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models
from ..utils import hash_password
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oath2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db), user_id: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # post_dic = post.dict()
    # post_dic['id'] = randrange(0, 10000000)
    
    # my_posts.append(post_dic)

    # This is done using an ORM
    new_post = models.Post(user_email=user_id.email,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # This was done using a database connector
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    return new_post

@router.get("/{id}", response_model=schemas.Post)
# The id field is a path parameter and is almost always a string
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # data base connector code
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    #ORM sqlalchemy code
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
   
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # ORM code
    post = db.query(models.Post).filter(models.Post.id == id)
    post1 = post.first()
    if post1.user_email != user_id.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# We can use pydantic to create a schema, which will contain the data we want the frontend user to send to the api server
# to retrieve data
@router.put("/{id}", response_model=schemas.Post)
def edit_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()

    if post1.user_email != user_id.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')

   
    if not post1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()