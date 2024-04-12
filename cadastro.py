import mysql.connector
import database

def cadastro():
    cursor = None

    try:
        
        conexao = database.conectar_banco()

        if conexao:
           
            cursor = conexao.cursor()

            
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            email = input("Email: ")
            cpf = int(input("CPF: "))
            nascimento = input("Nascimento: ")
            senha = int(input("Senha: "))

            
            sql_clientes = "INSERT INTO clientes (nome, idade, email, cpf, nascimento, senha) VALUES (%s, %s, %s, %s, %s, %s)"
            val_clientes = (nome, idade, email, cpf, nascimento, senha)

            
            cursor.execute(sql_clientes, val_clientes)

            
            id_cliente = cursor.lastrowid

            
            sql_saldo = "INSERT INTO saldo (id_cliente, saldo) VALUES (%s, %s)"
            val_saldo = (id_cliente, 0)  

            
            cursor.execute(sql_saldo, val_saldo)

            
            conexao.commit()

            print("Cadastro realizado com sucesso!")

    except mysql.connector.Error as error:
        print(f"Erro ao executar operações no banco de dados: {error}")

    finally:
        
        if cursor:
            cursor.close()
        database.fechar_conexao(conexao)


cadastro()
