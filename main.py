import os
from banco_dados import *
import datetime
from colorama import init, Fore, Style

# Cores nos textos
init()
vermelho = Fore.RED
verde = Fore.GREEN
negrito = Style.BRIGHT
resetar = Style.RESET_ALL


def criar_banco_de_dados():
    try:
        if not os.path.exists('gerenciador_tarefas.db'):
            conexao = sqlite3.connect('gerenciador_tarefas.db')
            cursor = conexao.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(100) NOT NULL,
                                data DATE NOT NULL,
                                status VARCHAR(10) NOT NULL
                            )''')

            conexao.commit()
            conexao.close()

    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")


def menu():
    print("""
MENU DE OPÇÕES
[1] Adicionar tarefa
[2] Remover Tarefa
[3] Concluir Tarefa
[4] Limpar lista de tarefas
[5] Exibir tarefas
[0] Sair
    """)


def add_tarefa():
    data_atual = datetime.date.today()
    nome = input('Nome da tarefa: ').strip().title()
    if nome == '':
        while nome == '':
            nome = input(vermelho + negrito + 'Digite uma tarefa válida, ou digite "S" para '
                                              'sair: ' + resetar).strip().title()
    if nome == 'S':
        print(vermelho + negrito + 'Saindo...' + resetar)
        return
    cadastrar_tarefas_sql(nome, data_atual)


def remover_tarefa():
    exibir_tarefas_sql()
    print()
    nomeid = input('Essas são suas tarefas, digite o número ID ou o nome '
                   'da tarefa para remove-la: ').strip()
    remover_tarefa_sql(nomeid)


def concluir_tarefa():
    exibir_tarefas_sql()
    print()
    nomeid = input('Essas são suas tarefas, digite o número ID ou o nome '
                   'da tarefa para concluí-la: ').strip()
    concluir_tarefa_sql(nomeid)


def limpar_tarefas():
    limpar_tarefas_sql()


def exibir_tarefas():
    exibir_tarefas_sql()


criar_banco_de_dados()

while True:
    menu()
    try:
        escolha = int(input('Qual opção você deseja: '))

        if escolha == 0:
            print(vermelho + negrito + 'Saindo...' + resetar)
            break
        elif escolha == 1:
            add_tarefa()
        elif escolha == 2:
            remover_tarefa()
        elif escolha == 3:
            concluir_tarefa()
        elif escolha == 4:
            limpar_tarefas()
        elif escolha == 5:
            exibir_tarefas()
        else:
            print(vermelho + negrito + 'Opção inválida, tente novamente.' + resetar)

    except ValueError:
        print(vermelho + negrito + "Por favor, digite uma opção válida ou digite 0 para sair." + resetar)
    except KeyboardInterrupt:
        print(vermelho + negrito + "\nOperação interrompida pelo usuário." + resetar)
