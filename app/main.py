import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from starlette.middleware.sessions import SessionMiddleware

from app.auth import gerar_md5
from app.database import get_db
from app.models import (
    Aluno,
    Disciplina,
    Matricula,
    Professor,
    Usuario,
)
from app.schemas import (
    AlunoResposta,
    DiarioDisciplinaResposta,
    ProfessorResposta,
    RelatorioAlunoResposta,
)


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Sistema Escolar",
    description=(
        "API para gerenciamento de alunos, "
        "professores e disciplinas"
    ),
    version="1.0.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SECRET_KEY",
        "chave-secreta-temporaria",
    ),
    same_site="lax",
    https_only=False,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

BancoDep = Annotated[Session, Depends(get_db)]


# =====================================================
# ROTAS DO SISTEMA WEB
# =====================================================

@app.get(
    "/",
    include_in_schema=False,
)
def pagina_inicial(request: Request):
    if request.session.get("usuario_id"):
        return RedirectResponse(
            url="/sistema",
            status_code=303,
        )

    return RedirectResponse(
        url="/login",
        status_code=303,
    )


@app.get(
    "/login",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def exibir_login(request: Request):
    if request.session.get("usuario_id"):
        return RedirectResponse(
            url="/sistema",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "erro": None,
        },
    )


@app.post(
    "/login",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def realizar_login(
    request: Request,
    banco: BancoDep,
    usuario: Annotated[str, Form()],
    senha: Annotated[str, Form()],
):
    consulta = select(Usuario).where(
        Usuario.usuario == usuario
    )

    usuario_banco = banco.scalar(consulta)

    senha_md5 = gerar_md5(senha)

    if (
        usuario_banco is None
        or usuario_banco.senha_md5 != senha_md5
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "erro": "Usuário ou senha inválidos.",
            },
            status_code=401,
        )

    request.session["usuario_id"] = usuario_banco.id
    request.session["usuario_nome"] = usuario_banco.nome

    return RedirectResponse(
        url="/sistema",
        status_code=303,
    )


@app.get(
    "/sistema",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def exibir_sistema(request: Request):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="sistema.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
        },
    )


@app.post(
    "/logout",
    include_in_schema=False,
)
def realizar_logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303,
    )

@app.get(
    "/alunos",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def pagina_alunos(
    request: Request,
    banco: BancoDep,
):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    consulta = select(Aluno).order_by(Aluno.nome)

    alunos = banco.scalars(consulta).all()

    return templates.TemplateResponse(
        request=request,
        name="alunos.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
            "alunos": alunos,
        },
    )


@app.get(
    "/alunos",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def pagina_alunos(
    request: Request,
    banco: BancoDep,
):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    consulta = select(Aluno).order_by(Aluno.nome)

    alunos = banco.scalars(consulta).all()

    return templates.TemplateResponse(
        request=request,
        name="alunos.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
            "alunos": alunos,
        },
    )
@app.get(
    "/alunos/{aluno_id}/relatorio",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def pagina_relatorio_aluno(
    aluno_id: int,
    request: Request,
    banco: BancoDep,
):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    consulta = (
        select(Aluno)
        .options(
            selectinload(
                Aluno.matriculas
            ).selectinload(Matricula.disciplina)
        )
        .where(Aluno.id == aluno_id)
    )

    aluno = banco.scalar(consulta)

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado.",
        )

    matriculas_ordenadas = sorted(
        aluno.matriculas,
        key=lambda item: item.disciplina.nome,
    )

    return templates.TemplateResponse(
        request=request,
        name="relatorio_aluno.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
            "aluno": aluno,
            "matriculas": matriculas_ordenadas,
        },
    )

@app.get(
    "/professores",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def pagina_professores(
    request: Request,
    banco: BancoDep,
):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    consulta = (
        select(Professor)
        .options(
            selectinload(Professor.disciplinas)
        )
        .order_by(Professor.nome)
    )

    professores = banco.scalars(consulta).all()

    return templates.TemplateResponse(
        request=request,
        name="professores.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
            "professores": professores,
        },
    )

@app.get(
    "/disciplinas/diario",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def pagina_diario_disciplinas(
    request: Request,
    banco: BancoDep,
):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    consulta = (
        select(Disciplina)
        .options(
            selectinload(Disciplina.professor),
            selectinload(
                Disciplina.matriculas
            ).selectinload(Matricula.aluno),
        )
        .order_by(Disciplina.nome)
    )

    disciplinas = banco.scalars(consulta).all()

    for disciplina in disciplinas:
        disciplina.matriculas.sort(
            key=lambda matricula: matricula.aluno.nome
        )

    return templates.TemplateResponse(
        request=request,
        name="diario.html",
        context={
            "usuario_nome": request.session.get(
                "usuario_nome"
            ),
            "disciplinas": disciplinas,
        },
    )
# =====================================================
# ROTAS DA API
# =====================================================

@app.get(
    "/api/status",
    tags=["Sistema"],
)
def verificar_sistema():
    return {
        "mensagem": "Sistema escolar funcionando!",
        "documentacao": "/docs",
    }


@app.get(
    "/api/alunos",
    response_model=list[AlunoResposta],
    tags=["Alunos"],
)
def listar_alunos(banco: BancoDep):
    consulta = select(Aluno).order_by(Aluno.nome)

    return banco.scalars(consulta).all()


@app.get(
    "/api/professores",
    response_model=list[ProfessorResposta],
    tags=["Professores"],
)
def listar_professores(banco: BancoDep):
    consulta = select(Professor).order_by(
        Professor.nome
    )

    return banco.scalars(consulta).all()


@app.get(
    "/api/disciplinas/diario",
    response_model=list[DiarioDisciplinaResposta],
    tags=["Disciplinas"],
)
def emitir_diario_disciplinas(banco: BancoDep):
    consulta = (
        select(Disciplina)
        .options(
            selectinload(Disciplina.professor),
            selectinload(
                Disciplina.matriculas
            ).selectinload(Matricula.aluno),
        )
        .order_by(Disciplina.nome)
    )

    disciplinas = banco.scalars(consulta).all()

    relatorio = []

    for disciplina in disciplinas:
        alunos = []

        matriculas_ordenadas = sorted(
            disciplina.matriculas,
            key=lambda item: item.aluno.nome,
        )

        for matricula in matriculas_ordenadas:
            alunos.append(
                {
                    "aluno_id": matricula.aluno.id,
                    "aluno_nome": matricula.aluno.nome,
                    "nota1": float(matricula.nota1),
                    "nota2": float(matricula.nota2),
                    "nota3": float(matricula.nota3),
                    "nota4": float(matricula.nota4),
                    "media": matricula.media,
                    "resultado_final": (
                        matricula.resultado_final
                    ),
                }
            )

        relatorio.append(
            {
                "disciplina_id": disciplina.id,
                "disciplina_nome": disciplina.nome,
                "horario": disciplina.horario,
                "professor_nome": (
                    disciplina.professor.nome
                ),
                "alunos": alunos,
            }
        )

    return relatorio


@app.get(
    "/api/alunos/{aluno_id}/relatorio",
    response_model=RelatorioAlunoResposta,
    tags=["Alunos"],
)
def emitir_relatorio_aluno(
    aluno_id: int,
    banco: BancoDep,
):
    consulta = (
        select(Aluno)
        .options(
            selectinload(
                Aluno.matriculas
            ).selectinload(Matricula.disciplina)
        )
        .where(Aluno.id == aluno_id)
    )

    aluno = banco.scalar(consulta)

    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado.",
        )

    matriculas_ordenadas = sorted(
        aluno.matriculas,
        key=lambda item: item.disciplina.nome,
    )

    disciplinas = []

    for matricula in matriculas_ordenadas:
        disciplinas.append(
            {
                "disciplina_id": (
                    matricula.disciplina.id
                ),
                "disciplina_nome": (
                    matricula.disciplina.nome
                ),
                "horario": (
                    matricula.disciplina.horario
                ),
                "nota1": float(matricula.nota1),
                "nota2": float(matricula.nota2),
                "nota3": float(matricula.nota3),
                "nota4": float(matricula.nota4),
                "media": matricula.media,
                "resultado_final": (
                    matricula.resultado_final
                ),
            }
        )

    return {
        "aluno_id": aluno.id,
        "aluno_nome": aluno.nome,
        "total_disciplinas": len(disciplinas),
        "disciplinas": disciplinas,
    }