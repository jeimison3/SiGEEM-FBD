from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Turma(Base):
    __tablename__ = 'turma'
    id_turma = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sala = Column(String(10))

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turma_id = Column(Integer, ForeignKey('turma.id_turma'), nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nome = Column(String(100))


class Aluno(Base):
    __tablename__ = 'alunos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14))
    data_nascimento = Column(Date)
    turma_id = Column(Integer, ForeignKey('turmas.id'))

class Professor(Base):
    __tablename__ = 'professores'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14))
    especialidade = Column(String(100))

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    carga_horaria = Column(Integer)
    professor_id = Column(Integer, ForeignKey('professores.id'))

class Nota(Base):
    __tablename__ = 'notas'
    
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    nota = Column(Float)
    bimestre = Column(Integer)

class Frequencia(Base):
    __tablename__ = 'frequencias'
    
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    data = Column(Date)
    presente = Column(Integer)  # 1 para presente, 0 para ausente

