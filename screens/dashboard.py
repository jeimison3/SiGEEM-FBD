import tkinter as tk

class DashboardScreen:
    def __init__(self, root, cpf, extra):
        self.root = root
        self.cpf = cpf
        [role, nome_user] = extra
        self.extra = extra
        self.nome = nome_user
        self.role = role
        
        # Centralização da Janela Principal
        largura_janela = 900
        altura_janela = 600
        
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.title(f"SiGEEM - Painel de Controle ({self.nome})")

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        header = tk.Frame(self.frame, bg='#2196F3', height=80)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Bem-vindo, {self.nome}!", 
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
        
        if self.role == "Aluno":
            buttons = []
        elif self.role == "Professor":
            buttons = [
                ("Turmas", self.abrir_turmas, '#4CAF50'),
                ("Notas", self.abrir_notas, '#F44336')
            ]
        elif self.role == "Coordenador":
            buttons = [
                ("Turmas", self.abrir_turmas, '#4CAF50'),
                ("Alunos", self.abrir_alunos, '#2196F3'),
                ("Professores", self.abrir_professores, '#FF9800'),
                ("Disciplinas", self.abrir_disciplinas, '#9C27B0'),
                ("Notas", self.abrir_notas, '#F44336'),
                ("Coordenadores", self.abrir_coordenadores, '#673AB7')
            ]
        else:
            raise TypeError("O usuário não deveria estar aqui.")
        
        for i, (text, command, color) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(buttons_frame, text=text, font=('Arial', 13, 'bold'),
                          bg=color, fg='white', width=18, height=3,
                          command=command, cursor='hand2', relief='flat')
            btn.grid(row=row, column=col, padx=15, pady=15)
    
    def abrir_turmas(self):
        self.frame.destroy()
        from screens.turmas import TurmasScreen
        TurmasScreen(self.root, self.cpf, self.extra)
    
    def abrir_alunos(self):
        self.frame.destroy()
        from screens.alunos import AlunosScreen
        AlunosScreen(self.root, self.cpf, self.extra)

    def abrir_coordenadores(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.coordenadores import CoordenadoresScreen
        CoordenadoresScreen(self.root, self.cpf, self.extra)
    
    def abrir_professores(self):
        self.frame.destroy()
        from screens.professores import ProfessoresScreen
        ProfessoresScreen(self.root, self.cpf, self.extra)
    
    def abrir_disciplinas(self):
        self.frame.destroy()
        from screens.disciplinas import DisciplinasScreen
        DisciplinasScreen(self.root, self.cpf, self.extra)
        
    def abrir_notas(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.notas import NotasScreen
        NotasScreen(self.root, self.cpf, self.extra)
    
    # def abrir_frequencia(self):
    #     self.frame.destroy()
    #     # IMPORTAÇÃO LOCAL
    #     from screens.frequencia import FrequenciaScreen
    #     FrequenciaScreen(self.root, self.cpf)
    
    def logout(self):
        from screens.login import LoginScreen
        self.frame.destroy()
        LoginScreen(self.root)