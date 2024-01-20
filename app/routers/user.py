from fastapi import APIRouter, Depends, HTTPException, status
from ..models import models, schema
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..utils import utils
from typing import Optional, List
from ..utils import oauth2



router = APIRouter(prefix='/user', tags=['User'])


@router.post("/", response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """API to create a new user, once created the credentials can be used to get the auth token which is required to perform any other operation."""
    user.password = utils.hash(user.password)
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=List[schema.UserOut])
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, email_search: Optional[str] = ""):
    """API to get all the user email and user ID which will be used to publisjh messages to other users"""
    user = db.query(models.Users).filter(models.Users.email.contains(email_search)).limit(limit).offset(offset).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return user


