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
def hello_world():
    search_query = request.args.get('search')
    filtered_list = filter_alunos(search_query)
    return render_template('index.html',
                           header ="Alunos",
                           lista=filtered_list)


@app.get("/alunos/<id>")
def aluno(id:int):

    for i in myList:
        if i.id == int(id):
            return i.nome

    return "O aluno nao existe"


@app.route("/add", methods=["POST"])
def add():
    nome = request.form['novoNome']
    turma = request.form['novaTurma']
    al = Alunos(nome, turma)

    myList.append(al)
    return redirect("/")


@app.route("/remove", methods=["POST"])
def remove():
    aluno_id = int(request.form['alunoId'])

    for aluno in myList:
        if aluno.id == aluno_id:
            myList.remove(aluno)
            return redirect("/")

@app.route("/procurar", methods=["POST"])
def filter_alunos(search_query):
    if not search_query:
        return myList
    else:
        search_query = search_query.lower()
        filtered_list = [aluno for aluno in myList if search_query in aluno.nome.lower()]
        return filtered_list

if __name__ == '__main__':
    app.run(debug=True)