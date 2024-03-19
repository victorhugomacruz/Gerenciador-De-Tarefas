import sqlite3
from colorama import Fore, Style
from datetime import datetime

# Cores nos textos
vermelho = Fore.RED
verde = Fore.GREEN
amarelo = Fore.YELLOW
negrito = Style.BRIGHT
resetar = Style.RESET_ALL


def cadastrar_tarefas_sql(nome, data_atual):
    conexao = None

    try:
        conexao = sqlite3.connect("gerenciador_tarefas.db")
        cursor = conexao.cursor()

        consulta_sql = "SELECT * FROM tarefas WHERE nome = ?"
        cursor.execute(consulta_sql, (nome,))

        tarefa = cursor.fetchone()

        if not tarefa:
            consulta_sql = "INSERT INTO tarefas (nome, data, status) VALUES (?, ?, ?)"
            dados = (nome, data_atual, 'Pendente')
            cursor.execute(consulta_sql, dados)

            conexao.commit()

            print(verde + negrito + f'Tarefa {amarelo + nome + verde} cadastrada com sucesso!' + resetar)
        else:
            print(vermelho + negrito + 'Essa tarefa já está cadastrada!' + resetar)

    except sqlite3.Error:
        print(vermelho + negrito + 'Erro ao executar operação no banco de dados' + resetar)

    except Exception as e:
        print(vermelho + negrito + f'Ocorreu um erro inesperado: {e}' + resetar)

    finally:
        if conexao:
            conexao.close()


def exibir_tarefas_sql():
    conexao = None

    try:
        conexao = sqlite3.connect("gerenciador_tarefas.db")
        cursor = conexao.cursor()

        consulta_sql = "SELECT * FROM tarefas ORDER BY data, id"
        cursor.execute(consulta_sql)

        tarefas = cursor.fetchall()

        if tarefas:
            for tarefa in tarefas:
                data_str = tarefa[2]
                data = datetime.strptime(data_str, '%Y-%m-%d')
                data_formatada = data.strftime('%d/%m/%Y')
                if tarefa[3] == 'Pendente':
                    print(f'{tarefa[0]} - {tarefa[1]} | Adicionado em: {data_formatada} | Status: {amarelo + tarefa[3]}'
                          + resetar)
                else:
                    print(f'{tarefa[0]} - {tarefa[1]} | Adicionado em: {data_formatada} | Status: {verde + tarefa[3]}'
                          + resetar)
        else:
            print(vermelho + negrito + 'Ainda não existe nenhuma Tarefa cadastrada!' + resetar)

    except sqlite3.Error:
        print(vermelho + negrito + 'Erro ao executar operação no banco de dados' + resetar)

    except Exception as e:
        print(vermelho + negrito + f'Ocorreu um erro inesperado: {e}' + resetar)

    finally:
        if conexao:
            conexao.close()


def remover_tarefa_sql(nomeid):
    conexao = None

    try:
        conexao = sqlite3.connect("gerenciador_tarefas.db")
        cursor = conexao.cursor()

        consulta_sql = "SELECT * FROM tarefas WHERE id = ? OR nome = ?"
        cursor.execute(consulta_sql, (nomeid, nomeid.title()))

        tarefa = cursor.fetchone()

        if tarefa:
            id_tarefa = tarefa[0]
            nome_tarefa = tarefa[1]

            consulta_sql = "DELETE FROM tarefas WHERE id = ?"
            cursor.execute(consulta_sql, (id_tarefa,))
            conexao.commit()
            print(verde + negrito + f'Tarefa {amarelo + nome_tarefa + verde} excluida com sucesso!' + resetar)
        else:
            print(vermelho + negrito + 'Tarefa não encontrada.' + resetar)

    except sqlite3.Error:
        print(vermelho + negrito + 'Erro ao executar operação no banco de dados' + resetar)

    except Exception as e:
        print(vermelho + negrito + f'Ocorreu um erro inesperado: {e}' + resetar)

    finally:
        if conexao:
            conexao.close()


def limpar_tarefas_sql():
    conexao = None

    try:
        conexao = sqlite3.connect("gerenciador_tarefas.db")
        cursor = conexao.cursor()

        consulta_sql = "DELETE FROM tarefas"
        cursor.execute(consulta_sql)

        consulta_atualizacao = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tarefas'"
        cursor.execute(consulta_atualizacao)

        conexao.commit()

        print(verde + negrito + 'Todas as tarefas foram excluidas com sucesso!' + resetar)

    except sqlite3.Error:
        print(vermelho + negrito + 'Erro ao executar operação no banco de dados' + resetar)

    except Exception as e:
        print(vermelho + negrito + f'Ocorreu um erro inesperado: {e}' + resetar)

    finally:
        if conexao:
            conexao.close()


def concluir_tarefa_sql(nomeid):
    conexao = None

    try:
        conexao = sqlite3.connect("gerenciador_tarefas.db")
        cursor = conexao.cursor()

        consulta_sql = "SELECT * FROM tarefas WHERE id = ? OR nome = ?"
        cursor.execute(consulta_sql, (nomeid, nomeid.title()))

        tarefa = cursor.fetchone()

        if tarefa:
            id_tarefa = tarefa[0]
            nome_tarefa = tarefa[1]

            consulta_sql = "UPDATE tarefas SET status = 'Concluído' WHERE id = ?"
            cursor.execute(consulta_sql, (id_tarefa,))
            conexao.commit()
            print(verde + negrito + f'Status da tarefa {amarelo + nome_tarefa + verde} alterado para Concluído!'
                  + resetar)
        else:
            print(vermelho + negrito + 'Tarefa não encontrada!' + resetar)

    except sqlite3.Error:
        print(vermelho + negrito + 'Erro ao executar operação no banco de dados' + resetar)

    except Exception as e:
        print(vermelho + negrito + f'Ocorreu um erro inesperado: {e}' + resetar)

    finally:
        if conexao:
            conexao.close()
