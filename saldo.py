import mysql.connector
import database

def consultar_saldo(id_cliente, senha):
    try:
        conexao = database.conectar_banco()

        if conexao:
            cursor = conexao.cursor()

            sql_verificar_cliente = "SELECT id FROM clientes WHERE id = %s AND senha = %s"
            cursor.execute(sql_verificar_cliente, (id_cliente, senha))
            cliente_existe = cursor.fetchone()

            if cliente_existe:

                sql_consulta_saldo = "SELECT saldo FROM saldo WHERE id_cliente = %s"
                cursor.execute(sql_consulta_saldo, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    saldo_cliente = resultado[0]
                    return saldo_cliente
                else:
                    print(f"Saldo não encontrado para o cliente com ID {id_cliente}.")
            else:
                print("Credenciais inválidas. Acesso negado.")

    except mysql.connector.Error as error:
        print(f"Erro ao consultar saldo: {error}")

    finally:

        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if conexao.is_connected():
            conexao.close()


id_cliente = int(input("Número da conta: "))
senha = input("Senha: ")


saldo_cliente = consultar_saldo(id_cliente, senha)

if saldo_cliente is not None:
    print(f"O saldo do cliente com ID {id_cliente} é: R$ {saldo_cliente:.2f}")
