from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nome = Column(String(100))

class Turma(Base):
    __tablename__ = 'turmas'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    ano = Column(Integer)
    turno = Column(String(20))

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
    __tablename__ = 'Nota'
    
    id_turma = Column(Integer, ForeignKey('turma.id_turma'), primary_key=True)
    id_aluno = Column(Integer, ForeignKey('aluno.id_aluno'), primary_key=True)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id_disciplina'), primary_key=True)
    id_professor = Column(Integer, ForeignKey('professor.id_professor'), primary_key=True)
    id_avaliacao = Column(Integer, ForeignKey('avaliacao.id_avaliacao'), primary_key=True)
    nota = Column(Float)
    peso = Column(Float)
    
class Avaliacao(Base):
    __tablename__ = 'Avaliacao'
    
    id_avaliacao = Column(Integer, primary_key=True)
    nome_avaliacao = Column(String(100))
    data_avaliacao = Column(Date)
    quanto_vale = Column(Float)
    peso = Column(Float)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id_disciplina'), nullable=False)
    id_turma = Column(Integer, ForeignKey('turma.id_turma'), nullable=False)
    id_professor = Column(Integer, ForeignKey('professor.id_professor'), nullable=False)