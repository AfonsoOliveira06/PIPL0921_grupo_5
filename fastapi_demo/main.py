from fastapi import FastAPI
from pessoas import ListaPessoas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/teste")
async def rootteste():
    p = ListaPessoas[0]
    return {"nome": f"{p.nome}", "idade": {p.idade}}

@app.get("/Listap")
async def rootteste():
    msg = []
    for i in ListaPessoas:
        msg.append({"nome": f"{i.nome}", "idade": {i.idade}})
    return msg

@app.get("/hello/{name}/{ano}")
async def say_hello(name: str, ano:int):
    msg = {"message": f"Hello {name}", "ano": ano}
    for i in range(10):
        msg[f"Mensagem {i}"] = f"conteudo da msg {i}: {i}"
    return msg 