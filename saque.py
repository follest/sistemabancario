import mysql.connector
import database
from datetime import date
import decimal

def saque():
    cursor = None

    try:
        # Conectar ao banco de dados
        conexao = database.conectar_banco()

        if conexao:
            cursor = conexao.cursor()

            id_cliente = int(input("ID do Cliente: "))
            senha = input("Senha: ")
            valor_saque = decimal.Decimal(input("Valor do Saque: "))
            data_saque = date.today()

            # Verificar se o cliente com o ID e senha especificados existe na tabela clientes
            sql_verificar_cliente = "SELECT id FROM clientes WHERE id = %s AND senha = %s"
            cursor.execute(sql_verificar_cliente, (id_cliente, senha))
            cliente_existe = cursor.fetchone()

            if cliente_existe:
                # O cliente com o ID e senha especificados existe, prosseguir com o saque

                # Obter o saldo atual do cliente na tabela 'saldo'
                sql_saldo_atual = "SELECT saldo FROM saldo WHERE id_cliente = %s"
                cursor.execute(sql_saldo_atual, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    saldo_atual = decimal.Decimal(resultado[0])

                    # Verificar se o saldo atual é suficiente para o saque
                    if saldo_atual >= valor_saque:
                        novo_saldo = saldo_atual - valor_saque

                        # Atualizar o saldo na tabela 'saldo'
                        sql_atualizar_saldo = "UPDATE saldo SET saldo = %s WHERE id_cliente = %s"
                        dados_atualizar_saldo = (novo_saldo, id_cliente)
                        cursor.execute(sql_atualizar_saldo, dados_atualizar_saldo)

                        # Inserir o saque na tabela 'saque'
                        sql_saque = "INSERT INTO saque (id_cliente, valor_saque, data_saque) VALUES (%s, %s, %s)"
                        dados_saque = (id_cliente, valor_saque, data_saque)
                        cursor.execute(sql_saque, dados_saque)

                        # Commit para salvar as alterações no banco de dados
                        conexao.commit()

                        print("Saque realizado com sucesso!")
                        print(f"Novo saldo para o cliente ID {id_cliente}: R$ {novo_saldo:.2f}")
                    else:
                        print("Saldo insuficiente para realizar o saque.")
                else:
                    print(f"Saldo não encontrado para o cliente ID {id_cliente}.")
            else:
                print(f"Senha incorreta.")

    except mysql.connector.Error as error:
        print(f"Erro ao realizar o saque: {error}")

    finally:
        # Fechar o cursor e a conexão com o banco de dados
        if cursor:
            cursor.close()
        database.fechar_conexao(conexao)

# Chamada da função 'saque' para realizar o saque
saque()
