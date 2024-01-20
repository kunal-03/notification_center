from fastapi import APIRouter, Depends, HTTPException, status
from ..models import models, schema
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..utils import utils




router = APIRouter(prefix='/user', tags=['User'])


@router.post("/", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return user


