from fastapi import FastAPI
from Pessoa import ListaPessoas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/teste")
async def root():
    return {"message": "Hello World teste"}


@app.get("/hello/{name}")
async def say_hello(nome: str):
    return {"message": f"Hello {nome}"}
