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
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/hello/{name}/{ano}")
async def say_hello(name: str, ano: int):
    msg = {"message": f"Hello {name}", "ano": ano}
    for i in range(10):
        msg[f"Mensagem {i}"] = f"conteudo da msg {i}: {i}"
    return msg
