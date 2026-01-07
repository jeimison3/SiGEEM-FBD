
import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
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
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.fazer_login())
    
    def fazer_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # TODO: Implementar validação real no banco de dados
        if self.validar_credenciais(username, password):
            self.frame.destroy()
            # IMPORTAÇÃO LOCAL para evitar circular import
            from screens.dashboard import DashboardScreen
            DashboardScreen(self.root, username)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")
    
    def validar_credenciais(self, username, password):
        """TODO: Implementar validação de credenciais no banco de dados"""
        return True

