# ============================================================
# Arquivo: screens/coordenadores.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox


class CoordenadoresScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username

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

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'CPF', 'Email'),
            show='headings'
        )

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Email', text='Email')

        self.tree.column('ID', width=60)
        self.tree.column('Nome', width=220)
        self.tree.column('CPF', width=150)
        self.tree.column('Email', width=220)

        self.tree.pack(fill='both', expand=True)

    # ---------------------------------------------------------
    # DADOS DE EXEMPLO
    # ---------------------------------------------------------
    def carregar_dados(self):
        self.tree.insert('', 'end', values=(1, 'Ana Paula', '123.456.789-00', 'ana@email.com'))
        self.tree.insert('', 'end', values=(2, 'Carlos Eduardo', '987.654.321-00', 'carlos@email.com'))

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
        _, nome, cpf, email = item['values']

        self.abrir_formulario(
            item_id=selecionado[0],
            nome_atual=nome,
            cpf_atual=cpf,
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

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja realmente remover o coordenador?"
        )

        if confirmar:
            self.tree.delete(selecionado[0])

    # ---------------------------------------------------------
    # FORMULÁRIO (NOVO E EDITAR)
    # ---------------------------------------------------------
    def abrir_formulario(self, item_id=None, nome_atual="", cpf_atual="", email_atual=""):
        dialog = tk.Toplevel(self.root)
        dialog.title("Coordenador")
        dialog.geometry("400x360")
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
        nome_entry = tk.Entry(frame, width=35)
        nome_entry.insert(0, nome_atual)
        nome_entry.pack(pady=5)

        # CPF
        tk.Label(frame, text="CPF:").pack(anchor='w')
        cpf_entry = tk.Entry(frame, width=35)
        cpf_entry.insert(0, cpf_atual)
        cpf_entry.pack(pady=5)

        # Email
        tk.Label(frame, text="Email:").pack(anchor='w')
        email_entry = tk.Entry(frame, width=35)
        email_entry.insert(0, email_atual)
        email_entry.pack(pady=5)

        def salvar():
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()
            email = email_entry.get().strip()

            if not nome or not cpf or not email:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            if item_id:
                self.tree.item(
                    item_id,
                    values=(item_id, nome, cpf, email)
                )
            else:
                novo_id = len(self.tree.get_children()) + 1
                self.tree.insert(
                    '',
                    'end',
                    values=(novo_id, nome, cpf, email)
                )

            dialog.destroy()

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
        DashboardScreen(self.root, self.username)

