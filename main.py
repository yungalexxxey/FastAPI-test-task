from fastapi import FastAPI
import uvicorn
from router import users, course
from auth import authentication
from db import models
from db.database import engine

app = FastAPI()

app.include_router(users.router)
app.include_router(course.router)
app.include_router(authentication.router)
models.Base.metadata.create_all(engine)




if __name__ == '__main__':
    uvicorn.run(app)



