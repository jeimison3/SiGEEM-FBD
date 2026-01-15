from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.connection import Base

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

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turma_id = Column(Integer, ForeignKey('turma.id_turma'), nullable=False)

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id_usuario = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nome = Column(String(100))


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
    __tablename__ = 'professor'

    id_professor = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    area_formacao = Column(String(100), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True, nullable=False)

    usuario = relationship("Usuario")
    # Versão Correta:
    disciplinas_habilitadas = relationship("Disciplina", secondary=prof_habilitado, back_populates="professores")

class Disciplina(Base):
    __tablename__ = 'disciplina'

    id_disciplina = Column(Integer, primary_key=True)
    nome_disciplina = Column(String(100))
    carga_horaria = Column(Integer, nullable=False)
    obrigatoriedade = Column(Boolean, default=True)
    ativa = Column(Boolean, default=True)
    prerequisito = Column(Integer, ForeignKey('disciplina.id_disciplina'))

    professores = relationship(
    "Professor", 
    secondary=prof_habilitado, 
    back_populates="disciplinas_habilitadas",
    overlaps="disciplinas_habilitadas"
)

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
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    data = Column(Date)
    presente = Column(Integer)  # 1 para presente, 0 para ausente

class Coordenador(Base):
    __tablename__ = 'coordenador'

    id_coordenador = Column(Integer, primary_key=True)
    nome_completo = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
