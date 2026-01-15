from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from database.connection import Base
from typing import List

prof_habilitado = Table(
    'prof_habilitado', Base.metadata,
    Column('id_professor', Integer, ForeignKey('professor.id_professor'), primary_key=True),
    Column('id_disciplina', Integer, ForeignKey('disciplina.id_disciplina'), primary_key=True)
)
class Turma(Base):
    __tablename__ = 'turma'
    id_turma = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    sala = Column(String(10))
    notas: Mapped[List["Nota"]] = relationship(back_populates="turma")

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    cpf = Column(String(14), unique=True, nullable=False)
    senha = Column(String(128), nullable=False)
    aluno: Mapped["Aluno"] = relationship(back_populates="usuario")
    professor: Mapped["Professor"] = relationship(back_populates="usuario")
    coordenador: Mapped["Coordenador"] = relationship(back_populates="usuario")


from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database.connection import Base

class Aluno(Base):
    __tablename__ = 'aluno'

    id_aluno = Column(Integer, primary_key=True)
    matricula = Column(String(20), unique=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone_responsavel = Column(String(20), nullable=False)
    ano_letivo = Column(Integer)
    email = Column(String(100), unique=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[id_usuario], back_populates="aluno")
    notas: Mapped[List["Nota"]] = relationship(back_populates="aluno")


class Professor(Base):
    __tablename__ = 'professor'

    id_professor = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    area_formacao = Column(String(100), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)

    usuario: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[id_usuario], back_populates="professor")
    # Versão Correta:
    disciplinas_habilitadas: Mapped[List["Disciplina"]] = relationship("Disciplina", secondary=prof_habilitado, back_populates="professores")
    notas: Mapped[List["Nota"]] = relationship(back_populates="professor")

class Disciplina(Base):
    __tablename__ = 'disciplina'

    id_disciplina = Column(Integer, primary_key=True)
    nome_disciplina = Column(String(100))
    carga_horaria = Column(Integer, nullable=False)
    obrigatoriedade = Column(Boolean, default=True)
    ativa = Column(Boolean, default=True)
    prerequisito = Column(Integer, ForeignKey('disciplina.id_disciplina'))

    professores: Mapped[List["Professor"]] = relationship(
        "Professor", 
        secondary=prof_habilitado, 
        back_populates="disciplinas_habilitadas",
        overlaps="disciplinas_habilitadas"
    )
    notas: Mapped[List["Nota"]] = relationship(back_populates="disciplina")

class Nota(Base):
    __tablename__ = 'nota'
    
    id_turma = Column(Integer, ForeignKey('turma.id_turma'), primary_key=True)
    id_aluno = Column(Integer, ForeignKey('aluno.id_aluno'), primary_key=True)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id_disciplina'), primary_key=True)
    id_professor = Column(Integer, ForeignKey('professor.id_professor'), primary_key=True)
    id_avaliacao = Column(Integer, ForeignKey('avaliacao.id_avaliacao'), primary_key=True)
    nota = Column(Float)
    peso = Column(Float)
    turma: Mapped["Turma"] = relationship("Turma", foreign_keys=[id_turma], back_populates="notas")
    aluno: Mapped["Aluno"] = relationship("Aluno", foreign_keys=[id_aluno], back_populates="notas")
    disciplina: Mapped["Disciplina"] = relationship("Disciplina", foreign_keys=[id_disciplina], back_populates="notas")
    professor: Mapped["Professor"] = relationship("Professor", foreign_keys=[id_professor], back_populates="notas")
    avaliacao: Mapped["Avaliacao"] = relationship("Avaliacao", foreign_keys=[id_avaliacao], back_populates="notas")
    
class Avaliacao(Base):
    __tablename__ = 'avaliacao'
    
    id_avaliacao = Column(Integer, primary_key=True)
    nome_avaliacao = Column(String(100))
    data_aplicacao = Column(Date)
    quanto_vale = Column(Float)
    peso = Column(Float)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id_disciplina'), nullable=False)
    id_turma = Column(Integer, ForeignKey('turma.id_turma'), nullable=False)
    id_professor = Column(Integer, ForeignKey('professor.id_professor'), nullable=False)
    notas: Mapped[List["Nota"]] = relationship(back_populates="avaliacao")

class Coordenador(Base):
    __tablename__ = 'coordenador'

    id_coordenador = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[id_usuario], back_populates="coordenador")