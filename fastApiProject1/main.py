from fastapi import FastAPI
from classe import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/post/{id}")
async def rootTeste(id: int):
    posts = ListaPost[id - 1]
    return {"id": posts.id, "title": f"{posts.title}", "body": f"{posts.body}", "userId": posts.userId}

@app.get("/posts/all")
async def say_hello():
    msg = []
    for p in ListaPost:
        msg.append({"id": p.id, "title": f"{p.title}", "body": f"{p.body}", "userId": p.userId})

    return msg


@app.get("/users/{userid}/albums")
async def say_hello(userid: int):
    msg = []
    user_exists = False

    for p in ListaPost:
        if p.userId == userid:
            msg.append({"userId": p.userId, "id": p.id, "title": f"{p.title}"})
            user_exists = True

    if not user_exists:
        return "Esse user não existe"

    return msg
