from fastapi import FastAPI
from Classes import  Pessoa, Professor, Aluno, Turma, Ufcd
import sqlite3

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/hello/{professor}")
async def dados_prof(name: str, idade: int, email: str, tel: int):
    return {"message": f"Hello {name}"}


@app.get("/hello/{turma}")
async def dados_prof(id: str, quant: int, dt: str):
    return {"message": f"Hello {id}"}


@app.post("/addAluno")
async def add_aluno(al: Aluno):
    conn = sqlite3.connect("escola_db.sqlite")
    conn.execute(f"""
        insert into Aluno ("nome", "idade", "turma", "email", "telefone") 
                    values ("{al.nome}", {al.idade}, "{al.turma}", "{al.email}", "{al.telefone}")
    """)

    conn.commit()

    conn.close()


@app.post("/addProfessor")
async def add_professor(pr: Professor):
    conn = sqlite3.connect("escola_db.sqlite")
    conn.execute(f"""
            insert into Professor ("nome", "idade", "email", "telefone") 
                        values ("{pr.nome}", {pr.idade}, "{pr.email}", "{pr.telefone}")
        """)

    conn.commit()

    conn.close()

@app.post("/addTurma")
async def add_turma(tu: Turma):
    conn = sqlite3.connect("escola_db.sqlite")
    conn.execute(f"""
            insert into Turma ("ident", "coord") 
                        values ("{tu.ident}", "{tu.coord}")
        """)

    conn.commit()

    conn.close()

@app.post("/addUfcd")
async def add_ufcd(uf: Ufcd):
    conn = sqlite3.connect("escola_db.sqlite")
    conn.execute(f"""
            insert into ufcds ("num", "professor", "turma") 
                        values ({uf.num}, "{uf.professor}", "{uf.turma}")
        """)

    conn.commit()

    conn.close()