from pydantic import BaseModel, ConfigDict


class AlunoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    telefone: str


class ProfessorResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    telefone: str


class AlunoDiarioResposta(BaseModel):
    aluno_id: int
    aluno_nome: str
    nota1: float
    nota2: float
    nota3: float
    nota4: float
    media: float
    resultado_final: str


class DiarioDisciplinaResposta(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    horario: str
    professor_nome: str
    alunos: list[AlunoDiarioResposta]


class DisciplinaAlunoResposta(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    horario: str
    nota1: float
    nota2: float
    nota3: float
    nota4: float
    media: float
    resultado_final: str


class RelatorioAlunoResposta(BaseModel):
    aluno_id: int
    aluno_nome: str
    total_disciplinas: int
    disciplinas: list[DisciplinaAlunoResposta]