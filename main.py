import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import END
from PIL import Image
import os
from banco_dados import *

# Listas para armazenar as tarefas pendentes, todas as tarefas, e as concluídas
checkboxes_pendentes = []
checkboxes_tarefas = []
checkboxes_concluidas = []

# Criando janela principal tkinter
janela = ctk.CTk()
ctk.set_appearance_mode("Dark")
janela.geometry("350x450")
janela.title("Gerenciador de Tarefas")
janela.iconbitmap('icons/icone_principal.ico')
janela.resizable(height=False, width=False)

# Imagens para a interface
img_adicionar_tarefa = ctk.CTkImage(dark_image=Image.open("./icons/botao-adicionar.png"), size=(20, 20))
img_limpar_tarefas = ctk.CTkImage(dark_image=Image.open("./icons/vassoura.png"), size=(20, 20))
img_remover_tarefa = ctk.CTkImage(dark_image=Image.open("./icons/botao-excluir.png"), size=(20, 20))

resultado = False


def criar_banco_de_dados():
    if not os.path.exists('gerenciador_tarefas.db'):
        conexao = sqlite3.connect('gerenciador_tarefas.db')
        cursor = conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome VARCHAR(100) NOT NULL,
                            status VARCHAR(10) NOT NULL
                        )''')
        conexao.commit()
        conexao.close()


def execucoes_sql(query, params=(), fetchall=False):
    global resultado
    conexao = sqlite3.connect("gerenciador_tarefas.db")
    cursor = conexao.cursor()
    cursor.execute(query, params)
    if fetchall:
        resultado = cursor.fetchall()
    conexao.commit()
    conexao.close()

    return resultado


def add_tarefa():
    def add_interface(n):
        tarefas_check = ctk.CTkCheckBox(tab1, text=n, command=lambda: check_box(tarefas_check, n))
        tarefas_check.pack(anchor="w", pady=5)
        checkboxes_tarefas.append(tarefas_check)

        tarefas_checkp = ctk.CTkCheckBox(tab2, text=n, command=lambda: check_box(tarefas_check, n))
        tarefas_checkp.pack(anchor="w", pady=5)
        checkboxes_pendentes.append(tarefas_checkp)

    nome = entry.get().strip().title()
    if nome == '':
        CTkMessagebox(title="Erro",
                      message="Insira um nome válido!",
                      icon="icons/error.png",
                      master=janela
                      )
        return
    entry.delete(0, END)

    conexao = sqlite3.connect("gerenciador_tarefas.db")
    cursor = conexao.cursor()
    consulta_sql = "SELECT * FROM tarefas WHERE nome = ?"
    cursor.execute(consulta_sql, (nome,))
    tarefa = cursor.fetchone()

    if not tarefa:
        consulta_sql = "INSERT INTO tarefas (nome, status) VALUES (?, ?)"
        dados = (nome, 'Pendente')
        cursor.execute(consulta_sql, dados)
        conexao.commit()
        conexao.close()

        add_interface(nome)


def limpar_widgets():
    for widget in tab1.winfo_children():
        widget.destroy()

    for widget in tab2.winfo_children():
        widget.destroy()

    for widget in tab3.winfo_children():
        widget.destroy()

    exibir_tarefas()


def limpar_tarefas():
    execucoes_sql("DELETE FROM tarefas")
    limpar_widgets()


def atualizar_status(nome, status):
    execucoes_sql("UPDATE tarefas SET status = ? WHERE nome = ?", (status, nome))


def check_box(c, nome):
    status = 'Concluída' if c.get() else 'Pendente'
    atualizar_status(nome, status)
    limpar_widgets()


def exibir_tarefas():

    global contador_pendente, contador_concluidas
    tarefas = execucoes_sql("SELECT nome, status FROM tarefas", fetchall=True)

    if not tarefas:
        for widget in tab1.winfo_children():
            widget.destroy()

        for widget in tab2.winfo_children():
            widget.destroy()

        for widget in tab3.winfo_children():
            widget.destroy()

    else:
        for tarefa in tarefas:
            tarefas_check = ctk.CTkCheckBox(tab1, text=tarefa[0])
            tarefas_check.configure(command=lambda check=tarefas_check, nomet=tarefa[0]: check_box(check, nomet))
            tarefas_check.pack(anchor="w", pady=5)

            if tarefa[1] == 'Pendente':
                tarefas_checkp = ctk.CTkCheckBox(tab2, text=tarefa[0])
                tarefas_checkp.configure(command=lambda check=tarefas_checkp, nomet=tarefa[0]: check_box(check, nomet))
                tarefas_checkp.pack(anchor="w", pady=5)

            if tarefa[1] == 'Concluída':
                tarefas_check.select()
                tarefas_checkc = ctk.CTkCheckBox(tab3, text=tarefa[0])
                tarefas_checkc.configure(command=lambda check=tarefas_checkc, nomet=tarefa[0]: check_box(check, nomet))
                tarefas_checkc.pack(anchor="w", pady=5)
                tarefas_checkc.select()


def remover_tarefa():
    janela.iconify()
    remover = ctk.CTkInputDialog(text="Remover tarefa",
                                 title="Remover tarefa",
                                 )
    nome_tarefa = remover.get_input()
    if nome_tarefa is None:
        janela.deiconify()
        return
    else:
        nome_tarefa = nome_tarefa.strip().title()
        tarefa = execucoes_sql("SELECT nome FROM tarefas WHERE nome = ?", (nome_tarefa,), fetchall=True)

        if tarefa:
            execucoes_sql("DELETE FROM tarefas WHERE nome = ?", (nome_tarefa,))
            janela.deiconify()
            limpar_widgets()
        else:
            CTkMessagebox(title="Erro",
                          message="Tarefa não encontrada!",
                          icon="icons/error.png",
                          master=janela
                          )
            janela.deiconify()
            return


criar_banco_de_dados()

entry = ctk.CTkEntry(janela,
                     width=200,
                     height=50,
                     placeholder_text="Digite sua tarefa aqui",
                     font=("", 14)
                     )
entry.pack(pady=5)

botao_tarefa = ctk.CTkButton(janela,
                             text="Adicionar Tarefa",
                             command=add_tarefa,
                             image=img_adicionar_tarefa
                             )
botao_tarefa.pack(pady=10)

scroll = ctk.CTkScrollableFrame(janela, width=300, height=50)
scroll.pack(pady=10)

tabview = ctk.CTkTabview(scroll, width=False, height=False)
tabview.pack()
tab1 = tabview.add("Tarefas")
tab2 = tabview.add("Pendentes")
tab3 = tabview.add("Concluídas")
tabview.tab("Tarefas").grid_columnconfigure(0, weight=1)
tabview.tab("Pendentes").grid_columnconfigure(0, weight=1)
tabview.tab("Concluídas").grid_columnconfigure(0, weight=1)

exibir_tarefas()

limpartarefas = ctk.CTkButton(janela,
                              text="Limpar lista de tarefas",
                              command=limpar_tarefas,
                              image=img_limpar_tarefas
                              )
limpartarefas.pack()

botao_remover = ctk.CTkButton(janela,
                              text="Remover Tarefa",
                              command=remover_tarefa,
                              image=img_remover_tarefa
                              )
botao_remover.pack(pady=10)

janela.mainloop()
