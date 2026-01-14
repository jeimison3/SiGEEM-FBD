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
            font=('Arial', 10),
            bg='#512DA8',
            fg='white',
            command=self.voltar,
            padx=15
        ).pack(side='right', padx=20)

        # Botões
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Novo", width=12, command=self.novo).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", width=12, command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remover", width=12, command=self.remover).grid(row=0, column=2, padx=5)

        # Tabela
        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(padx=20, pady=10, fill='both', expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Nome', 'CPF'),
            show='headings'
        )

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')

        self.tree.column('ID', width=60)
        self.tree.column('Nome', width=250)
        self.tree.column('CPF', width=150)

        self.tree.pack(fill='both', expand=True)

    def carregar_dados(self):
        # Dados de exemplo
        self.tree.insert('', 'end', values=(1, 'Ana Paula', '123.456.789-00'))
        self.tree.insert('', 'end', values=(2, 'Carlos Eduardo', '987.654.321-00'))

    def novo(self):
        self.abrir_formulario()

    def editar(self):
        if not self.tree.selection():
            messagebox.showwarning("Aviso", "Selecione um coordenador!")
            return
        messagebox.showinfo("Editar", "Editar coordenador (ainda não implementado)")

    def remover(self):
        if not self.tree.selection():
            messagebox.showwarning("Aviso", "Selecione um coordenador!")
            return
        messagebox.showinfo("Remover", "Remover coordenador (ainda não implementado)")
    def novo(self):
        self.abrir_formulario()

    def abrir_formulario(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Coordenador")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill='both', expand=True)

        tk.Label(
            frame,
            text="Cadastrar Coordenador",
            font=('Arial', 14, 'bold')
        ).pack(pady=10)

        tk.Label(frame, text="Nome:").pack(anchor='w')
        nome_entry = tk.Entry(frame, width=30)
        nome_entry.pack(pady=5)

        tk.Label(frame, text="CPF:").pack(anchor='w')
        cpf_entry = tk.Entry(frame, width=30)
        cpf_entry.pack(pady=5)

        def salvar():
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()

            if not nome or not cpf:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            messagebox.showinfo(
                "Sucesso",
                f"Coordenador cadastrado:\n\nNome: {nome}\nCPF: {cpf}"
            )
            dialog.destroy()

        tk.Button(
            frame,
            text="Salvar",
            width=15,
            command=salvar
        ).pack(pady=15)

    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
        