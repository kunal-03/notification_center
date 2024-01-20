from fastapi import FastAPI
from .models import models
from .routers import user
from .db.database import engine
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)