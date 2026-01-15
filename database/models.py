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

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database.connection import Base

class Aluno(Base):
    __tablename__ = 'Aluno'

    id_aluno = Column(Integer, primary_key=True)
    matricula = Column(String(20), unique=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone_responsavel = Column(String(20), nullable=False)
    ano_letivo = Column(Integer)
    email = Column(String(100), unique=True)
    id_usuario = Column(
        Integer,
        ForeignKey('Usuario.id_usuario'),
        unique=True,
        nullable=False
    )


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

class Coordenador(Base):
    __tablename__ = 'Coordenador'
    __tablename__ = 'coordenador'

    id_coordenador = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=False)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)