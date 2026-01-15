# ============================================================
# Arquivo: screens/notas.py
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import DatabaseConnection
from database.models import Nota, Turma, Aluno, Disciplina, Professor, Avaliacao


class NotasScreen:
    def __init__(self, root, username, extra):
        self.root = root
        self.username = username
        self.extra = extra
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        self._last_rows = {}

        self.create_widgets()
        self.carregar_dados()

    def create_widgets(self):
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")

        tk.Label(header, text="Gerenciamento de Notas", font=("Arial", 16, "bold"), bg="#2196F3", fg="white").pack(side="left", padx=20, pady=15)

        back_btn = tk.Button(header, text="← Voltar", font=("Arial", 10), bg="#1976D2", fg="white", command=self.voltar, cursor="hand2", padx=15)
        back_btn.pack(side="right", padx=20)

        btn_frame = tk.Frame(self.frame, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Novo", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=12, command=self.novo, cursor="hand2").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", font=("Arial", 11, "bold"), bg="#FF9800", fg="white", width=12, command=self.editar, cursor="hand2").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remover", font=("Arial", 11, "bold"), bg="#F44336", fg="white", width=12, command=self.remover, cursor="hand2").grid(row=0, column=2, padx=5)

        tree_frame = tk.Frame(self.frame, bg="white")
        tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, columns=("TurmaNome", "NomeAluno", "DisciNome", "ProfeNome", "Avali", "Nota"), show="headings", yscrollcommand=scrollbar.set)

        self.tree.heading("TurmaNome", text="Turma")
        self.tree.heading("NomeAluno", text="Aluno")
        self.tree.heading("DisciNome", text="Disciplina")
        self.tree.heading("ProfeNome", text="Professor")
        self.tree.heading("Avali", text="Avaliação")
        self.tree.heading("Nota", text="Nota")

        self.tree.column("TurmaNome", width=80)
        self.tree.column("NomeAluno", width=220)
        self.tree.column("DisciNome", width=160)
        self.tree.column("ProfeNome", width=180)
        self.tree.column("Avali", width=180)
        self.tree.column("Nota", width=80)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

    def carregar_dados(self):
        session = DatabaseConnection.get_session()
        try:
            notas = session.query(Nota).join(Nota.turma).join(Nota.aluno).join(Nota.disciplina).join(Nota.professor).join(Nota.avaliacao).all()

            for item in self.tree.get_children():
                self.tree.delete(item)

            self._last_rows.clear()

            for n in notas:
                values = (n.turma.nome, n.aluno.nome_completo, n.disciplina.nome_disciplina, n.professor.nome_completo, n.avaliacao.nome_avaliacao, float(n.nota) if n.nota is not None else None)
                iid = self.tree.insert("", "end", values=values)

                self._last_rows[iid] = {
                    "id_turma": n.id_turma,
                    "id_aluno": n.id_aluno,
                    "id_disciplina": n.id_disciplina,
                    "id_professor": n.id_professor,
                    "id_avaliacao": n.id_avaliacao,
                }
        finally:
            session.close()

    def novo(self):
        self.abrir_formulario(modo="novo")

    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma nota para editar!")
            return

        iid = selected[0]
        key = self._last_rows.get(iid)
        if not key:
            messagebox.showerror("Erro", "Não foi possível identificar a nota selecionada.")
            return

        session = DatabaseConnection.get_session()
        try:
            nota_obj = session.query(Nota).filter_by(id_turma=key["id_turma"], id_aluno=key["id_aluno"], id_disciplina=key["id_disciplina"], id_professor=key["id_professor"], id_avaliacao=key["id_avaliacao"]).first()
            if not nota_obj:
                messagebox.showerror("Erro", "Nota não encontrada no banco.")
                return

            dados = {
                "id_turma": nota_obj.id_turma,
                "id_aluno": nota_obj.id_aluno,
                "id_disciplina": nota_obj.id_disciplina,
                "id_professor": nota_obj.id_professor,
                "id_avaliacao": nota_obj.id_avaliacao,
                "nota": float(nota_obj.nota) if nota_obj.nota is not None else None,
                "peso": float(nota_obj.peso) if nota_obj.peso is not None else None,
            }
        finally:
            session.close()

        self.abrir_formulario(modo="editar", dados=dados)

    def remover(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma nota para remover!")
            return

        iid = selected[0]
        key = self._last_rows.get(iid)
        if not key:
            messagebox.showerror("Erro", "Não foi possível identificar a nota selecionada.")
            return

        valores = self.tree.item(iid)["values"]
        aluno_nome = valores[1]
        avali_nome = valores[4]

        resp = messagebox.askyesno("Confirmar Remoção", f"Deseja remover a nota do aluno '{aluno_nome}' na avaliação '{avali_nome}'?\n\nEsta ação não pode ser desfeita!")
        if not resp:
            return

        session = DatabaseConnection.get_session()
        try:
            nota_obj = session.query(Nota).filter_by(id_turma=key["id_turma"], id_aluno=key["id_aluno"], id_disciplina=key["id_disciplina"], id_professor=key["id_professor"], id_avaliacao=key["id_avaliacao"]).first()
            if not nota_obj:
                messagebox.showerror("Erro", "Nota não encontrada no banco.")
                return

            session.delete(nota_obj)
            session.commit()

            messagebox.showinfo("Sucesso", "Nota removida com sucesso!")
            self.carregar_dados()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro ao remover: {str(e)}")
        finally:
            session.close()

    def abrir_formulario(self, modo="novo", dados=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Nota" if modo == "novo" else "Editar Nota")
        dialog.geometry("520x720")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = tk.Frame(dialog, bg="white", padx=24, pady=18)
        main_frame.pack(fill="both", expand=True)

        titulo = "Cadastrar Nova Nota" if modo == "novo" else "Editar Nota"
        tk.Label(main_frame, text=titulo, font=("Arial", 16, "bold"), bg="white", fg="#2196F3").pack(pady=10)

        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(pady=10, fill="both", expand=True)
        form_frame.columnconfigure(0, weight=1)

        session = DatabaseConnection.get_session()
        try:
            turmas_db = session.query(Turma).all()
            alunos_db = session.query(Aluno).all()
            disciplinas_db = session.query(Disciplina).all()
            professores_db = session.query(Professor).all()
            avaliacoes_db = session.query(Avaliacao).all()
        finally:
            session.close()

        turma_map = {f"{t.nome} (#{t.id_turma})": t.id_turma for t in turmas_db}
        aluno_map = {f"{a.nome_completo} (#{a.id_aluno})": a.id_aluno for a in alunos_db}
        disc_map = {f"{d.nome_disciplina} (#{d.id_disciplina})": d.id_disciplina for d in disciplinas_db}
        prof_map = {f"{p.nome_completo} (#{p.id_professor})": p.id_professor for p in professores_db}
        avali_map = {f"{av.nome_avaliacao} (#{av.id_avaliacao})": av.id_avaliacao for av in avaliacoes_db}

        turmas = ["Selecione..."] + list(turma_map.keys())
        alunos = ["Selecione..."] + list(aluno_map.keys())
        disciplinas = ["Selecione..."] + list(disc_map.keys())
        professores = ["Selecione..."] + list(prof_map.keys())
        avaliacoes = ["Selecione..."] + list(avali_map.keys())

        tk.Label(form_frame, text="Turma: *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=0, column=0, sticky="w", pady=(6, 6))
        turma_var = tk.StringVar(value=turmas[0])
        turma_combo = ttk.Combobox(form_frame, textvariable=turma_var, values=turmas, font=("Arial", 11), state="readonly")
        turma_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Aluno: *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=2, column=0, sticky="w", pady=(6, 6))
        aluno_var = tk.StringVar(value=alunos[0])
        aluno_combo = ttk.Combobox(form_frame, textvariable=aluno_var, values=alunos, font=("Arial", 11), state="readonly")
        aluno_combo.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Disciplina: *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=4, column=0, sticky="w", pady=(6, 6))
        disc_var = tk.StringVar(value=disciplinas[0])
        disc_combo = ttk.Combobox(form_frame, textvariable=disc_var, values=disciplinas, font=("Arial", 11), state="readonly")
        disc_combo.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Professor: *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=6, column=0, sticky="w", pady=(6, 6))
        prof_var = tk.StringVar(value=professores[0])
        prof_combo = ttk.Combobox(form_frame, textvariable=prof_var, values=professores, font=("Arial", 11), state="readonly")
        prof_combo.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Avaliação: *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=8, column=0, sticky="w", pady=(6, 6))
        avali_var = tk.StringVar(value=avaliacoes[0])
        avali_combo = ttk.Combobox(form_frame, textvariable=avali_var, values=avaliacoes, font=("Arial", 11), state="readonly")
        avali_combo.grid(row=9, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Nota (0 a 10): *", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=10, column=0, sticky="w", pady=(6, 6))
        nota_entry = tk.Entry(form_frame, font=("Arial", 11))
        nota_entry.grid(row=11, column=0, sticky="ew", pady=(0, 10))

        tk.Label(form_frame, text="Peso (opcional):", font=("Arial", 11, "bold"), bg="white", fg="#333").grid(row=12, column=0, sticky="w", pady=(6, 6))
        peso_entry = tk.Entry(form_frame, font=("Arial", 11))
        peso_entry.grid(row=13, column=0, sticky="ew", pady=(0, 10))

        if modo == "editar" and dados:
            turma_key = next((k for k, v in turma_map.items() if v == dados["id_turma"]), None)
            aluno_key = next((k for k, v in aluno_map.items() if v == dados["id_aluno"]), None)
            disc_key = next((k for k, v in disc_map.items() if v == dados["id_disciplina"]), None)
            prof_key = next((k for k, v in prof_map.items() if v == dados["id_professor"]), None)
            avali_key = next((k for k, v in avali_map.items() if v == dados["id_avaliacao"]), None)

            if turma_key:
                turma_var.set(turma_key)
            if aluno_key:
                aluno_var.set(aluno_key)
            if disc_key:
                disc_var.set(disc_key)
            if prof_key:
                prof_var.set(prof_key)
            if avali_key:
                avali_var.set(avali_key)

            if dados.get("nota") is not None:
                nota_entry.insert(0, str(dados["nota"]))
            if dados.get("peso") is not None:
                peso_entry.insert(0, str(dados["peso"]))

        def _parse_float(value: str, field_name: str, required: bool = False):
            v = value.strip().replace(",", ".")
            if not v:
                if required:
                    raise ValueError(f"O campo {field_name} é obrigatório.")
                return None
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"O campo {field_name} deve ser numérico.")

        def salvar():
            try:
                turma_txt = turma_var.get()
                aluno_txt = aluno_var.get()
                disc_txt = disc_var.get()
                prof_txt = prof_var.get()
                avali_txt = avali_var.get()

                if turma_txt == "Selecione...":
                    raise ValueError("Selecione uma Turma.")
                if aluno_txt == "Selecione...":
                    raise ValueError("Selecione um Aluno.")
                if disc_txt == "Selecione...":
                    raise ValueError("Selecione uma Disciplina.")
                if prof_txt == "Selecione...":
                    raise ValueError("Selecione um Professor.")
                if avali_txt == "Selecione...":
                    raise ValueError("Selecione uma Avaliação.")

                id_turma = turma_map[turma_txt]
                id_aluno = aluno_map[aluno_txt]
                id_disciplina = disc_map[disc_txt]
                id_professor = prof_map[prof_txt]
                id_avaliacao = avali_map[avali_txt]

                nota_val = _parse_float(nota_entry.get(), "Nota", required=True)
                if nota_val < 0 or nota_val > 10:
                    raise ValueError("A Nota deve estar entre 0 e 10.")

                peso_val = _parse_float(peso_entry.get(), "Peso", required=False)

                session = DatabaseConnection.get_session()
                try:
                    if modo == "novo":
                        existente = session.query(Nota).filter_by(id_turma=id_turma, id_aluno=id_aluno, id_disciplina=id_disciplina, id_professor=id_professor, id_avaliacao=id_avaliacao).first()
                        if existente:
                            raise ValueError("Já existe uma nota para essa combinação (Turma/Aluno/Disciplina/Professor/Avaliação).")

                        nova = Nota(id_turma=id_turma, id_aluno=id_aluno, id_disciplina=id_disciplina, id_professor=id_professor, id_avaliacao=id_avaliacao, nota=nota_val, peso=peso_val)
                        session.add(nova)
                        session.commit()

                        messagebox.showinfo("Sucesso", "Nota cadastrada com sucesso!")
                        dialog.destroy()
                        self.carregar_dados()
                    else:
                        if not dados:
                            raise ValueError("Dados da nota para edição não foram carregados.")

                        nota_obj = session.query(Nota).filter_by(id_turma=dados["id_turma"], id_aluno=dados["id_aluno"], id_disciplina=dados["id_disciplina"], id_professor=dados["id_professor"], id_avaliacao=dados["id_avaliacao"]).first()
                        if not nota_obj:
                            raise ValueError("Nota não encontrada no banco para atualização.")

                        chave_mudou = (id_turma != dados["id_turma"]) or (id_aluno != dados["id_aluno"]) or (id_disciplina != dados["id_disciplina"]) or (id_professor != dados["id_professor"]) or (id_avaliacao != dados["id_avaliacao"])

                        if chave_mudou:
                            existe_destino = session.query(Nota).filter_by(id_turma=id_turma, id_aluno=id_aluno, id_disciplina=id_disciplina, id_professor=id_professor, id_avaliacao=id_avaliacao).first()
                            if existe_destino:
                                raise ValueError("Já existe uma nota com a nova combinação escolhida. Altere os campos ou edite apenas nota/peso.")

                            session.delete(nota_obj)
                            session.flush()
                            # Recriar para manter integridade
                            nota_obj = Nota(id_turma=id_turma, id_aluno=id_aluno, id_disciplina=id_disciplina, id_professor=id_professor, id_avaliacao=id_avaliacao, nota=nota_val, peso=peso_val)
                            session.add(nota_obj)
                        else:
                            nota_obj.nota = nota_val
                            nota_obj.peso = peso_val

                        session.commit()
                        messagebox.showinfo("Sucesso", "Nota atualizada com sucesso!")
                        dialog.destroy()
                        self.carregar_dados()

                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()

            except Exception as e:
                messagebox.showerror("Erro", str(e))

        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(pady=12)

        cor_botao = "#4CAF50" if modo == "novo" else "#FF9800"
        texto_botao = "Cadastrar" if modo == "novo" else "Salvar Alterações"

        tk.Button(btn_frame, text=texto_botao, font=("Arial", 12, "bold"), bg=cor_botao, fg="white", width=18, height=2, command=salvar, cursor="hand2").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Cancelar", font=("Arial", 12), bg="#757575", fg="white", width=18, height=2, command=dialog.destroy, cursor="hand2").grid(row=0, column=1, padx=5)

    def voltar(self):
        self.frame.destroy()
        from screens.dashboard import DashboardScreen
        DashboardScreen(self.root, self.username, self.extra)
