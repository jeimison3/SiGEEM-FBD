# ============================================================
# Arquivo: screens/coordenadores.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database.connection import DatabaseConnection
from database.models import Coordenador, Usuario


class CoordenadoresScreen:
    def __init__(self, root, username, extra):
        self.root = root
        self.username = username
        self.extra = extra

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)

        self.create_widgets()
        self.carregar_dados()

    # ---------------------------------------------------------
    # INTERFACE
    # ---------------------------------------------------------
    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#673AB7', height=60)
        header.pack(fill='x')

        tk.Label(
            header,
            text="Gerenciamento de Coordenadores",
            font=('Arial', 16, 'bold'),
            bg='#673AB7',
            fg='white'
        ).pack(side='left', padx=20, pady=15)

        tk.Button(
            header,
            text="← Voltar",
            bg='#512DA8',
            fg='white',
            command=self.voltar,
            padx=15
        ).pack(side='right', padx=20)

        # Botões
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Novo", width=12, command=self.novo)\
            .grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Editar", width=12, command=self.editar)\
            .grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Remover", width=12, command=self.remover)\
            .grid(row=0, column=2, padx=5)

        # Tabela
        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Incluímos id_usuario como coluna "interna" (oculta) para facilitar CRUD
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'CPF', 'Data Nasc', 'Telefone', 'Email', 'ID_Usuario'),
            show='headings'
        )

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Data Nasc', text='Data Nasc.')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('ID_Usuario', text='ID Usuário')

        self.tree.column('ID', width=60)
        self.tree.column('Nome', width=220)
        self.tree.column('CPF', width=150)
        self.tree.column('Data Nasc', width=110)
        self.tree.column('Telefone', width=120)
        self.tree.column('Email', width=220)

        # Ocultar ID_Usuario
        self.tree.column('ID_Usuario', width=0, stretch=False)

        self.tree.pack(fill='both', expand=True)

    # ---------------------------------------------------------
    # CARREGAR DADOS DO BANCO
    # ---------------------------------------------------------
    def carregar_dados(self):
        session = DatabaseConnection.get_session()
        try:
            coordenadores = session.query(Coordenador).all()

            # Limpar árvore
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Preencher com dados do banco
            for coord in coordenadores:
                cpf = ""
                if getattr(coord, "usuario", None):
                    cpf = coord.usuario.cpf or ""

                data_nasc = ""
                if coord.data_nascimento:
                    try:
                        data_nasc = coord.data_nascimento.strftime('%d/%m/%Y')
                    except Exception:
                        data_nasc = ""

                self.tree.insert('', 'end', values=(
                    coord.id_coordenador,
                    coord.nome_completo,
                    cpf,
                    data_nasc,
                    coord.telefone,
                    coord.email,
                    coord.id_usuario  # coluna oculta
                ))
        finally:
            session.close()

    # ---------------------------------------------------------
    # NOVO
    # ---------------------------------------------------------
    def novo(self):
        self.abrir_formulario()

    # ---------------------------------------------------------
    # EDITAR
    # ---------------------------------------------------------
    def editar(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um coordenador!")
            return

        item = self.tree.item(selecionado[0])
        values = item['values']

        # values = (id_coordenador, nome, cpf, data_nasc, telefone, email, id_usuario)
        id_coordenador = values[0]
        nome = values[1]
        cpf = values[2]
        data_nasc = values[3]
        telefone = values[4]
        email = values[5]
        id_usuario = values[6]

        self.abrir_formulario(
            item_id=id_coordenador,
            id_usuario_atual=id_usuario,
            nome_atual=nome,
            cpf_atual=cpf,
            data_nascimento_atual=data_nasc,
            telefone_atual=telefone,
            email_atual=email
        )

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um coordenador!")
            return

        item = self.tree.item(selecionado[0])
        values = item['values']
        id_coordenador = values[0]
        id_usuario = values[6]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja realmente remover o coordenador?"
        )

        if not confirmar:
            return

        session = DatabaseConnection.get_session()
        try:
            coord = session.query(Coordenador).filter_by(id_coordenador=id_coordenador).first()
            if not coord:
                messagebox.showwarning("Aviso", "Coordenador não encontrado no banco!")
                return

            # Remove coordenador
            session.delete(coord)

            # Opcional: remover também o usuário associado (se existir)
            # (Se seu sistema referenciar Usuario em outros lugares, ajuste conforme sua regra.)
            if id_usuario:
                user = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
                if user:
                    session.delete(user)

            session.commit()
            self.carregar_dados()
        except IntegrityError:
            session.rollback()
            messagebox.showerror(
                "Erro",
                "Não foi possível remover. Verifique vínculos/constraints no banco."
            )
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Falha ao remover: {e}")
        finally:
            session.close()

    # ---------------------------------------------------------
    # FORMULÁRIO (NOVO E EDITAR)
    # ---------------------------------------------------------
    def abrir_formulario(
        self,
        item_id=None,
        id_usuario_atual=None,
        nome_atual="",
        cpf_atual="",
        data_nascimento_atual="",
        telefone_atual="",
        email_atual=""
    ):
        dialog = tk.Toplevel(self.root)
        dialog.title("Coordenador")
        dialog.geometry("420x520")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        titulo = "Editar Coordenador" if item_id else "Novo Coordenador"

        tk.Label(
            frame,
            text=titulo,
            font=('Arial', 14, 'bold')
        ).pack(pady=10)

        # Nome
        tk.Label(frame, text="Nome completo:").pack(anchor='w')
        nome_entry = tk.Entry(frame, width=38)
        nome_entry.insert(0, nome_atual)
        nome_entry.pack(pady=5)

        # CPF (Usuario)
        tk.Label(frame, text="CPF (Usuário):").pack(anchor='w')
        cpf_entry = tk.Entry(frame, width=38)
        cpf_entry.insert(0, cpf_atual)
        cpf_entry.pack(pady=5)

        # Senha (Usuario)
        senha_label_text = "Senha (Usuário):" if not item_id else "Senha (Usuário) [deixe em branco para manter]:"
        tk.Label(frame, text=senha_label_text).pack(anchor='w')
        senha_entry = tk.Entry(frame, width=38, show="*")
        senha_entry.pack(pady=5)

        # Data Nascimento
        tk.Label(frame, text="Data de nascimento (dd/mm/aaaa):").pack(anchor='w')
        data_entry = tk.Entry(frame, width=38)
        data_entry.insert(0, data_nascimento_atual)
        data_entry.pack(pady=5)

        # Telefone
        tk.Label(frame, text="Telefone:").pack(anchor='w')
        telefone_entry = tk.Entry(frame, width=38)
        telefone_entry.insert(0, telefone_atual)
        telefone_entry.pack(pady=5)

        # Email
        tk.Label(frame, text="Email:").pack(anchor='w')
        email_entry = tk.Entry(frame, width=38)
        email_entry.insert(0, email_atual)
        email_entry.pack(pady=5)

        def parse_data_br(data_str: str):
            data_str = (data_str or "").strip()
            try:
                return datetime.strptime(data_str, "%d/%m/%Y").date()
            except Exception:
                return None

        def salvar():
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()
            senha = senha_entry.get().strip()
            data_nasc = parse_data_br(data_entry.get())
            telefone = telefone_entry.get().strip()
            email = email_entry.get().strip()

            # Validações (conforme NOT NULL e UNIQUE)
            if not nome or not cpf or not data_nasc or not telefone or not email:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return

            # No cadastro, senha é obrigatória (Usuario.senha NOT NULL)
            if not item_id and not senha:
                messagebox.showerror("Erro", "Informe a senha para o novo usuário!")
                return

            session = DatabaseConnection.get_session()
            try:
                if item_id:
                    # EDITAR
                    coord = session.query(Coordenador).filter_by(id_coordenador=item_id).first()
                    if not coord:
                        messagebox.showerror("Erro", "Coordenador não encontrado no banco!")
                        return

                    user = session.query(Usuario).filter_by(id_usuario=coord.id_usuario).first()
                    if not user:
                        messagebox.showerror("Erro", "Usuário do coordenador não encontrado!")
                        return

                    # Atualiza coordenador
                    coord.nome_completo = nome
                    coord.data_nascimento = data_nasc
                    coord.telefone = telefone
                    coord.email = email

                    # Atualiza usuário
                    user.cpf = cpf
                    if senha:  # se digitou, troca
                        user.senha = senha

                    session.commit()
                    dialog.destroy()
                    self.carregar_dados()

                else:
                    # NOVO
                    novo_user = Usuario(
                        cpf=cpf,
                        senha=senha
                    )
                    session.add(novo_user)
                    session.flush()  # garante id_usuario preenchido

                    novo_coord = Coordenador(
                        nome_completo=nome,
                        data_nascimento=data_nasc,
                        telefone=telefone,
                        email=email,
                        id_usuario=novo_user.id_usuario
                    )
                    session.add(novo_coord)

                    session.commit()
                    dialog.destroy()
                    self.carregar_dados()

            except IntegrityError:
                session.rollback()
                messagebox.showerror(
                    "Erro",
                    "Violação de unicidade/constraint (CPF ou Email já existe, ou Usuário já vinculado)."
                )
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Falha ao salvar: {e}")
            finally:
                session.close()

        tk.Button(
            frame,
            text="Salvar",
            width=18,
            command=salvar
        ).pack(pady=20)

    # ---------------------------------------------------------
    # VOLTAR
    # ---------------------------------------------------------
    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username, self.extra)