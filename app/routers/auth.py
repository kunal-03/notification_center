from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import database
from ..models import models, schema
from ..utils import utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    """API to get the auth token that need to be passed for all the other api's"""
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentails")
    if not utils.veriy(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentails")
    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return{"access_token": access_token, "token_type": "bearer"}
