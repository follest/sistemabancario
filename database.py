import mysql.connector

def conectar_banco():
    try:
        #
        db_connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )
        print("Conexão bem-sucedida!")
        return db_connection
    except mysql.connector.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

def fechar_conexao(conexao):
    if conexao:
        conexao.close()
        print("\nConexão com o banco de dados fechada.")