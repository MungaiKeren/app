from fastapi import FastAPI
from post import Post
from database import engine
from router import posts

app = FastAPI()

Post.metadata.create_all(bind=engine)

app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}