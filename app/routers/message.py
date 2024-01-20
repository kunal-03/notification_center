from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from typing import List, Optional
from ..models import models,schema
from ..utils import oauth2


router = APIRouter(prefix='/message', tags=['Message'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def publish_message(message: schema.MessageCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    print(message.receivers)
    messages = []
    receivers = message.receivers
    for receiver in receivers:
        new_message = models.Message(sender=current_user.id, receiver=receiver ,**message.model_dump(exclude=["receivers"]))
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        messages.append(new_message)   
    return messages