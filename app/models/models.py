from ..db.database import Base
from sqlalchemy import ForeignKey, Integer, String, Boolean, Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__  = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, index=True)
    receiver = Column(Integer, index=True)
    message_content = Column(String)
    context = Column(String)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    seen = Column(Boolean, server_default=False)
    deleted = Column(Boolean, server_default=False)
    archived = Column(Boolean, server_default=False)