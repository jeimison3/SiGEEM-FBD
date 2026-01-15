# ============================================================
# Arquivo: screens/notas.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class NotasScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
        self.carregar_dados()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#2196F3', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="Gerenciamento de Notas", 
                font=('Arial', 16, 'bold'), bg='#2196F3', 
                fg='white').pack(side='left', padx=20, pady=15)
        
        back_btn = tk.Button(header, text="← Voltar", font=('Arial', 10),
                            bg='#1976D2', fg='white', 
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
        
        self.tree = ttk.Treeview(tree_frame, columns=('TurmaNome', 'NomeAluno', 'DisciNome', 'ProfeNome', 'Avali', 'Nota'),
                                show='headings', yscrollcommand=scrollbar.set)
        
        self.tree.heading('TurmaNome', text='Turma')
        self.tree.heading('NomeAluno', text='Aluno')
        self.tree.heading('DisciNome', text='Disciplina')
        self.tree.heading('ProfeNome', text='Professor')
        self.tree.heading('Avali', text='Avaliação')
        self.tree.heading('Nota', text='Nota')
        
        self.tree.column('TurmaNome', width=50)
        self.tree.column('NomeAluno', width=200)
        self.tree.column('DisciNome', width=120)
        self.tree.column('ProfeNome', width=120)
        self.tree.column('Avali', width=150)
        self.tree.column('Nota', width=150)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
    
    def carregar_dados(self):
        from database.connection import DatabaseConnection
        from database.models import Aluno, Turma, Nota, Disciplina, Professor
        
        session = DatabaseConnection.get_session()
        try:
            notas = session.query(Nota).all()
            
            # Limpar árvore
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Preencher com dados do banco
            for nota in notas:
                turma_nome = ""
                aluno_nome = ""
                disci_nome = ""
                profe_nome = ""
                avali_nome = ""
                if nota.id_turma:
                    turma = session.query(Turma).filter_by(id_turma=nota.id_turma).first()
                    if turma:
                        turma_nome = turma.nome
                if nota.id_aluno:
                    aluno = session.query(Aluno).filter_by(id_aluno=nota.id_aluno).first()
                    if aluno:
                        aluno_nome = aluno.nome_completo
                if nota.id_disciplina:
                    disciplina = session.query(Disciplina).filter_by(id_disciplina=nota.id_disciplina).first()
                    if disciplina:
                        disci_nome = disciplina.nome_disciplina
                if nota.id_professor:
                    professor = session.query(Professor).filter_by(id_professor=nota.id_professor).first()
                    if turma:
                        profe_nome = professor.nome_completo
                # if nota.id_avaliacao:
                #     avaliacao = session.query(Avaliacao).filter_by(id_avaliacao=nota.id_avaliacao).first()
                #     if avaliacao:
                #         avali_nome = avaliacao.nome_avaliacao
                
                data_nasc = aluno.data_nascimento.strftime('%d/%m/%Y') if aluno.data_nascimento else ''
                
                self.tree.insert('', 'end', values=(
                    turma_nome,
                    aluno_nome,
                    disci_nome,
                    profe_nome,
                    # avali_nome,
                    nota.nota
                ))
        finally:
            session.close()
        
        # Dados de exemplo (remover quando implementar banco)
        # self.tree.insert('', 'end', values=(1, 'João Silva', '123.456.789-00', '01/01/2010', '1º Ano A'))
        # self.tree.insert('', 'end', values=(2, 'Maria Costa', '987.654.321-00', '15/03/2011', '2º Ano B'))
        # self.tree.insert('', 'end', values=(3, 'Pedro Santos', '456.789.123-00', '22/07/2009', '1º Ano A'))
    
    def novo(self):
        """Abrir formulário para cadastrar novo aluno"""
        self.abrir_formulario(modo='novo')
    
    def editar(self):
        """Abrir formulário para editar aluno selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar!")
            return
        
        # Pegar dados do aluno selecionado
        item = self.tree.item(selected[0])
        valores = item['values']
        
        dados_aluno = {
            'id': valores[0],
            'nome': valores[1],
            'cpf': valores[2],
            'data_nasc': valores[3],
            'turma': valores[4]
        }
        
        self.abrir_formulario(modo='editar', dados=dados_aluno)
    
    def remover(self):
        """Remover aluno selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um aluno para remover!")
            return
        
        item = self.tree.item(selected[0])
        valores = item['values']
        aluno_id = valores[0]
        aluno_nome = valores[1]
        
        # Confirmar remoção
        resposta = messagebox.askyesno(
            "Confirmar Remoção", 
            f"Deseja realmente remover o aluno '{aluno_nome}'?\n\n"
            "Esta ação não pode ser desfeita!"
        )
        
        if resposta:
            """
            TODO: Remover do banco de dados
            
            Exemplo SQLAlchemy:
            
            from database.connection import DatabaseConnection
            from database.models import Aluno
            
            session = DatabaseConnection.get_session()
            try:
                aluno = session.query(Aluno).filter_by(id=aluno_id).first()
                
                if aluno:
                    session.delete(aluno)
                    session.commit()
                    messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
                    self.carregar_dados()
                
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Erro ao remover: {str(e)}")
            finally:
                session.close()
            
            
            Exemplo psycopg2:
            
            from database.connection import DatabaseConnection
            
            conn = DatabaseConnection.get_psycopg2_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("DELETE FROM alunos WHERE id = %s", (aluno_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
                self.carregar_dados()
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Erro ao remover: {str(e)}")
            finally:
                cursor.close()
                conn.close()
            """
            
            messagebox.showinfo("Sucesso", 
                f"Aluno '{aluno_nome}' removido!\n(Implementar remoção no banco)")
            self.tree.delete(selected[0])
    
    def abrir_formulario(self, modo='novo', dados=None):
        """
        Abrir janela de formulário para cadastro/edição
        
        Args:
            modo: 'novo' ou 'editar'
            dados: dicionário com dados do aluno (apenas para edição)
        """
        
        # Criar janela de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Nota" if modo == 'novo' else "Editar Nota")
        dialog.geometry("550x700")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)
        
        # Centralizar janela
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Frame principal (sem canvas, aumentamos a janela)
        main_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        titulo = "Cadastrar Novo Aluno" if modo == 'novo' else f"Editar Aluno #{dados['id']}"
        tk.Label(main_frame, text=titulo, 
                font=('Arial', 16, 'bold'), bg='white', fg='#2196F3').pack(pady=15)
        
        # Frame do formulário
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(pady=10, fill='both', expand=True)
        
        # ========== CAMPO: Nome Completo ==========
        tk.Label(form_frame, text="Nome Completo: *", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=0, column=0, sticky='w', pady=12)
        
        nome_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        nome_entry.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # ========== CAMPO: CPF ==========
        tk.Label(form_frame, text="CPF: *", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=2, column=0, sticky='w', pady=12)
        
        cpf_frame = tk.Frame(form_frame, bg='white')
        cpf_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        
        cpf_entry = tk.Entry(cpf_frame, font=('Arial', 11), width=20)
        cpf_entry.pack(side='left')
        
        tk.Label(cpf_frame, text="(Ex: 123.456.789-00)", 
                font=('Arial', 9, 'italic'), bg='white', fg='#666').pack(side='left', padx=10)
        
        # ========== CAMPO: Data de Nascimento ==========
        tk.Label(form_frame, text="Data de Nascimento: *", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=4, column=0, sticky='w', pady=12)
        
        data_frame = tk.Frame(form_frame, bg='white')
        data_frame.grid(row=5, column=0, sticky='ew', pady=(0, 10))
        
        # Dia
        tk.Label(data_frame, text="Dia:", font=('Arial', 10), bg='white').pack(side='left')
        dia_var = tk.StringVar()
        dia_combo = ttk.Combobox(data_frame, textvariable=dia_var, width=5, 
                                 values=[str(i).zfill(2) for i in range(1, 32)], 
                                 state='readonly', font=('Arial', 10))
        dia_combo.pack(side='left', padx=5)
        
        # Mês
        tk.Label(data_frame, text="Mês:", font=('Arial', 10), bg='white').pack(side='left', padx=(10, 0))
        mes_var = tk.StringVar()
        mes_combo = ttk.Combobox(data_frame, textvariable=mes_var, width=5,
                                 values=[str(i).zfill(2) for i in range(1, 13)],
                                 state='readonly', font=('Arial', 10))
        mes_combo.pack(side='left', padx=5)
        
        # Ano
        tk.Label(data_frame, text="Ano:", font=('Arial', 10), bg='white').pack(side='left', padx=(10, 0))
        ano_var = tk.StringVar()
        anos = [str(i) for i in range(2000, 2020)]
        ano_combo = ttk.Combobox(data_frame, textvariable=ano_var, width=7,
                                 values=anos, state='readonly', font=('Arial', 10))
        ano_combo.pack(side='left', padx=5)
        
        # ========== CAMPO: Turma ==========
        tk.Label(form_frame, text="Turma:", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=6, column=0, sticky='w', pady=12)
        
        # TODO: Carregar turmas do banco de dados
        turmas = ["Selecione...", "1º Ano A", "1º Ano B", "2º Ano A", "2º Ano B", "3º Ano A"]
        turma_var = tk.StringVar(value=turmas[0])
        turma_combo = ttk.Combobox(form_frame, textvariable=turma_var,
                                   values=turmas, font=('Arial', 11),
                                   width=33, state='readonly')
        turma_combo.grid(row=7, column=0, sticky='ew', pady=(0, 10))
        
        # ========== CAMPO: Endereço (Opcional) ==========
        tk.Label(form_frame, text="Endereço: (opcional)", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=8, column=0, sticky='w', pady=12)
        
        endereco_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        endereco_entry.grid(row=9, column=0, sticky='ew', pady=(0, 10))
        
        # ========== CAMPO: Telefone (Opcional) ==========
        tk.Label(form_frame, text="Telefone: (opcional)", font=('Arial', 11, 'bold'), 
                bg='white', fg='#333').grid(row=10, column=0, sticky='w', pady=12)
        
        telefone_frame = tk.Frame(form_frame, bg='white')
        telefone_frame.grid(row=11, column=0, sticky='ew', pady=(0, 10))
        
        telefone_entry = tk.Entry(telefone_frame, font=('Arial', 11), width=20)
        telefone_entry.pack(side='left')
        
        tk.Label(telefone_frame, text="(Ex: (85) 99999-9999)", 
                font=('Arial', 9, 'italic'), bg='white', fg='#666').pack(side='left', padx=10)
        
        # Preencher campos se for edição
        if modo == 'editar' and dados:
            nome_entry.insert(0, dados['nome'])
            cpf_entry.insert(0, dados['cpf'])
            
            # Preencher data
            if dados['data_nasc']:
                try:
                    partes = dados['data_nasc'].split('/')
                    dia_var.set(partes[0])
                    mes_var.set(partes[1])
                    ano_var.set(partes[2])
                except:
                    pass
            
            if dados['turma']:
                turma_var.set(dados['turma'])
        
        # Nota de campos obrigatórios
        tk.Label(main_frame, text="* Campos obrigatórios", 
                font=('Arial', 9, 'italic'), bg='white', fg='#666').pack(pady=(10, 5))
        
        # Frame de botões
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=15)
        
        # ========== FUNÇÃO: Salvar ==========
        def salvar():
            # Validar campos
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()
            dia = dia_var.get()
            mes = mes_var.get()
            ano = ano_var.get()
            turma = turma_var.get()
            endereco = endereco_entry.get().strip()
            telefone = telefone_entry.get().strip()
            
            # Validações
            if not nome:
                messagebox.showerror("Erro", "O campo Nome é obrigatório!")
                nome_entry.focus()
                return
            
            if not cpf:
                messagebox.showerror("Erro", "O campo CPF é obrigatório!")
                cpf_entry.focus()
                return
            
            if not dia or not mes or not ano:
                messagebox.showerror("Erro", "A Data de Nascimento é obrigatória!")
                return
            
            # Validar formato de data
            try:
                data_nascimento = f"{dia}/{mes}/{ano}"
                datetime.strptime(data_nascimento, '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida!")
                return
            
            # Validar CPF (formato básico)
            if len(cpf.replace('.', '').replace('-', '')) != 11:
                messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
                cpf_entry.focus()
                return
            
            if modo == 'novo':
                """
                TODO: Inserir no banco de dados
                
                Exemplo SQLAlchemy:
                
                from database.connection import DatabaseConnection
                from database.models import Aluno, Turma
                from datetime import datetime
                
                session = DatabaseConnection.get_session()
                try:
                    # Buscar ID da turma
                    turma_id = None
                    if turma != "Selecione...":
                        turma_obj = session.query(Turma).filter_by(nome=turma).first()
                        if turma_obj:
                            turma_id = turma_obj.id
                    
                    # Converter data
                    data_obj = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                    
                    # Criar novo aluno
                    novo_aluno = Aluno(
                        nome=nome,
                        cpf=cpf,
                        data_nascimento=data_obj,
                        turma_id=turma_id
                    )
                    
                    session.add(novo_aluno)
                    session.commit()
                    
                    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                    dialog.destroy()
                    self.carregar_dados()
                    
                except Exception as e:
                    session.rollback()
                    messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
                finally:
                    session.close()
                
                
                Exemplo psycopg2:
                
                from database.connection import DatabaseConnection
                
                conn = DatabaseConnection.get_psycopg2_connection()
                cursor = conn.cursor()
                
                try:
                    # Buscar ID da turma
                    turma_id = None
                    if turma != "Selecione...":
                        cursor.execute("SELECT id FROM turmas WHERE nome = %s", (turma,))
                        result = cursor.fetchone()
                        if result:
                            turma_id = result[0]
                    
                    # Converter data para formato SQL
                    from datetime import datetime
                    data_obj = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                    
                    # Inserir aluno
                    cursor.execute('''
                        INSERT INTO alunos (nome, cpf, data_nascimento, turma_id)
                        VALUES (%s, %s, %s, %s)
                    ''', (nome, cpf, data_obj, turma_id))
                    
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                    dialog.destroy()
                    self.carregar_dados()
                    
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
                """
                
                messagebox.showinfo("Sucesso", 
                    f"Aluno '{nome}' cadastrado!\n(Implementar salvamento no banco)")
                dialog.destroy()
                self.carregar_dados()
                
            else:  # modo == 'editar'
                """
                TODO: Atualizar no banco de dados
                
                Exemplo SQLAlchemy:
                
                from database.connection import DatabaseConnection
                from database.models import Aluno, Turma
                from datetime import datetime
                
                session = DatabaseConnection.get_session()
                try:
                    aluno = session.query(Aluno).filter_by(id=dados['id']).first()
                    
                    if aluno:
                        # Buscar ID da turma
                        turma_id = None
                        if turma != "Selecione...":
                            turma_obj = session.query(Turma).filter_by(nome=turma).first()
                            if turma_obj:
                                turma_id = turma_obj.id
                        
                        # Converter data
                        data_obj = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                        
                        # Atualizar campos
                        aluno.nome = nome
                        aluno.cpf = cpf
                        aluno.data_nascimento = data_obj
                        aluno.turma_id = turma_id
                        
                        session.commit()
                        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                        dialog.destroy()
                        self.carregar_dados()
                    
                except Exception as e:
                    session.rollback()
                    messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
                finally:
                    session.close()
                
                
                Exemplo psycopg2:
                
                from database.connection import DatabaseConnection
                
                conn = DatabaseConnection.get_psycopg2_connection()
                cursor = conn.cursor()
                
                try:
                    # Buscar ID da turma
                    turma_id = None
                    if turma != "Selecione...":
                        cursor.execute("SELECT id FROM turmas WHERE nome = %s", (turma,))
                        result = cursor.fetchone()
                        if result:
                            turma_id = result[0]
                    
                    # Converter data
                    from datetime import datetime
                    data_obj = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                    
                    # Atualizar aluno
                    cursor.execute('''
                        UPDATE alunos 
                        SET nome = %s, cpf = %s, data_nascimento = %s, turma_id = %s
                        WHERE id = %s
                    ''', (nome, cpf, data_obj, turma_id, dados['id']))
                    
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                    dialog.destroy()
                    self.carregar_dados()
                    
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
                """
                
                messagebox.showinfo("Sucesso", 
                    f"Aluno '{nome}' atualizado!\n(Implementar atualização no banco)")
                dialog.destroy()
                self.carregar_dados()
        
        # Botão Salvar
        cor_botao = '#4CAF50' if modo == 'novo' else '#FF9800'
        texto_botao = 'Cadastrar' if modo == 'novo' else 'Salvar Alterações'
        
        tk.Button(btn_frame, text=texto_botao, font=('Arial', 12, 'bold'),
                 bg=cor_botao, fg='white', width=18, height=2,
                 command=salvar, cursor='hand2').grid(row=0, column=0, padx=5)
        
        # Botão Cancelar
        tk.Button(btn_frame, text="Cancelar", font=('Arial', 12),
                 bg='#757575', fg='white', width=18, height=2,
                 command=dialog.destroy, cursor='hand2').grid(row=0, column=1, padx=5)
    
    def voltar(self):
        self.frame.destroy()
        # IMPORTAÇÃO LOCAL
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)