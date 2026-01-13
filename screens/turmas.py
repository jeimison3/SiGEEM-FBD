import tkinter as tk
from tkinter import ttk, messagebox

class TurmasScreen:
    def __init__(self, root, username="Admin"):
        self.root = root
        self.username = username
        self.dados_turmas = [
            {'id': 1, 'nome': '1º Ano A', 'ano': '2024', 'turno': 'Manhã'}
        ] 
        self.proximo_id = 2
        
        self.frame = tk.Frame(root, bg='#f0f0f0')
        self.frame.pack(fill='both', expand=True)
        
        self.create_widgets()
        self.carregar_dados()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.frame, bg='#4CAF50', height=50)
        header.pack(fill='x')
        tk.Label(header, text="Sistema de Turmas", font=('Arial', 14, 'bold'), 
                 bg='#4CAF50', fg='white').pack(pady=10)

        # Barra de Busca (CONSULTA/FILTRAGEM) - 1,5 pts
        search_frame = tk.Frame(self.frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="🔍 Filtrar por nome:", bg='#f0f0f0').pack(side='left')
        self.ent_filtro = tk.Entry(search_frame)
        self.ent_filtro.pack(side='left', padx=5, expand=True, fill='x')
        self.ent_filtro.bind('<KeyRelease>', lambda e: self.carregar_dados())

        # Botões Principais (INCLUSÃO, EDIÇÃO, REMOÇÃO) - 4,5 pts
        btn_frame = tk.Frame(self.frame, bg='#f0f0f0')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="➕ Novo", bg='#4CAF50', fg='white', width=10,
                  command=self.abrir_formulario).pack(side='left', padx=5)
        
        # AQUI ESTÁ O BOTÃO EDITAR
        tk.Button(btn_frame, text="✏️ Editar", bg='#FF9800', fg='white', width=10,
                  command=self.preparar_edicao).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ Remover", bg='#F44336', fg='white', width=10,
                  command=self.remover).pack(side='left', padx=5)

        # Tabela
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Nome', 'Ano', 'Turno'), show='headings')
        for col in ('ID', 'Nome', 'Ano', 'Turno'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(padx=20, pady=10, fill='both', expand=True)

    def carregar_dados(self):
        """Lógica de filtragem"""
        for i in self.tree.get_children(): self.tree.delete(i)
        filtro = self.ent_filtro.get().lower()
        for t in self.dados_turmas:
            if filtro in t['nome'].lower():
                self.tree.insert('', 'end', values=(t['id'], t['nome'], t['ano'], t['turno']))

    def preparar_edicao(self):
        """Verifica se há algo selecionado antes de abrir o formulário de edição"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma turma na tabela para editar!")
            return
        
        # Pega os dados da linha selecionada
        valores = self.tree.item(sel)['values']
        # Chama o formulário passando os dados para preenchimento
        self.abrir_formulario(editar=True, dados_atuais=valores)

    def abrir_formulario(self, editar=False, dados_atuais=None):
        """Janela única para Cadastro e Edição"""
        janela_form = tk.Toplevel(self.root)
        janela_form.title("Editar Turma" if editar else "Nova Turma")
        janela_form.geometry("300x300")
        janela_form.grab_set()

        tk.Label(janela_form, text="Nome da Turma:").pack(pady=(10,0))
        ent_nome = tk.Entry(janela_form)
        ent_nome.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Ano Letivo:").pack(pady=(10,0))
        ent_ano = tk.Entry(janela_form)
        ent_ano.pack(padx=20, fill='x')

        tk.Label(janela_form, text="Turno:").pack(pady=(10,0))
        cb_turno = ttk.Combobox(janela_form, values=["Manhã", "Tarde", "Noite"])
        cb_turno.pack(padx=20, fill='x')

        # Se for edição, preenche os campos com os valores atuais
        if editar:
            ent_nome.insert(0, dados_atuais[1])
            ent_ano.insert(0, dados_atuais[2])
            cb_turno.set(dados_atuais[3])

        def salvar():
            nome, ano, turno = ent_nome.get(), ent_ano.get(), cb_turno.get()
            if not (nome and ano and turno):
                messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
                return

            if editar:
                # Localiza pelo ID e atualiza a lista
                for t in self.dados_turmas:
                    if t['id'] == dados_atuais[0]:
                        t['nome'], t['ano'], t['turno'] = nome, ano, turno
                messagebox.showinfo("Sucesso", "Turma atualizada!")
            else:
                # Cria novo registro
                nova_turma = {'id': self.proximo_id, 'nome': nome, 'ano': ano, 'turno': turno}
                self.dados_turmas.append(nova_turma)
                self.proximo_id += 1
                messagebox.showinfo("Sucesso", "Turma cadastrada!")
            
            self.carregar_dados()
            janela_form.destroy()

        tk.Button(janela_form, text="Confirmar", bg='#2196F3', fg='white', 
                  command=salvar, height=2).pack(pady=20, padx=20, fill='x')

    def remover(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma turma para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir esta turma?"):
            id_rem = self.tree.item(sel)['values'][0]
            self.dados_turmas = [t for t in self.dados_turmas if t['id'] != id_rem]
            self.carregar_dados()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = TurmasScreen(root)
    root.mainloop()
