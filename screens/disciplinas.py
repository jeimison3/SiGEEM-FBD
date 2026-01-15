import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_turmas, get_avaliacoes, add_avaliacao, delete_avaliacao, get_disciplinas, get_professores
from datetime import datetime


class AvaliacoesScreen:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        # Carregar turmas, disciplinas e professores
        try:
            turmas = get_turmas()
            self.turmas_disponiveis = [t['nome'] for t in turmas]
            self.turmas_ids = {t['nome']: t['id_turma'] for t in turmas}
        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")
            self.turmas_disponiveis = []
            self.turmas_ids = {}

        try:
            disciplinas = get_disciplinas()
            self.disciplinas_disponiveis = [d['nome_disciplina'] for d in disciplinas]
            self.disciplinas_ids = {d['nome_disciplina']: d['id_disciplina'] for d in disciplinas}
        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")
            self.disciplinas_disponiveis = []
            self.disciplinas_ids = {}

        try:
            professores = get_professores()
            self.professores_disponiveis = [p['nome_completo'] for p in professores]
            self.professores_ids = {p['nome_completo']: p['id_professor'] for p in professores}
        except Exception as e:
            print(f"Erro ao carregar professores: {e}")
            self.professores_disponiveis = []
            self.professores_ids = {}

        try:
            self.dados_avaliacoes = get_avaliacoes()
        except Exception as e:
            print(f"Erro ao carregar avaliações: {e}")
            import traceback
            traceback.print_exc()
            self.dados_avaliacoes = []

        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)

        self.create_widgets()
        self.carregar_dados()

    def create_widgets(self):
        # Header (Cor Vinho/Borgonha para diferenciar das outras telas)
        header = tk.Frame(self.frame, bg='#AC2B41', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="Gestão de Avaliações", font=('Arial', 14, 'bold'), 
                 bg='#AC2B41', fg='white').pack(side='left', padx=20, pady=15)

        # Botão Voltar para o Dashboard
        tk.Button(header, text="← Voltar", bg='#822031', fg='white', 
                  command=self.voltar, cursor='hand2', padx=15).pack(side='right', padx=20)

        # 1) CONSULTA/FILTRAGEM (1,5 pts)
        search_frame = tk.Frame(self.frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="🔍 Filtrar Avaliação:", bg='#f0f0f0').pack(side='left')
        self.ent_filtro = tk.Entry(search_frame)
        self.ent_filtro.pack(side='left', padx=5, expand=True, fill='x')
        self.ent_filtro.bind('<KeyRelease>', lambda e: self.carregar_dados())

        # Botões de Ação (INCLUSÃO, EDIÇÃO, REMOÇÃO)
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="➕ Nova", bg='#4CAF50', fg='white', width=12,
                  command=self.novo).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="✏️ Editar", bg='#FF9800', fg='white', width=12,
                  command=self.preparar_edicao).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ Remover", bg='#F44336', fg='white', width=12,
                  command=self.remover).pack(side='left', padx=5)

        # Tabela (Treeview)
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Titulo', 'Turma'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Titulo', text='Título da Prova')
        self.tree.heading('Turma', text='Turma')
        self.tree.pack(padx=20, pady=10, fill='both', expand=True)

    def carregar_dados(self):
        """Lógica de Consulta/Filtro"""
        for i in self.tree.get_children(): self.tree.delete(i)
        filtro = self.ent_filtro.get().lower()
        for a in self.dados_avaliacoes:
            if filtro in a['nome'].lower():
                self.tree.insert('', 'end', values=(a['id'], a['nome'], a['turma']))

    def novo(self):
        """Inclusão - Abre formulário se houver turmas"""
        if not self.turmas_disponiveis:
            messagebox.showwarning("Atenção", "Cadastre uma TURMA primeiro no menu de Turmas!")
            return
        self.abrir_formulario()

    def preparar_edicao(self):
        """Edição - Verifica seleção"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma avaliação para editar!")
            return
        valores = self.tree.item(sel)['values']
        self.abrir_formulario(editar=True, dados_atuais=valores)

    def abrir_formulario(self, editar=False, dados_atuais=None):
        janela_form = tk.Toplevel(self.root)
        janela_form.title("Nova Avaliação" if not editar else "Editar Avaliação")
        janela_form.geometry("400x500")
        janela_form.grab_set()

        tk.Label(janela_form, text="Nome da Avaliação:").pack(pady=5)
        ent_nome = tk.Entry(janela_form)
        ent_nome.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Data de Aplicação (YYYY-MM-DD):").pack(pady=5)
        ent_data = tk.Entry(janela_form)
        ent_data.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Quanto Vale:").pack(pady=5)
        ent_quanto = tk.Entry(janela_form)
        ent_quanto.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Peso:").pack(pady=5)
        ent_peso = tk.Entry(janela_form)
        ent_peso.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Disciplina:").pack(pady=5)
        cb_disciplina = ttk.Combobox(janela_form, values=self.disciplinas_disponiveis, state="readonly")
        cb_disciplina.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Turma:").pack(pady=5)
        cb_turma = ttk.Combobox(janela_form, values=self.turmas_disponiveis, state="readonly")
        cb_turma.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Professor:").pack(pady=5)
        cb_professor = ttk.Combobox(janela_form, values=self.professores_disponiveis, state="readonly")
        cb_professor.pack(padx=20, fill='x')

        if editar:
            ent_nome.insert(0, dados_atuais[1])
            cb_turma.set(dados_atuais[2])

        def salvar():
            nome = ent_nome.get()
            data = ent_data.get()
            quanto_vale = ent_quanto.get()
            peso = ent_peso.get()
            disciplina = cb_disciplina.get()
            turma = cb_turma.get()
            professor = cb_professor.get()

            if not (nome and disciplina and turma and professor):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return

            try:
                quanto_vale = float(quanto_vale) if quanto_vale else None
                peso = float(peso) if peso else None
            except ValueError:
                messagebox.showerror("Erro", "Quanto Vale e Peso devem ser números!")
                return

            try:
                id_disciplina = self.disciplinas_ids.get(disciplina)
                id_turma = self.turmas_ids.get(turma)
                id_professor = self.professores_ids.get(professor)

                if editar:
                    messagebox.showinfo("Aviso", "Edição não implementada ainda.")
                else:
                    nid = add_avaliacao(nome, data or None, quanto_vale, peso, id_disciplina, id_turma, id_professor)
                    messagebox.showinfo("Sucesso", f"Avaliação cadastrada (id={nid})")
                    self.dados_avaliacoes = get_avaliacoes()

            except Exception as e:
                messagebox.showerror("Erro ao salvar", f"Erro: {str(e)}")
                import traceback
                traceback.print_exc()

            self.carregar_dados()
            janela_form.destroy()

        tk.Button(janela_form, text="Confirmar", bg='#2196F3', fg='white', 
                  command=salvar).pack(pady=20)

    def remover(self):
        """Remoção"""
        sel = self.tree.selection()
        if sel and messagebox.askyesno("Confirmar", "Deseja excluir esta avaliação?"):
            id_rem = self.tree.item(sel)['values'][0]
            try:
                delete_avaliacao(id_rem)
                messagebox.showinfo("Sucesso", "Avaliação removida do banco!")
                self.dados_avaliacoes = [a for a in self.dados_avaliacoes if a['id'] != id_rem]
            except Exception:
                self.dados_avaliacoes = [a for a in self.dados_avaliacoes if a['id'] != id_rem]
                messagebox.showwarning("Atenção", "Removida localmente; erro ao remover do DB.")
            self.carregar_dados()

    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username)
