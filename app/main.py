from fastapi import FastAPI
from .models import models
from .routers import user, auth, message
from .db.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(message.router)