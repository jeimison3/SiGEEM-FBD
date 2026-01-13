import tkinter as tk

class DashboardScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        
        # Centralização da Janela Principal
        largura_janela = 900
        altura_janela = 600
        
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.title(f"SiGEEM - Painel de Controle ({self.username})")

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        header = tk.Frame(self.frame, bg='#2196F3', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Bem-vindo, {self.username}!", 
                font=('Arial', 14, 'bold'), bg='#2196F3', fg='white').pack(
                    side='left', padx=20, pady=20)
        
        logout_btn = tk.Button(header, text="Sair", font=('Arial', 10),
                              bg='#f44336', fg='white', command=self.logout,
                              cursor='hand2', padx=15)
        logout_btn.pack(side='right', padx=20)
        
        # Título Central
        tk.Label(self.frame, text="SiGEEM - Sistema Escolar", 
                font=('Arial', 24, 'bold'), bg='#f0f0f0', 
                fg='#333').pack(pady=40)
        
        # Container dos botões
        buttons_frame = tk.Frame(self.frame, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        buttons = [
            ("Turmas", self.abrir_turmas, '#4CAF50'),
            ("Alunos", self.abrir_alunos, '#2196F3'),
            ("Professores", self.abrir_professores, '#FF9800'),
            ("Disciplinas", self.abrir_disciplinas, '#9C27B0'),
            ("Agendar Aulas", self.abrir_aulas, '#3F51B5'), # RF07
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(buttons_frame, text=text, font=('Arial', 13, 'bold'),
                          bg=color, fg='white', width=18, height=3,
                          command=command, cursor='hand2', relief='flat')
            btn.grid(row=row, column=col, padx=15, pady=15)

    #Métodos de Navegação com Importação Local
    
    def abrir_turmas(self):
        self.frame.destroy()
        from screens.turmas import TurmasScreen
        TurmasScreen(self.root, self.username)
    
    def abrir_alunos(self):
        self.frame.destroy()
        from screens.alunos import AlunosScreen
        AlunosScreen(self.root, self.username)
    
    def abrir_professores(self):
        self.frame.destroy()
        from screens.professores import ProfessoresScreen
        ProfessoresScreen(self.root, self.username)
    
    def abrir_disciplinas(self):
        self.frame.destroy()
        from screens.disciplinas import DisciplinasScreen
        DisciplinasScreen(self.root, self.username)

    def abrir_aulas(self):
        self.frame.destroy()
        from screens.aulas import AulasScreen
        AulasScreen(self.root, self.username)
    
    def logout(self):
        from screens.login import LoginScreen
        self.frame.destroy()
        LoginScreen(self.root)