import random

from flask import Flask, render_template, redirect, request

app = Flask(__name__)


class Alunos:
    def __init__(self, nome, turma):
        self.id = random.randint(0, 1000000)
        self.nome = nome
        self.turma = turma

    def __eq__(self, other):
        return self.id == id


myList = [Alunos("Joao", "PI"),
          Alunos("Carlos", "PI"),
          Alunos("Luis", "PI")]

@app.route('/')
def hello_world():  # put application's code here

    return render_template('index.html',
                           header="Ola Mundo",
                           lista=myList)


@app.get("/alunos/<id>")
def aluno(id: int):

    for i in myList:
        if i == int(id):
            return i.nome

    return "O aluno na existe"


@app.route("/add", methods=["POST"])
def add():
    nome = request.form['novoNome']
    turma =request.form['novaTurma']
    al = Alunos(nome, turma)

    myList.append(al)
    return redirect("/")





if __name__ == '__main__':
    app.run(debug=True)