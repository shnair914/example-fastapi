from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from app.oath2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 

# Session starts when you want to send a query to a database. Once you are finished the session will close out. 





'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='gopal1995', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print("Connecting to database failed")
        print(error)
        time.sleep(3)
'''
@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db    
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "srinair@yahoo.com",
                 "password": "gopal1995"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user
# def test_root(client, session):
#     res = client.get("/")
#     assert res.json().get('message') == 'hello world'
#     assert res.status_code == 200

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
        },
        {
            "title": "second title",
            "content": "second content"
        }
    ]

    # def create_post_model(post):
    #     return models.Post(**post)

    # post_map = map(create_post_model, posts_data)
    # posts = list(post_map)
    # session.add_all(models.Post(title='first title', content='first content', owner='User1'), models.Post(title='second title', content='second content', owner='user2'))
   

    # session.commit() 
    # session.query(models.Post).all()

    # return posts 