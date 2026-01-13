import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import DatabaseConnection
from database.models import Professor

class ProfessoresScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        # Definição de Cores
        self.color_header = '#2c3e50'  # Azul Escuro
        self.color_toolbar = '#3D3D3D' # Cinza Escuro
        self.color_bg = '#3D3D3D'      # Fundo das laterais
        
        self.main_container = tk.Frame(root, bg=self.color_bg)
        self.main_container.pack(fill='both', expand=True)
        
        self.header = tk.Frame(self.main_container, bg=self.color_header, height=60)
        self.header.pack(fill='x')
        self.create_header_widgets()
    
        self.toolbar = tk.Frame(self.main_container, bg=self.color_toolbar, pady=15)
        self.toolbar.pack(fill='x')
        self.create_toolbar_widgets()

        # --- ÁREA DA TABELA
        
        self.table_frame = tk.Frame(self.main_container, bg='white')
        self.table_frame.place(relx=0.5, rely=0.62, relwidth=0.94, relheight=0.68, anchor='center')
        
        self.create_table_widgets()
        self.carregar_dados()
    
    def create_header_widgets(self):
        tk.Label(self.header, text="Gerenciamento de Professores", 
                font=('Arial', 18, 'bold'), bg=self.color_header, 
                fg='white').pack(side='left', padx=20, pady=15)
        
        tk.Button(self.header, text="← Voltar", font=('Arial', 10),
                 bg='#555555', fg='white', command=self.voltar, 
                 cursor='hand2', relief='flat', padx=15).pack(side='right', padx=20)

    def create_toolbar_widgets(self):
        btn_container = tk.Frame(self.toolbar, bg=self.color_toolbar)
        btn_container.pack(expand=True)
        
        tk.Button(btn_container, text="Novo", font=('Arial', 11, 'bold'),
                 bg='#4CAF50', fg='white', width=12, height=2, relief='flat',
                 command=lambda: self.abrir_formulario(), cursor='hand2').pack(side='left', padx=10)
        
        tk.Button(btn_container, text=" Editar", font=('Arial', 11, 'bold'),
                 bg='#FF9800', fg='white', width=12, height=2, relief='flat',
                 command=self.editar, cursor='hand2').pack(side='left', padx=10)
        
        tk.Button(btn_container, text=" Remover", font=('Arial', 11, 'bold'),
                 bg='#F44336', fg='white', width=12, height=2, relief='flat',
                 command=self.remover, cursor='hand2').pack(side='left', padx=10)

    def create_table_widgets(self):
        # Frame interno para dar um pequeno respiro entre a borda branca e a tabela
        inner_container = tk.Frame(self.table_frame, bg= self.color_toolbar)
        inner_container.pack(fill='both', expand=True)

        # Estilização
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=('Arial', 10))
        style.configure("Treeview.Heading", background="#2c3e50", foreground="#ffffff", font=('Arial', 10, 'bold'))
        
        scrollbar = ttk.Scrollbar(inner_container, orient="vertical")
        scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(
            inner_container, 
            columns=('ID', 'Nome', 'CPF', 'Especialidade'), 
            show='headings',
            yscrollcommand=scrollbar.set  
        )
        
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='NOME')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Especialidade', text='ESPECIALIDADE')
        
        self.tree.column('ID', width=50, anchor="center")
        self.tree.column('Nome', width=300)
        self.tree.column('CPF', width=150, anchor="center")
        self.tree.column('Especialidade', width=200, anchor="center")
        
        self.tree.pack(fill='both', expand=True)

    def abrir_formulario(self, professor_id=None):
        self.janela_form = tk.Toplevel(self.root)
        self.janela_form.title("Dados do Professor")
        largura, altura = 450, 480
        x = (self.janela_form.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_form.winfo_screenheight() // 2) - (altura // 2)
        self.janela_form.geometry(f"{largura}x{altura}+{x}+{y}")
        self.janela_form.grab_set() 
        self.janela_form.resizable(False, False)

        container = tk.Frame(self.janela_form, padx=40, pady=30)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Nome Completo:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_nome = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_nome.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="CPF:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_cpf = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_cpf.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="Especialidade:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_esp = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_esp.pack(pady=(0, 25), ipady=4)

        if professor_id:
            session = DatabaseConnection.get_session()
            p = session.query(Professor).get(professor_id)
            if p:
                self.ent_nome.insert(0, p.nome)
                self.ent_cpf.insert(0, p.cpf)
                self.ent_esp.insert(0, p.especialidade if p.especialidade else "")
            session.close()
            txt_btn, cor_btn = "Salvar Alterações", "#FF9800"
            cmd = lambda: self.salvar_no_banco(professor_id)
        else:
            txt_btn, cor_btn = "Cadastrar Professor", "#4CAF50"
            cmd = lambda: self.salvar_no_banco()

        tk.Button(container, text=txt_btn, bg=cor_btn, fg="white", 
                 font=('Arial', 12, 'bold'), command=cmd, 
                 cursor="hand2", height=2, relief='flat').pack(fill="x")

    def salvar_no_banco(self, professor_id=None):
        nome, cpf, esp = self.ent_nome.get(), self.ent_cpf.get(), self.ent_esp.get()
        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios!")
            return

        session = DatabaseConnection.get_session()
        try:
            if professor_id:
                p = session.query(Professor).get(professor_id)
                p.nome, p.cpf, p.especialidade = nome, cpf, esp
            else:
                session.add(Professor(nome=nome, cpf=cpf, especialidade=esp))
            session.commit()
            messagebox.showinfo("Sucesso", "Operação realizada!")
            self.janela_form.destroy()
            self.carregar_dados()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            session.close()

    def carregar_dados(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        session = DatabaseConnection.get_session()
        try:
            for p in session.query(Professor).all():
                self.tree.insert('', 'end', values=(p.id, p.nome, p.cpf, p.especialidade))
        finally:
            session.close()

    def editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um item.")
            return
        self.abrir_formulario(self.tree.item(sel)['values'][0])

    def remover(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            id_p = self.tree.item(sel)['values'][0]
            session = DatabaseConnection.get_session()
            try:
                p = session.query(Professor).get(id_p)
                session.delete(p)
                session.commit()
                self.carregar_dados()
            finally:
                session.close()

    def voltar(self):
        self.main_container.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)