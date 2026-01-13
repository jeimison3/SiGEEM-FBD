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
    
    # Relacionamentos
    alunos = relationship("Aluno", back_populates="turma")
    aulas = relationship("Aula", back_populates="turma")

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14))
    data_nascimento = Column(Date)
    turma_id = Column(Integer, ForeignKey('turmas.id'))
    
    # Relacionamentos
    turma = relationship("Turma", back_populates="alunos")
    notas = relationship("Nota", back_populates="aluno")
    frequencias = relationship("Frequencia", back_populates="aluno")

class Professor(Base):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14))
    especialidade = Column(String(100))
    
    # Relacionamentos
    disciplinas = relationship("Disciplina", back_populates="professor")
    aulas = relationship("Aula", back_populates="professor")

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    carga_horaria = Column(Integer)
    professor_id = Column(Integer, ForeignKey('professores.id'))
    
    # Relacionamentos
    professor = relationship("Professor", back_populates="disciplinas")
    aulas = relationship("Aula", back_populates="disciplina")
    notas = relationship("Nota", back_populates="disciplina")

class Aula(Base):
    """Implementação do RF07 - Cadastro de Aula"""
    __tablename__ = 'aulas'
    
    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    turma_id = Column(Integer, ForeignKey('turmas.id'), nullable=False)
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'), nullable=False)
    data_aula = Column(Date, nullable=False)
    hora_inicio = Column(String(5), nullable=False) 
    hora_fim = Column(String(5), nullable=False)

    # Relacionamentos para busca de nomes e validação de regras de negócio
    professor = relationship("Professor", back_populates="aulas")
    turma = relationship("Turma", back_populates="aulas")
    disciplina = relationship("Disciplina", back_populates="aulas")

class Nota(Base):
    """Implementação do RF08 - Cadastro de Notas"""
    __tablename__ = 'notas'
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    nota = Column(Float)
    bimestre = Column(Integer)
    
    aluno = relationship("Aluno", back_populates="notas")
    disciplina = relationship("Disciplina", back_populates="notas")

class Frequencia(Base):
    """Implementação do RF09 - Cadastro de Frequência"""
    __tablename__ = 'frequencias'
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    data = Column(Date)
    presente = Column(Integer) # 1 para presente, 0 para ausente
    
    aluno = relationship("Aluno", back_populates="frequencias")