import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import DatabaseConnection
from database.models import Disciplina, Professor

class DisciplinasScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        self.color_header = '#2c3e50'
        self.color_toolbar = '#3D3D3D'
        self.color_bg = '#3D3D3D'
        
        self.main_container = tk.Frame(root, bg=self.color_bg)
        self.main_container.pack(fill='both', expand=True)
        self.header = tk.Frame(self.main_container, bg=self.color_header, height=60)
        self.header.pack(fill='x')
        self.create_header_widgets()
        
        self.toolbar = tk.Frame(self.main_container, bg=self.color_toolbar, pady=15)
        self.toolbar.pack(fill='x')
        self.create_toolbar_widgets()

        self.table_frame = tk.Frame(self.main_container, bg='white')
        self.table_frame.place(relx=0.5, rely=0.62, relwidth=0.94, relheight=0.68, anchor='center')
        
        self.create_table_widgets()
        self.carregar_dados()
    
    def create_header_widgets(self):
        tk.Label(self.header, text="Gerenciamento de Disciplinas", 
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
        inner_container = tk.Frame(self.table_frame, bg=self.color_toolbar)
        inner_container.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=('Arial', 10))
        style.configure("Treeview.Heading", background="#2c3e50", foreground="#ffffff", font=('Arial', 10, 'bold'))
        
        scrollbar = ttk.Scrollbar(inner_container, orient="vertical")
        scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(
            inner_container, 
            columns=('ID', 'Nome', 'Carga', 'Professor'), 
            show='headings',
            yscrollcommand=scrollbar.set  
        )
        
        scrollbar.config(command=self.tree.yview)
        
        tk.Button(self.table_frame, text="🗑️ Remover", bg='#F44336', fg='white', width=12,
                  command=self.remover).pack(side='left', padx=5)

        # Tabela (Treeview)
        self.tree = ttk.Treeview(self.table_frame, columns=('ID', 'Titulo', 'Turma'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='NOME DA DISCIPLINA')
        self.tree.heading('Carga', text='CARGA HORÁRIA')
        self.tree.heading('Professor', text='PROFESSOR RESPONSÁVEL')
        
        self.tree.column('ID', width=50, anchor="center")
        self.tree.column('Nome', width=300)
        self.tree.column('Carga', width=150, anchor="center")
        self.tree.column('Professor', width=250)
        
        self.tree.pack(fill='both', expand=True)

    def abrir_formulario(self, disciplina_id=None):
        self.janela_form = tk.Toplevel(self.root)
        self.janela_form.title("Dados da Disciplina")
        largura, altura = 450, 480
        x = (self.janela_form.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_form.winfo_screenheight() // 2) - (altura // 2)
        self.janela_form.geometry(f"{largura}x{altura}+{x}+{y}")
        self.janela_form.grab_set() 
        self.janela_form.resizable(False, False)

        container = tk.Frame(self.janela_form, padx=40, pady=30)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Nome da Disciplina:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_nome = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_nome.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="Carga Horária (horas):", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_carga = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_carga.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="Professor Responsável:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.combo_prof = ttk.Combobox(container, width=37, font=('Arial', 11), state="readonly")
        self.combo_prof.pack(pady=(0, 25), ipady=4)

        session = DatabaseConnection.get_session()
        professores = session.query(Professor).all()
        self.combo_prof['values'] = [f"{p.id_professor} - {p.nome_completo}" for p in professores]

        if disciplina_id:
            d = session.query(Disciplina).get(disciplina_id)
            if d:
                self.ent_nome.insert(0, d.nome_disciplina)
                self.ent_carga.insert(0, d.carga_horaria)
                if d.professor:
                    self.combo_prof.set(f"{d.professor.id_professor} - {d.professor.nome_completo}")
            
            txt_btn, cor_btn = "Salvar Alterações", "#FF9800"
            cmd = lambda: self.salvar_no_banco(disciplina_id)
        else:
            txt_btn, cor_btn = "Cadastrar Disciplina", "#4CAF50"
            cmd = lambda: self.salvar_no_banco()
        
        session.close()

        tk.Button(container, text=txt_btn, bg=cor_btn, fg="white", 
                 font=('Arial', 12, 'bold'), command=cmd, 
                 cursor="hand2", height=2, relief='flat').pack(fill="x")

    def salvar_no_banco(self, disciplina_id=None):
        nome, carga = self.ent_nome.get(), self.ent_carga.get()
        prof_selecionado = self.combo_prof.get()

        if not nome or not carga:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios!")
            return
        
       
        try:
            carga_final = int(carga)
        except ValueError:
            messagebox.showerror("Erro", "Carga Horária deve ser um número inteiro!")
            return

        session = DatabaseConnection.get_session()
        try:
            prof_id = int(prof_selecionado.split(" - ")[0]) if prof_selecionado else None
            
            if disciplina_id:
                d = session.query(Disciplina).get(disciplina_id)
                d.nome_disciplina, d.carga_horaria, d.id_professor = nome, int(carga), prof_id
            else:
                session.add(Disciplina(nome_disciplina=nome, carga_horaria=int(carga), id_professor=prof_id))
            
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
            for d in session.query(Disciplina).all():
                print(d)
                nome_prof = d.professor.nome_completo if d.professor else "Não atribuído"
                self.tree.insert('', 'end', values=(d.id_disciplina, d.nome_disciplina, d.carga_horaria, nome_prof))
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
        if messagebox.askyesno("Confirmar", "Deseja excluir esta disciplina?"):
            id_d = self.tree.item(sel)['values'][0]
            session = DatabaseConnection.get_session()
            try:
                d = session.query(Disciplina).get(id_d)
                session.delete(d)
                session.commit()
                self.carregar_dados()
            finally:
                session.close()

    def voltar(self):
        self.main_container.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
