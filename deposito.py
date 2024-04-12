import mysql.connector
import database
from datetime import date
import decimal

def deposito():
    cursor = None

    try:
        
        conexao = database.conectar_banco()

        if conexao:
            cursor = conexao.cursor()

            id_cliente = int(input("Chave Pix: "))
            senha = input("Senha: ")
            valor_deposito = decimal.Decimal(input("Valor do Depósito: "))  
            data_deposito = date.today()

           
            sql_verificar_cliente = "SELECT id FROM clientes WHERE id = %s AND senha = %s"
            cursor.execute(sql_verificar_cliente, (id_cliente, senha))
            cliente_existe = cursor.fetchone()

            if cliente_existe:
                

                
                sql_deposito = "INSERT INTO deposito (id_cliente, valor_deposito, data_deposito) VALUES (%s, %s, %s)"
                dados_deposito = (id_cliente, valor_deposito, data_deposito)
                cursor.execute(sql_deposito, dados_deposito)

               
                sql_saldo_atual = "SELECT saldo FROM saldo WHERE id_cliente = %s"
                cursor.execute(sql_saldo_atual, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    saldo_atual = decimal.Decimal(resultado[0])  
                    novo_saldo = saldo_atual + valor_deposito

                   
                    sql_atualizar_saldo = "UPDATE saldo SET saldo = %s WHERE id_cliente = %s"
                    dados_atualizar_saldo = (novo_saldo, id_cliente)
                    cursor.execute(sql_atualizar_saldo, dados_atualizar_saldo)

                   
                    conexao.commit()

                    print("Depósito realizado com sucesso!")
                    print(f"Novo saldo para o cliente ID {id_cliente}: R$ {novo_saldo:.2f}")
                else:
                    print(f"Saldo não encontrado para o cliente ID {id_cliente}.")
            else:
                print("Senha errada. Operação cancelada.")

    except mysql.connector.Error as error:
        print(f"Erro ao realizar o depósito: {error}")

    finally:
       
        if cursor:
            cursor.close()
        database.fechar_conexao(conexao)


deposito()
