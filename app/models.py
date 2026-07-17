from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    rua: Mapped[str] = mapped_column(String(150), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)

    matriculas: Mapped[list[Matricula]] = relationship(
        back_populates="aluno"
    )


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    rua: Mapped[str] = mapped_column(String(150), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)

    disciplinas: Mapped[list[Disciplina]] = relationship(
        back_populates="professor"
    )


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    horario: Mapped[str] = mapped_column(String(100), nullable=False)

    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professores.id"),
        nullable=False,
    )

    professor: Mapped[Professor] = relationship(
        back_populates="disciplinas"
    )

    matriculas: Mapped[list[Matricula]] = relationship(
        back_populates="disciplina"
    )


class Matricula(Base):
    __tablename__ = "matriculas"

    __table_args__ = (
        UniqueConstraint(
            "aluno_id",
            "disciplina_id",
            name="aluno_disciplina_unico",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    aluno_id: Mapped[int] = mapped_column(
        ForeignKey("alunos.id"),
        nullable=False,
    )

    disciplina_id: Mapped[int] = mapped_column(
        ForeignKey("disciplinas.id"),
        nullable=False,
    )

    nota1: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
        default=0,
    )

    nota2: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
        default=0,
    )

    nota3: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
        default=0,
    )

    nota4: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
        default=0,
    )

    aluno: Mapped[Aluno] = relationship(
        back_populates="matriculas"
    )

    disciplina: Mapped[Disciplina] = relationship(
        back_populates="matriculas"
    )

    @property
    def media(self) -> float:
        soma = self.nota1 + self.nota2 + self.nota3 + self.nota4
        return round(float(soma / 4), 2)

    @property
    def resultado_final(self) -> str:
        if self.media >= 6:
            return "APROVADO"

        return "REPROVADO"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    usuario: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    senha_md5: Mapped[str] = mapped_column(String(32), nullable=False)