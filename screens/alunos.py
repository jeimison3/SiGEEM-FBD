# ============================================================
# Arquivo: screens/alunos.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.connection import DatabaseConnection
from models.aluno import Aluno
from models.turma import Turma


class AlunosScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)

        self.create_widgets()
        self.carregar_dados()

    # =====================================================
    # INTERFACE
    # =====================================================
    def create_widgets(self):
        header = tk.Frame(self.frame, bg='#2196F3', height=60)
        header.pack(fill='x')

        tk.Label(
            header,
            text="Gerenciamento de Alunos",
            font=('Arial', 16, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(side='left', padx=20, pady=15)

        tk.Button(
            header,
            text="← Voltar",
            bg='#1976D2',
            fg='white',
            command=self.voltar,
            padx=15
        ).pack(side='right', padx=20)

        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Novo", width=12, command=self.novo).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", width=12, command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remover", width=12, command=self.remover).grid(row=0, column=2, padx=5)

        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'CPF', 'Data', 'Turma'),
            show='headings'
        )

        for col in ('ID', 'Nome', 'CPF', 'Data', 'Turma'):
            self.tree.heading(col, text=col)

        self.tree.column('ID', width=50)
        self.tree.column('Nome', width=200)
        self.tree.column('CPF', width=120)
        self.tree.column('Data', width=100)
        self.tree.column('Turma', width=150)

        self.tree.pack(fill='both', expand=True)

    # =====================================================
    # BANCO – LISTAR
    # =====================================================
    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        session = DatabaseConnection.get_session()

        try:
            alunos = session.query(Aluno).all()

            for aluno in alunos:
                turma_nome = aluno.turma.nome if aluno.turma else ""

                self.tree.insert('', 'end', values=(
                    aluno.id_aluno,
                    aluno.nome_completo,
                    aluno.cpf,
                    aluno.data_nascimento.strftime('%d/%m/%Y'),
                    turma_nome
                ))
        finally:
            session.close()

    # =====================================================
    # CRUD
    # =====================================================
    def novo(self):
        self.abrir_formulario()

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        valores = self.tree.item(selecionado[0])['values']

        dados = {
            'id': valores[0],
            'nome': valores[1],
            'cpf': valores[2],
            'data': valores[3],
            'turma': valores[4]
        }

        self.abrir_formulario(dados)

    def remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        valores = self.tree.item(selecionado[0])['values']
        aluno_id = valores[0]

        if not messagebox.askyesno("Confirmar", "Deseja remover este aluno?"):
            return

        session = DatabaseConnection.get_session()

        try:
            aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
            if aluno:
                session.delete(aluno)
                session.commit()
                self.carregar_dados()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", str(e))
        finally:
            session.close()

    # =====================================================
    # FORMULÁRIO
    # =====================================================
    def abrir_formulario(self, dados=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Aluno")
        dialog.geometry("400x400")
        dialog.grab_set()

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Nome Completo").pack(anchor='w')
        nome_entry = tk.Entry(frame)
        nome_entry.pack(fill='x')

        tk.Label(frame, text="CPF").pack(anchor='w', pady=(10, 0))
        cpf_entry = tk.Entry(frame)
        cpf_entry.pack(fill='x')

        tk.Label(frame, text="Data de Nascimento (dd/mm/aaaa)").pack(anchor='w', pady=(10, 0))
        data_entry = tk.Entry(frame)
        data_entry.pack(fill='x')

        tk.Label(frame, text="Turma").pack(anchor='w', pady=(10, 0))
        turma_combo = ttk.Combobox(frame, state='readonly')
        turma_combo.pack(fill='x')

        session = DatabaseConnection.get_session()
        turmas = session.query(Turma).all()
        session.close()

        turma_combo['values'] = [t.nome for t in turmas]

        if dados:
            nome_entry.insert(0, dados['nome'])
            cpf_entry.insert(0, dados['cpf'])
            data_entry.insert(0, dados['data'])
            turma_combo.set(dados['turma'])

        def salvar():
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()
            data_txt = data_entry.get().strip()
            turma_nome = turma_combo.get()

            if not nome or not cpf or not data_txt:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios")
                return

            try:
                data = datetime.strptime(data_txt, '%d/%m/%Y').date()
            except ValueError:
                messagebox.showerror("Erro", "Data inválida")
                return

            session = DatabaseConnection.get_session()

            try:
                turma = session.query(Turma).filter_by(nome=turma_nome).first()

                if dados:
                    aluno = session.query(Aluno).filter_by(id_aluno=dados['id']).first()
                else:
                    aluno = Aluno()

                aluno.nome_completo = nome
                aluno.cpf = cpf
                aluno.data_nascimento = data
                aluno.turma_id = turma.id_turma if turma else None

                session.add(aluno)
                session.commit()

                dialog.destroy()
                self.carregar_dados()

            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", str(e))
            finally:
                session.close()

        tk.Button(frame, text="Salvar", command=salvar).pack(pady=20)

    # =====================================================
    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
