import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import DatabaseConnection
from database.models import Aula, Professor, Turma, Disciplina
from datetime import datetime

class AulasScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        # Definição de Cores
        self.color_header = '#2c3e50'  # Azul Escuro
        self.color_toolbar = '#3D3D3D' # Cinza Escuro
        self.color_bg = '#3D3D3D'      # Fundo das laterais
        
        # Container Principal
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
        tk.Label(self.header, text="Gestão de Horários e Aulas", 
                font=('Arial', 18, 'bold'), bg=self.color_header, 
                fg='white').pack(side='left', padx=20, pady=15)
        
        tk.Button(self.header, text="← Voltar", font=('Arial', 10),
                 bg='#555555', fg='white', command=self.voltar, 
                 cursor='hand2', relief='flat', padx=15).pack(side='right', padx=20)

    def create_toolbar_widgets(self):
        btn_container = tk.Frame(self.toolbar, bg=self.color_toolbar)
        btn_container.pack(expand=True)
        
        # Botão Novo
        tk.Button(btn_container, text="Agendar Aula", font=('Arial', 11, 'bold'),
                 bg='#4CAF50', fg='white', width=18, height=2, relief='flat',
                 command=self.abrir_formulario, cursor='hand2').pack(side='left', padx=10)
        
        # Botão Remover
        tk.Button(btn_container, text="Cancelar Aula", font=('Arial', 11, 'bold'),
                 bg='#F44336', fg='white', width=18, height=2, relief='flat',
                 command=self.remover_aula, cursor='hand2').pack(side='left', padx=10)

    def create_table_widgets(self):
        inner_container = tk.Frame(self.table_frame, bg=self.color_toolbar)
        inner_container.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=('Arial', 10))
        style.configure("Treeview.Heading", background="#2c3e50", foreground="#ffffff", font=('Arial', 10, 'bold'))
        
        scrollbar = ttk.Scrollbar(inner_container, orient="vertical")
        scrollbar.pack(side='right', fill='y')

        columns = ('ID', 'Data', 'Horário', 'Disciplina', 'Professor', 'Turma')
        self.tree = ttk.Treeview(
            inner_container, 
            columns=columns, 
            show='headings',
            yscrollcommand=scrollbar.set  
        )
        
        scrollbar.config(command=self.tree.yview)
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center", width=120)
        
        self.tree.column('ID', width=50)
        self.tree.column('Disciplina', width=200)
        self.tree.column('Professor', width=200)
        
        self.tree.pack(fill='both', expand=True)

    def abrir_formulario(self):
        self.janela_form = tk.Toplevel(self.root)
        self.janela_form.title("Novo Agendamento")
        
        largura, altura = 450, 580
        x = (self.janela_form.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela_form.winfo_screenheight() // 2) - (altura // 2)
        self.janela_form.geometry(f"{largura}x{altura}+{x}+{y}")
        self.janela_form.grab_set()
        self.janela_form.resizable(False, False)

        container = tk.Frame(self.janela_form, padx=40, pady=20)
        container.pack(fill="both", expand=True)

        session = DatabaseConnection.get_session()

        fields = [
            ("Professor:", "cb_prof", [f"{p.id} - {p.nome}" for p in session.query(Professor).all()]),
            ("Disciplina:", "cb_disc", [f"{d.id} - {d.nome}" for d in session.query(Disciplina).all()]),
            ("Turma:", "cb_turma", [f"{t.id} - {t.nome}" for t in session.query(Turma).all()])
        ]

        for label_text, attr_name, values in fields:
            tk.Label(container, text=label_text, font=('Arial', 10, 'bold')).pack(anchor="w")
            combo = ttk.Combobox(container, width=37, state="readonly", font=('Arial', 11))
            combo['values'] = values
            combo.pack(pady=(0, 15), ipady=4)
            setattr(self, attr_name, combo)

        tk.Label(container, text="Data (AAAA-MM-DD):", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_data = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_data.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="Início (HH:MM):", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_ini = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_ini.pack(pady=(0, 15), ipady=4)

        tk.Label(container, text="Fim (HH:MM):", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.ent_fim = tk.Entry(container, width=40, font=('Arial', 11))
        self.ent_fim.pack(pady=(0, 20), ipady=4)

        tk.Button(container, text="Confirmar Horário", bg="#4CAF50", fg="white",
                  font=('Arial', 12, 'bold'), command=self.salvar_aula, 
                  cursor="hand2", height=2, relief='flat').pack(fill="x")
        
        session.close()

    def salvar_aula(self):
        try:
            if not all([self.cb_prof.get(), self.cb_disc.get(), self.cb_turma.get(), self.ent_ini.get()]):
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return

            p_id = int(self.cb_prof.get().split(" - ")[0])
            d_id = int(self.cb_disc.get().split(" - ")[0])
            t_id = int(self.cb_turma.get().split(" - ")[0])
            data_aula = datetime.strptime(self.ent_data.get(), "%Y-%m-%d").date()

            session = DatabaseConnection.get_session()
            
            conflito = session.query(Aula).filter(
                Aula.professor_id == p_id,
                Aula.data_aula == data_aula,
                Aula.hora_inicio == self.ent_ini.get()
            ).first()

            if conflito:
                messagebox.showerror("Erro de Regra", "Conflito: Professor já ocupado neste horário!")
                session.close()
                return

            nova_aula = Aula(
                professor_id=p_id, disciplina_id=d_id, turma_id=t_id,
                data_aula=data_aula, hora_inicio=self.ent_ini.get(), hora_fim=self.ent_fim.get()
            )

            session.add(nova_aula)
            session.commit()
            session.close()
            
            messagebox.showinfo("Sucesso", "Aula agendada com sucesso!")
            self.janela_form.destroy()
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao agendar: {e}")

    def carregar_dados(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        session = DatabaseConnection.get_session()
        try:
            for a in session.query(Aula).all():
                self.tree.insert('', 'end', values=(
                    a.id, a.data_aula, f"{a.hora_inicio}-{a.hora_fim}", 
                    a.disciplina.nome, a.professor.nome, a.turma.nome
                ))
        finally:
            session.close()

    def remover_aula(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma aula para remover.")
            return
        if messagebox.askyesno("Confirmar", "Deseja cancelar esta aula?"):
            id_aula = self.tree.item(sel)['values'][0]
            session = DatabaseConnection.get_session()
            try:
                aula = session.query(Aula).get(id_aula)
                session.delete(aula)
                session.commit()
                self.carregar_dados()
            finally:
                session.close()

    def voltar(self):
        self.main_container.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)