from sqlalchemy import (
    Column, Integer, String, Date, Float,
    Boolean, ForeignKey, Table
)
from sqlalchemy.orm import relationship, Mapped
from typing import List
from database.connection import Base


# ============================================================
# TABELA ASSOCIATIVA PROFESSOR ↔ DISCIPLINA
# ============================================================
prof_habilitado = Table(
    'Prof_Habilitado',
    Base.metadata,
    Column('id_professor', Integer, ForeignKey('Professor.id_professor'), primary_key=True),
    Column('id_disciplina', Integer, ForeignKey('Disciplina.id_disciplina'), primary_key=True)
)


# ============================================================
# USUÁRIO
# ============================================================
class Usuario(Base):
    __tablename__ = 'Usuario'

    id_usuario = Column(Integer, primary_key=True)
    cpf = Column(String(14), unique=True, nullable=False)
    senha = Column(String(128), nullable=False)


# ============================================================
# ALUNO
# ============================================================
class Aluno(Base):
    __tablename__ = 'Aluno'

    id_aluno = Column(Integer, primary_key=True)
    matricula = Column(String(20), unique=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone_responsavel = Column(String(20), nullable=False)
    ano_letivo = Column(Integer)
    email = Column(String(100), unique=True)

    id_usuario = Column(Integer, ForeignKey('Usuario.id_usuario'), unique=True, nullable=False)
    usuario = relationship("Usuario")


# ============================================================
# PROFESSOR
# ============================================================
class Professor(Base):
    __tablename__ = 'Professor'

    id_professor = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    area_formacao = Column(String(100), nullable=False)

    id_usuario = Column(Integer, ForeignKey('Usuario.id_usuario'), unique=True, nullable=False)
    usuario = relationship("Usuario")

    disciplinas: Mapped[List["Disciplina"]] = relationship(
        "Disciplina",
        secondary=prof_habilitado,
        back_populates="professores"
    )


# ============================================================
# COORDENADOR
# ============================================================
class Coordenador(Base):
    __tablename__ = 'Coordenador'

    id_coordenador = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    id_usuario = Column(Integer, ForeignKey('Usuario.id_usuario'), unique=True, nullable=False)
    usuario = relationship("Usuario")


# ============================================================
# DISCIPLINA
# ============================================================
class Disciplina(Base):
    __tablename__ = 'Disciplina'

    id_disciplina = Column(Integer, primary_key=True)
    nome_disciplina = Column(String(100), nullable=False)
    carga_horaria = Column(Integer, nullable=False)

    professores: Mapped[List["Professor"]] = relationship(
        "Professor",
        secondary=prof_habilitado,
        back_populates="disciplinas"
    )


# ============================================================
# TURMA
# ============================================================
class Turma(Base):
    __tablename__ = 'Turma'

    id_turma = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sala = Column(String(10))


# ============================================================
# AVALIAÇÃO
# ============================================================
class Avaliacao(Base):
    __tablename__ = 'Avaliacao'

    id_avaliacao = Column(Integer, primary_key=True)
    nome_avaliacao = Column(String(100))
    data_aplicacao = Column(Date)
    quanto_vale = Column(Float)
    peso = Column(Float)

    id_disciplina = Column(Integer, ForeignKey('Disciplina.id_disciplina'), nullable=False)
    id_turma = Column(Integer, ForeignKey('Turma.id_turma'), nullable=False)
    id_professor = Column(Integer, ForeignKey('Professor.id_professor'), nullable=False)


# ============================================================
# NOTA
# ============================================================
class Nota(Base):
    __tablename__ = 'Nota'

    id_turma = Column(Integer, ForeignKey('Turma.id_turma'), primary_key=True)
    id_aluno = Column(Integer, ForeignKey('Aluno.id_aluno'), primary_key=True)
    id_disciplina = Column(Integer, ForeignKey('Disciplina.id_disciplina'), primary_key=True)
    id_professor = Column(Integer, ForeignKey('Professor.id_professor'), primary_key=True)
    id_avaliacao = Column(Integer, ForeignKey('Avaliacao.id_avaliacao'), primary_key=True)

    nota = Column(Float)
    peso = Column(Float)
