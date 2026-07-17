from sqlalchemy import func, select

from app.database import SessionLocal
from app.models import Aluno, Disciplina, Matricula, Professor, Usuario


def testar_modelos():
    banco = SessionLocal()

    try:
        quantidade_alunos = banco.scalar(
            select(func.count()).select_from(Aluno)
        )

        quantidade_professores = banco.scalar(
            select(func.count()).select_from(Professor)
        )

        quantidade_disciplinas = banco.scalar(
            select(func.count()).select_from(Disciplina)
        )

        quantidade_matriculas = banco.scalar(
            select(func.count()).select_from(Matricula)
        )

        quantidade_usuarios = banco.scalar(
            select(func.count()).select_from(Usuario)
        )

        print("Modelos conectados corretamente!")
        print(f"Alunos: {quantidade_alunos}")
        print(f"Professores: {quantidade_professores}")
        print(f"Disciplinas: {quantidade_disciplinas}")
        print(f"Matrículas: {quantidade_matriculas}")
        print(f"Usuários: {quantidade_usuarios}")

        print("\nAlunos cadastrados:")

        consulta = select(Aluno).order_by(Aluno.nome)
        alunos = banco.scalars(consulta).all()

        for aluno in alunos:
            print(f"- {aluno.id}: {aluno.nome}")

    except Exception as erro:
        print("Erro ao testar os modelos.")
        print(erro)

    finally:
        banco.close()


if __name__ == "__main__":
    testar_modelos()