# ============================================================
# Arquivo: screens/coordenadores.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.connection import SessionLocal
from database.models import Coordenador, Usuario


class CoordenadoresScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.db = SessionLocal()

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)

        self.create_widgets()
        self.carregar_dados()

    # ---------------------------------------------------------
    # INTERFACE
    # ---------------------------------------------------------
    def create_widgets(self):
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

        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Novo", width=12, command=self.novo).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", width=12, command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remover", width=12, command=self.remover).grid(row=0, column=2, padx=5)

        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(padx=20, pady=10, fill='both', expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'CPF', 'Email'),
            show='headings'
        )

        for col in ('ID', 'Nome', 'CPF', 'Email'):
            self.tree.heading(col, text=col)

        self.tree.column('ID', width=60)
        self.tree.column('Nome', width=220)
        self.tree.column('CPF', width=150)
        self.tree.column('Email', width=220)

        self.tree.pack(fill='both', expand=True)

    # ---------------------------------------------------------
    # CARREGAR DO BANCO
    # ---------------------------------------------------------
    def carregar_dados(self):
        self.tree.delete(*self.tree.get_children())

        coordenadores = self.db.query(Coordenador).all()
        for c in coordenadores:
            self.tree.insert('', 'end', values=(
                c.id_coordenador,
                c.nome_completo,
                c.usuario.cpf,
                c.email
            ))

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
        id_coordenador = item["values"][0]

        coord = self.db.query(Coordenador).get(id_coordenador)
        self.abrir_formulario(coord)

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um coordenador!")
            return

        if not messagebox.askyesno("Confirmar", "Deseja remover o coordenador?"):
            return

        item = self.tree.item(selecionado[0])
        id_coordenador = item["values"][0]

        coord = self.db.query(Coordenador).get(id_coordenador)

        self.db.delete(coord.usuario)
        self.db.delete(coord)
        self.db.commit()

        self.carregar_dados()

    # ---------------------------------------------------------
    # FORMULÁRIO
    # ---------------------------------------------------------
    def abrir_formulario(self, coordenador=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Coordenador")
        dialog.geometry("420x420")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        def campo(label):
            tk.Label(frame, text=label).pack(anchor='w')
            e = tk.Entry(frame, width=40)
            e.pack(pady=5)
            return e

        nome_entry = campo("Nome completo")
        nasc_entry = campo("Data nascimento (YYYY-MM-DD)")
        tel_entry = campo("Telefone")
        email_entry = campo("Email")
        cpf_entry = campo("CPF")
        senha_entry = campo("Senha")

        if coordenador:
            nome_entry.insert(0, coordenador.nome_completo)
            nasc_entry.insert(0, coordenador.data_nascimento.strftime("%Y-%m-%d"))
            tel_entry.insert(0, coordenador.telefone)
            email_entry.insert(0, coordenador.email)
            cpf_entry.insert(0, coordenador.usuario.cpf)

        def salvar():
            try:
                nome = nome_entry.get().strip()
                cpf = cpf_entry.get().strip()
                email = email_entry.get().strip()

                if not nome or not cpf or not email:
                    messagebox.showerror("Erro", "Preencha todos os campos!")
                    return

                if coordenador:
                    coordenador.nome_completo = nome
                    coordenador.email = email
                    coordenador.telefone = tel_entry.get()
                    coordenador.data_nascimento = datetime.strptime(
                        nasc_entry.get(), "%Y-%m-%d"
                    ).date()
                    coordenador.usuario.cpf = cpf
                else:
                    user = Usuario(
                        cpf=cpf,
                        senha=senha_entry.get()
                    )
                    self.db.add(user)
                    self.db.flush()

                    novo = Coordenador(
                        nome_completo=nome,
                        data_nascimento=datetime.strptime(
                            nasc_entry.get(), "%Y-%m-%d"
                        ).date(),
                        telefone=tel_entry.get(),
                        email=email,
                        id_usuario=user.id_usuario
                    )
                    self.db.add(novo)

                self.db.commit()
                messagebox.showinfo("Sucesso", "Coordenador salvo com sucesso!")
                dialog.destroy()
                self.carregar_dados()

            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Erro", str(e))

        tk.Button(frame, text="Salvar", width=15, command=salvar).pack(pady=15)

    # ---------------------------------------------------------
    # VOLTAR
    # ---------------------------------------------------------
    def voltar(self):
        self.db.close()
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
