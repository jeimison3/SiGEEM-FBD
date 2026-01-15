
import tkinter as tk
from tkinter import ttk, messagebox

class TurmasScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
        self.carregar_dados()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#FF9800', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="Gerenciamento de Professores", 
                font=('Arial', 16, 'bold'), bg='#FF9800', 
                fg='white').pack(side='left', padx=20, pady=15)
        
        back_btn = tk.Button(header, text="← Voltar", font=('Arial', 10),
                            bg='#F57C00', fg='white', 
                            command=self.voltar, cursor='hand2', padx=15)
        back_btn.pack(side='right', padx=20)
        
        # Botões de ação
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Novo", font=('Arial', 11, 'bold'),
                 bg='#4CAF50', fg='white', width=12, command=self.novo,
                 cursor='hand2').grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame, text="Editar", font=('Arial', 11, 'bold'),
                 bg='#FF9800', fg='white', width=12, command=self.editar,
                 cursor='hand2').grid(row=0, column=1, padx=5)
        
        tk.Button(btn_frame, text="Remover", font=('Arial', 11, 'bold'),
                 bg='#F44336', fg='white', width=12, command=self.remover,
                 cursor='hand2').grid(row=0, column=2, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(self.frame, bg='white')
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Nome', 'CPF', 'Especialidade'),
                                show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Especialidade', text='Especialidade')
        
        self.tree.column('ID', width=50)
        self.tree.column('Nome', width=250)
        self.tree.column('CPF', width=150)
        self.tree.column('Especialidade', width=200)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
    
    def carregar_dados(self):
        """TODO: Implementar carregamento de dados do banco"""
        self.tree.insert('', 'end', values=(1, 'Maria Santos', '987.654.321-00', 'Matemática'))
    
    def novo(self):
        """TODO: Implementar inserção no banco de dados"""
        messagebox.showinfo("Info", "Função NOVO - Implementar inserção no banco")
    
    def editar(self):
        """TODO: Implementar edição no banco de dados"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um professor para editar!")
            return
        messagebox.showinfo("Info", "Função EDITAR - Implementar atualização no banco")
    
    def remover(self):
        """TODO: Implementar remoção do banco de dados"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um professor para remover!")
            return
        messagebox.showinfo("Info", "Função REMOVER - Implementar exclusão do banco")
    
    def voltar(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
