import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from database.connection import DatabaseConnection, Base
from database.models import Usuario, Turma, Aluno, Professor, Disciplina, Nota, Frequencia

def criar_banco():
    print("--- Inicializando Banco de Dados SiGEEM ---")
    try:
        engine = DatabaseConnection.get_engine()
        with engine.connect() as connection:
            print("Conexao estabelecida. Verificando tabelas...")
            Base.metadata.create_all(bind=engine)
            print("\n[SUCESSO]: Tabelas sincronizadas!")
            
    except Exception as e:
        print("\n[ERRO NO POSTGRESQL]:")
        print(repr(e)) 

if __name__ == "__main__":
    criar_banco()