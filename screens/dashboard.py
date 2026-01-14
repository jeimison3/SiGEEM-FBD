
import tkinter as tk

class DashboardScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#2196F3', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Bem-vindo, {self.username}!", 
                font=('Arial', 16, 'bold'), bg='#2196F3', fg='white').pack(
                    side='left', padx=20, pady=20)
        
        logout_btn = tk.Button(header, text="Sair", font=('Arial', 10),
                              bg='#f44336', fg='white', command=self.logout,
                              cursor='hand2', padx=15)
        logout_btn.pack(side='right', padx=20)
        
        # Título
        tk.Label(self.frame, text="Dashboard - Sistema Escolar", 
                font=('Arial', 22, 'bold'), bg='#f0f0f0', 
                fg='#333').pack(pady=30)
        
        # Container dos botões
        buttons_frame = tk.Frame(self.frame, bg='#f0f0f0')
        buttons_frame.pack(pady=20)
        
        # Definir botões
        buttons = [
            ("Turmas", self.abrir_turmas, '#4CAF50'),
            ("Alunos", self.abrir_alunos, '#2196F3'),
            ("Professores", self.abrir_professores, '#FF9800'),
            ("Disciplinas", self.abrir_disciplinas, '#9C27B0'),
            ("Coordenadores", self.abrir_coordenadores, '#673AB7'),
            # ("Notas", self.abrir_notas, '#F44336'),
            # ("Frequência", self.abrir_frequencia, '#00BCD4')
        ]
        
        # Criar grid de botões
        for i, (text, command, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(buttons_frame, text=text, font=('Arial', 14, 'bold'),
                          bg=color, fg='white', width=15, height=3,
                          command=command, cursor='hand2')
            btn.grid(row=row, column=col, padx=15, pady=15)
    
    def abrir_turmas(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.turmas import TurmasScreen
        TurmasScreen(self.root, self.username)
    
    def abrir_alunos(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.alunos import AlunosScreen
        AlunosScreen(self.root, self.username)

    def abrir_coordenadores(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.coordenadores import CoordenadoresScreen
        CoordenadoresScreen(self.root, self.username)
    
    def abrir_professores(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.professores import ProfessoresScreen
        ProfessoresScreen(self.root, self.username)
    
    def abrir_disciplinas(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.disciplinas import DisciplinasScreen
        DisciplinasScreen(self.root, self.username)
    
    # def abrir_notas(self):
    #     self.frame.destroy()
    #     # IMPORTAÇÃO LOCAL
    #     from screens.notas import NotasScreen
    #     NotasScreen(self.root, self.username)
    
    # def abrir_frequencia(self):
    #     self.frame.destroy()
    #     # IMPORTAÇÃO LOCAL
    #     from screens.frequencia import FrequenciaScreen
    #     FrequenciaScreen(self.root, self.username)
    
    def logout(self):
        # IMPORTAÇÃO LOCAL
        from screens.login import LoginScreen
        self.frame.destroy()
        LoginScreen(self.root)