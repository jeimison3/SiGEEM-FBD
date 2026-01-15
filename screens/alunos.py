# ============================================================
# Arquivo: screens/alunos.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database.connection import DatabaseConnection
from database.models import Aluno, Usuario


class AlunosScreen:
    def __init__(self, root, username, extra):
        self.root = root
        self.username = username
        self.extra = extra
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)

        self.create_widgets()
        self.carregar_dados()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#2196F3', height=60)
        header.pack(fill='x')

        tk.Label(
            header,
            text="Gerenciamento de Alunos",
            font=('Arial', 16, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(side='left', padx=20, pady=15)

        back_btn = tk.Button(
            header,
            text="← Voltar",
            font=('Arial', 10),
            bg='#1976D2',
            fg='white',
            command=self.voltar,
            cursor='hand2',
            padx=15
        )
        back_btn.pack(side='right', padx=20)

        # Botões de ação
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Novo",
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.novo,
            cursor='hand2'
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Editar",
            font=('Arial', 11, 'bold'),
            bg='#FF9800',
            fg='white',
            width=12,
            command=self.editar,
            cursor='hand2'
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Remover",
            font=('Arial', 11, 'bold'),
            bg='#F44336',
            fg='white',
            width=12,
            command=self.remover,
            cursor='hand2'
        ).grid(row=0, column=2, padx=5)

        # Treeview
        tree_frame = tk.Frame(self.frame, bg='white')
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')

        # Colunas ajustadas ao modelo:
        # Aluno: id_aluno, matricula, nome_completo, data_nascimento, telefone_responsavel,
        #       ano_letivo, email, id_usuario(oculta)
        # Usuario: cpf (exibimos), senha (não exibimos)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Matrícula', 'Nome', 'CPF', 'Data Nasc', 'Tel. Resp', 'Ano Letivo', 'Email', 'ID_Usuario'),
            show='headings',
            yscrollcommand=scrollbar.set
        )

        self.tree.heading('ID', text='ID')
        self.tree.heading('Matrícula', text='Matrícula')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Data Nasc', text='Data Nascimento')
        self.tree.heading('Tel. Resp', text='Telefone Resp.')
        self.tree.heading('Ano Letivo', text='Ano Letivo')
        self.tree.heading('Email', text='Email')
        self.tree.heading('ID_Usuario', text='ID Usuário')

        self.tree.column('ID', width=60)
        self.tree.column('Matrícula', width=110)
        self.tree.column('Nome', width=220)
        self.tree.column('CPF', width=140)
        self.tree.column('Data Nasc', width=110)
        self.tree.column('Tel. Resp', width=140)
        self.tree.column('Ano Letivo', width=90)
        self.tree.column('Email', width=220)

        # Ocultar coluna interna
        self.tree.column('ID_Usuario', width=0, stretch=False)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)

    def carregar_dados(self):
        session = DatabaseConnection.get_session()
        try:
            alunos = session.query(Aluno).all()

            # Limpar árvore
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Preencher com dados do banco
            for aluno in alunos:
                cpf = ""
                if getattr(aluno, "usuario", None):
                    cpf = aluno.usuario.cpf or ""

                data_nasc = ""
                if aluno.data_nascimento:
                    try:
                        data_nasc = aluno.data_nascimento.strftime('%d/%m/%Y')
                    except Exception:
                        data_nasc = ""

                ano_letivo = aluno.ano_letivo if aluno.ano_letivo is not None else ""

                self.tree.insert('', 'end', values=(
                    aluno.id_aluno,
                    aluno.matricula or "",
                    aluno.nome_completo,
                    cpf,
                    data_nasc,
                    aluno.telefone_responsavel,
                    ano_letivo,
                    aluno.email or "",
                    aluno.id_usuario  # coluna oculta
                ))
        finally:
            session.close()

    def novo(self):
        """Abrir formulário para cadastrar novo aluno"""
        self.abrir_formulario(modo='novo')

    def editar(self):
        """Abrir formulário para editar aluno selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar!")
            return

        item = self.tree.item(selected[0])
        valores = item['values']

        # valores = (id_aluno, matricula, nome, cpf, data_nasc, tel_resp, ano_letivo, email, id_usuario)
        dados_aluno = {
            'id_aluno': valores[0],
            'matricula': valores[1],
            'nome_completo': valores[2],
            'cpf': valores[3],
            'data_nasc': valores[4],
            'telefone_responsavel': valores[5],
            'ano_letivo': valores[6],
            'email': valores[7],
            'id_usuario': valores[8],
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
        aluno_nome = valores[2]
        id_usuario = valores[8]

        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Deseja realmente remover o aluno '{aluno_nome}'?\n\n"
            "Esta ação não pode ser desfeita!"
        )

        if not resposta:
            return

        session = DatabaseConnection.get_session()
        try:
            aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
            if not aluno:
                messagebox.showwarning("Aviso", "Aluno não encontrado no banco!")
                return

            session.delete(aluno)

            if id_usuario:
                user = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
                if user:
                    session.delete(user)

            session.commit()
            messagebox.showinfo("Sucesso", f"Aluno '{aluno_nome}' removido!")
            self.carregar_dados()

        except IntegrityError:
            session.rollback()
            messagebox.showerror(
                "Erro",
                "Não foi possível remover. Verifique vínculos/constraints no banco."
            )
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Falha ao remover: {e}")
        finally:
            session.close()

    def abrir_formulario(self, modo='novo', dados=None):
        """
        Abrir janela de formulário para cadastro/edição

        Args:
            modo: 'novo' ou 'editar'
            dados: dicionário com dados do aluno (apenas para edição)
        """

        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Aluno" if modo == 'novo' else "Editar Aluno")
        dialog.geometry("420x880")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)

        # Centralizar janela
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        main_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        aluno_id = dados['id_aluno'] if (modo == 'editar' and dados) else None
        id_usuario_atual = dados['id_usuario'] if (modo == 'editar' and dados) else None

        titulo = "Cadastrar Novo Aluno" if modo == 'novo' else f"Editar Aluno #{aluno_id}"
        tk.Label(main_frame,text=titulo,font=('Arial', 16, 'bold'),bg='white',fg='#2196F3').pack(pady=15)

        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(pady=10, fill='both', expand=True)

        # ========== CAMPO: Matrícula ==========
        tk.Label(form_frame,text="Matrícula: (opcional)",font=('Arial', 11, 'bold'),bg='white',fg='#333').grid(row=0, column=0, sticky='w', pady=12)

        matricula_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        matricula_entry.grid(row=1, column=0, sticky='ew', pady=(0, 10))

        # ========== CAMPO: Nome Completo ==========
        tk.Label(
            form_frame,
            text="Nome Completo: *",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=2, column=0, sticky='w', pady=12)

        nome_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        nome_entry.grid(row=3, column=0, sticky='ew', pady=(0, 10))

        # ========== CAMPO: CPF (Usuario) ==========
        tk.Label(
            form_frame,
            text="CPF (Usuário): *",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=4, column=0, sticky='w', pady=12)

        cpf_frame = tk.Frame(form_frame, bg='white')
        cpf_frame.grid(row=5, column=0, sticky='ew', pady=(0, 10))

        cpf_entry = tk.Entry(cpf_frame, font=('Arial', 11), width=20)
        cpf_entry.pack(side='left')

        tk.Label(
            cpf_frame,
            text="(Ex: 123.456.789-00)",
            font=('Arial', 9, 'italic'),
            bg='white',
            fg='#666'
        ).pack(side='left', padx=10)

        # ========== CAMPO: Senha (Usuario) ==========
        senha_label_text = "Senha (Usuário): *" if modo == 'novo' else "Senha (Usuário) [deixe em branco para manter]:"
        tk.Label(
            form_frame,
            text=senha_label_text,
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=6, column=0, sticky='w', pady=12)

        senha_entry = tk.Entry(form_frame, font=('Arial', 11), width=35, show="*")
        senha_entry.grid(row=7, column=0, sticky='ew', pady=(0, 10))

        # ========== CAMPO: Data de Nascimento ==========
        tk.Label(
            form_frame,
            text="Data de Nascimento: *",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=8, column=0, sticky='w', pady=12)

        data_frame = tk.Frame(form_frame, bg='white')
        data_frame.grid(row=9, column=0, sticky='ew', pady=(0, 10))

        tk.Label(data_frame, text="Dia:", font=('Arial', 10), bg='white').pack(side='left')
        dia_var = tk.StringVar()
        dia_combo = ttk.Combobox(
            data_frame,
            textvariable=dia_var,
            width=5,
            values=[str(i).zfill(2) for i in range(1, 32)],
            state='readonly',
            font=('Arial', 10)
        )
        dia_combo.pack(side='left', padx=5)

        tk.Label(data_frame, text="Mês:", font=('Arial', 10), bg='white').pack(side='left', padx=(10, 0))
        mes_var = tk.StringVar()
        mes_combo = ttk.Combobox(
            data_frame,
            textvariable=mes_var,
            width=5,
            values=[str(i).zfill(2) for i in range(1, 13)],
            state='readonly',
            font=('Arial', 10)
        )
        mes_combo.pack(side='left', padx=5)

        tk.Label(data_frame, text="Ano:", font=('Arial', 10), bg='white').pack(side='left', padx=(10, 0))
        ano_var = tk.StringVar()
        anos = [str(i) for i in range(2000, 2020)]
        ano_combo = ttk.Combobox(
            data_frame,
            textvariable=ano_var,
            width=7,
            values=anos,
            state='readonly',
            font=('Arial', 10)
        )
        ano_combo.pack(side='left', padx=5)

        # ========== CAMPO: Telefone Responsável ==========
        tk.Label(
            form_frame,
            text="Telefone do Responsável: *",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=10, column=0, sticky='w', pady=12)

        tel_frame = tk.Frame(form_frame, bg='white')
        tel_frame.grid(row=11, column=0, sticky='ew', pady=(0, 10))

        tel_resp_entry = tk.Entry(tel_frame, font=('Arial', 11), width=20)
        tel_resp_entry.pack(side='left')

        tk.Label(
            tel_frame,
            text="(Ex: (85) 99999-9999)",
            font=('Arial', 9, 'italic'),
            bg='white',
            fg='#666'
        ).pack(side='left', padx=10)

        # ========== CAMPO: Ano Letivo (opcional) ==========
        tk.Label(
            form_frame,
            text="Ano Letivo: (opcional)",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=12, column=0, sticky='w', pady=12)

        ano_letivo_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        ano_letivo_entry.grid(row=13, column=0, sticky='ew', pady=(0, 10))

        # ========== CAMPO: Email (opcional, mas UNIQUE) ==========
        tk.Label(
            form_frame,
            text="Email: (opcional)",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).grid(row=14, column=0, sticky='w', pady=12)

        email_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        email_entry.grid(row=15, column=0, sticky='ew', pady=(0, 10))

        # Preencher campos se for edição
        if modo == 'editar' and dados:
            matricula_entry.insert(0, dados.get('matricula') or "")
            nome_entry.insert(0, dados.get('nome_completo') or "")
            cpf_entry.insert(0, dados.get('cpf') or "")

            # Preencher data
            if dados.get('data_nasc'):
                try:
                    partes = str(dados['data_nasc']).split('/')
                    dia_var.set(partes[0])
                    mes_var.set(partes[1])
                    ano_var.set(partes[2])
                except Exception:
                    pass

            tel_resp_entry.insert(0, dados.get('telefone_responsavel') or "")
            if dados.get('ano_letivo') not in (None, ""):
                ano_letivo_entry.insert(0, str(dados.get('ano_letivo')))
            email_entry.insert(0, dados.get('email') or "")

        tk.Label(
            main_frame,
            text="* Campos obrigatórios",
            font=('Arial', 9, 'italic'),
            bg='white',
            fg='#666'
        ).pack(pady=(10, 5))

        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=15)

        def salvar():
            nome = nome_entry.get().strip()
            cpf = cpf_entry.get().strip()
            senha = senha_entry.get().strip()

            dia = dia_var.get()
            mes = mes_var.get()
            ano = ano_var.get()

            matricula = matricula_entry.get().strip() or None
            telefone_responsavel = tel_resp_entry.get().strip()
            ano_letivo_raw = ano_letivo_entry.get().strip()
            email = email_entry.get().strip() or None

            if not nome:
                messagebox.showerror("Erro", "O campo Nome é obrigatório!")
                nome_entry.focus()
                return

            if not cpf:
                messagebox.showerror("Erro", "O campo CPF é obrigatório!")
                cpf_entry.focus()
                return

            if modo == 'novo' and not senha:
                messagebox.showerror("Erro", "A senha é obrigatória para novo usuário!")
                senha_entry.focus()
                return

            if not dia or not mes or not ano:
                messagebox.showerror("Erro", "A Data de Nascimento é obrigatória!")
                return

            # Data
            try:
                data_nascimento_str = f"{dia}/{mes}/{ano}"
                data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').date()
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida!")
                return

            if len(cpf.replace('.', '').replace('-', '')) != 11:
                messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
                cpf_entry.focus()
                return

            if not telefone_responsavel:
                messagebox.showerror("Erro", "Telefone do responsável é obrigatório!")
                tel_resp_entry.focus()
                return

            # ano_letivo opcional
            ano_letivo = None
            if ano_letivo_raw:
                try:
                    ano_letivo = int(ano_letivo_raw)
                except ValueError:
                    messagebox.showerror("Erro", "Ano letivo deve ser um número inteiro!")
                    ano_letivo_entry.focus()
                    return

            session = DatabaseConnection.get_session()
            try:
                if modo == 'novo':
                    # Criar Usuario primeiro
                    import bcrypt
                    salt = bcrypt.gensalt()
                    novo_user = Usuario(cpf=cpf, senha=bcrypt.hashpw(str(senha).encode("utf-8"), salt))
                    session.add(novo_user)
                    session.flush()  # garante id_usuario

                    novo_aluno = Aluno(
                        matricula=matricula,
                        nome_completo=nome,
                        data_nascimento=data_nascimento,
                        telefone_responsavel=telefone_responsavel,
                        ano_letivo=ano_letivo,
                        email=email,
                        id_usuario=novo_user.id_usuario
                    )
                    session.add(novo_aluno)

                    session.commit()
                    messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado!")
                    dialog.destroy()
                    self.carregar_dados()

                else:
                    # Editar Aluno e Usuario
                    aluno = session.query(Aluno).filter_by(id_aluno=aluno_id).first()
                    if not aluno:
                        messagebox.showerror("Erro", "Aluno não encontrado no banco!")
                        return

                    user = session.query(Usuario).filter_by(id_usuario=aluno.id_usuario).first()
                    if not user:
                        messagebox.showerror("Erro", "Usuário do aluno não encontrado!")
                        return

                    aluno.matricula = matricula
                    aluno.nome_completo = nome
                    aluno.data_nascimento = data_nascimento
                    aluno.telefone_responsavel = telefone_responsavel
                    aluno.ano_letivo = ano_letivo
                    aluno.email = email

                    user.cpf = cpf
                    if senha:  # opcional no editar
                        import bcrypt
                        salt = bcrypt.gensalt()
                        user.senha = bcrypt.hashpw(str(senha).encode("utf-8"), salt)

                    session.commit()
                    messagebox.showinfo("Sucesso", f"Aluno '{nome}' atualizado!")
                    dialog.destroy()
                    self.carregar_dados()

            except IntegrityError:
                session.rollback()
                messagebox.showerror(
                    "Erro",
                    "Violação de unicidade/constraint (CPF, matrícula ou email já existe, ou usuário já vinculado)."
                )
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Falha ao salvar: {e}")
            finally:
                session.close()

        cor_botao = '#4CAF50' if modo == 'novo' else '#FF9800'
        texto_botao = 'Cadastrar' if modo == 'novo' else 'Salvar Alterações'

        tk.Button(
            btn_frame,
            text=texto_botao,
            font=('Arial', 12, 'bold'),
            bg=cor_botao,
            fg='white',
            width=18,
            height=2,
            command=salvar,
            cursor='hand2'
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Cancelar",
            font=('Arial', 12),
            bg='#757575',
            fg='white',
            width=18,
            height=2,
            command=dialog.destroy,
            cursor='hand2'
        ).grid(row=0, column=1, padx=5)

    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username, self.extra)
