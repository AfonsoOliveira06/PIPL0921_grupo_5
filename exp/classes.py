class Ser_vivo:
    def respirar(self):
        print("a respirar")

class Pessoa(Ser_vivo):
    def __init__(self, nome: str, idade:int, email: str):
        self.nome = nome
        self.idade = idade
        self.email = email

    def __str__(self):
        return f"Pessoa(nome: {self.nome}, idade: {self.idade}, email: {self.email})"
class Aluno(Pessoa, Ser_vivo):
    def __init__(self, nome: str, idade:int, email: str, turma: str):
        super().__init__(nome, idade, email)
        self.turma = turma

    def __str__(self):
        return f"{super().__str__()}, turma: {self.turma}"
