from pydantic import BaseModel
from typing import Dict, List

class Pessoa(BaseModel):
    nome: str
    idade: int
    email: str
    telefone: int

class Aluno(Pessoa):
    turma: str
    notas: Dict[str, float] = {}
    faltas: Dict[str, int] = {}

    def add_notas(self, ufcd: str, nota: float):
        self.notas[ufcd] = nota

    def add_faltas(self, ufcd: str, faltas: int):
        self.faltas[ufcd] = faltas

class Professor(Pessoa):
    ufcds: List[str] = []
    faltas: Dict[str, int] = {}
    horario: Dict[str, str] = {}

    def add_ufcd(self, ufcd: str):
        self.ufcds.append(ufcd)

    def add_faltas(self, ufcd: str, faltas: int):
        self.faltas[ufcd] = faltas

    def add_horario(self, dia: str, horas: str):
        self.horario[dia] = horas

class Turma(BaseModel):
    ident: str
    coord: str
    alunos: List[Aluno] = []
    horario: Dict[str, str] = {}
    ufcds: List[str] = []

    def add_aluno(self, aluno: Aluno):
        if isinstance(aluno, Aluno):
            self.alunos.append(aluno)
        else:
            return f"O aluno {aluno} não está inscrito nesta escola"

    def add_horario(self, dia: str, horas: str):
        self.horario[dia] = horas

    def add_ufcd(self, ufcd: str):
        self.ufcds.append(ufcd)

    def add_falta(self, aluno: Aluno, ufcd: str, faltas: int):
        if ufcd in self.ufcds:
            if aluno in self.alunos:
                aluno.add_faltas(ufcd, faltas)
            else:
                return f"O aluno {aluno} não pertence a esta turma"
        else:
            return f"A UFCD {ufcd} não pertence ao plano de aulas desta turma"


class Ufcd(BaseModel):
    num: int
    professor: str
    turma: str


