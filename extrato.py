import mysql.connector
import database

def extrato():
    cursor = None

    try:
        
        conexao = database.conectar_banco()

        if conexao:
            cursor = conexao.cursor()

            
            id_cliente = int(input("ID do Cliente: "))
            senha = input("Senha: ")

            
            sql_verificar_cliente = "SELECT id FROM clientes WHERE id = %s AND senha = %s"
            cursor.execute(sql_verificar_cliente, (id_cliente, senha))
            cliente_existe = cursor.fetchone()

            if cliente_existe:
                
               
                sql_depositos = "SELECT valor_deposito, data_deposito FROM deposito WHERE id_cliente = %s"
                cursor.execute(sql_depositos, (id_cliente,))
                depositos = cursor.fetchall()

               
                sql_saques = "SELECT valor_saque, data_saque FROM saque WHERE id_cliente = %s"
                cursor.execute(sql_saques, (id_cliente,))
                saques = cursor.fetchall()

                
                print(f"Extrato Bancário para o Cliente ID {id_cliente}:")
                print("\nDepósitos:")
                for deposito in depositos:
                    valor_deposito, data_deposito = deposito
                    print(f"  - Depósito de R$ {valor_deposito:.2f} em {data_deposito}")

                print("\nSaques:")
                for saque in saques:
                    valor_saque, data_saque = saque
                    print(f"  - Saque de R$ {valor_saque:.2f} em {data_saque}")

            else:
                print(f"Cliente com ID {id_cliente} ou senha incorretos.")

    except mysql.connector.Error as error:
        print(f"Erro ao gerar o extrato bancário: {error}")

    finally:
        
        if cursor:
            cursor.close()
        database.fechar_conexao(conexao)


extrato()

