
import tkinter as tk
from tkinter import messagebox
from database.connection import DatabaseConnection
from database.models import Usuario, Coordenador, Professor, Aluno
import bcrypt

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        self.role = ""
        self.nome = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title = tk.Label(self.frame, text="Sistema de Gerenciamento Escolar", 
                        font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333')
        title.pack(pady=50)
        
        # Container central
        login_frame = tk.Frame(self.frame, bg='white', padx=40, pady=40)
        login_frame.pack(pady=20)
        
        # Usuário
        tk.Label(login_frame, text="Usuário:", font=('Arial', 12), 
                bg='white').grid(row=0, column=0, sticky='w', pady=10)
        self.username_entry = tk.Entry(login_frame, font=('Arial', 12), width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Senha
        tk.Label(login_frame, text="Senha:", font=('Arial', 12), 
                bg='white').grid(row=1, column=0, sticky='w', pady=10)
        self.password_entry = tk.Entry(login_frame, font=('Arial', 12), 
                                      width=25, show='*')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Botão de login
        login_btn = tk.Button(login_frame, text="Entrar", font=('Arial', 12, 'bold'),
                             bg='#4CAF50', fg='white', width=20, height=2,
                             command=self.fazer_login, cursor='hand2')
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.password_entry.bind('<Return>', lambda e: self.fazer_login())
    
    def fazer_login(self):
        cpf = self.username_entry.get()
        password = self.password_entry.get()
        
        if not cpf or not password:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        if self.validar_credenciais(cpf, password):
            self.frame.destroy()
            from screens.dashboard import DashboardScreen
            DashboardScreen(self.root, cpf, [self.role, self.nome])
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")
    
    def validar_credenciais(self, cpf, password):
        resultado = False
        session = DatabaseConnection.get_session()
        
        salt = bcrypt.gensalt()
        try:
            usuario_check = session.query(Usuario).filter_by(cpf=cpf).first()
            if usuario_check:
                try:
                    resultado=bcrypt.checkpw(str(password).encode("utf-8"), str(usuario_check.senha).encode("utf-8"))
                    if resultado:
                        coord = session.query(Coordenador).filter_by(id_usuario=usuario_check.id_usuario).first()
                        profe = session.query(Professor).filter_by(id_usuario=usuario_check.id_usuario).first()
                        aluno = session.query(Aluno).filter_by(id_usuario=usuario_check.id_usuario).first()
                        if coord:
                            self.role = "Coordenador"
                            self.nome = coord.nome_completo
                        elif profe:
                            self.role = "Professor"
                            self.nome = profe.nome_completo
                        elif aluno:
                            self.role = "Aluno"
                            self.nome = aluno.nome_completo
                        else:
                            raise ValueError(f"A credencial não foi devidamente alocada a um tipo de usuário.")
                except Exception as e:
                    print(e)
        finally:
            session.close()
        return resultado

