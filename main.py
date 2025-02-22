from fastapi import FastAPI
from post import Post
from database import engine
from router import posts, users, auth
from user import User

app = FastAPI()

Post.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}