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
    receivers = message.receivers
    for receiver in receivers:
        receiver_exist = db.query(models.Users).filter(models.Users.id==receiver).first()
        if not receiver_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Receiver with id# {receiver} not found.")
        new_message = models.Message(sender=current_user.id, receiver=receiver ,**message.model_dump(exclude=["receivers"]))
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
    return {"message": "Messages published successfully"}

@router.get('/', response_model=List[schema.MessageResponse])
def get_Messages(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = "" ):
    messages = db.query(models.Message).filter(models.Message.message_content.contains(search)).limit(limit).offset(offset).all()
    return messages

@router.put('/{message_id}', status_code=status.HTTP_201_CREATED, response_model=schema.MessageResponse)
def mark_message(message_id: int, action: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    allowed_actions = ["seen", "deleted", "archived"]
    if action not in allowed_actions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action, only ['seen', 'deleted', 'archived'] actions are allowed.")
    message_query = db.query(models.Message).filter(models.Message.id==message_id)
    message = message_query.first()
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with  id# {id} does not exist")
    if message.receiver != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    if not getattr(message, action):
        setattr(message, action, True)
        db.commit()
        db.refresh(message)
        return message
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Message already marked as {action}")