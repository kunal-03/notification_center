from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.db.database import get_db, Base
from app.utils.oauth2 import create_access_token
from app.models import models

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/notificaton_center_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "kunal123@gmail.com",
                 "password": "password123"}
    res = client.post("/user/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "kunal@gmail.com",
                 "password": "password123"}
    res = client.post("/user/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


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
def test_messages(test_user, session, test_user2):
    messages_data = [{
        "message_content": "first message",
        "context": "first context",
        "sender": test_user['id'],
        "receiver": test_user2['id']

    }, {
        "message_content": "2nd message",
        "context": "2nd context",
        "sender": test_user['id'],
        "receiver": test_user2['id']
    },
        {
        "message_content": "3rd message",
        "context": "3rd context",
        "sender": test_user2['id'],
        "receiver": test_user['id']
    }, {
        "message_content": "4rd message",
        "context": "4rd context",
        "sender": test_user2['id'],
        "receiver": test_user['id']
    }]

    def create_message_model(message):
        return models.Message(**message)

    message_map = map(create_message_model, messages_data)
    messages = list(message_map)

    session.add_all(messages)
    session.commit()

    messages = session.query(models.Message).all()
    return messages