import oracledb
from database.db import conectar

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE usuarios (
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                nome VARCHAR2(100) NOT NULL,
                email VARCHAR2(100) NOT NULL,
                PRIMARY KEY(id),
                CONSTRAINT email_unico UNIQUE (email)
            )
        """)
        conn.commit()
        print("Tabela criada com sucesso")
    except oracledb.DatabaseError as e:
        error_obj = e.args[0]
        if hasattr(error_obj, 'code') and error_obj.code == 955:
            print("Tabela já existente...")
        else:
            print(f"Erro Oracle: {e}")
    finally:
        cursor.close()
        conn.close()


def inserir_usuario(nome, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (NOME, EMAIL) VALUES (:nome,:email)', {'nome': nome, 'email': email}) # :nome é um placeholder
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall() 
    conn.close()
    return usuarios

def excluir_usuario(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE ID = :id', {'id': user_id})
    conn.commit()
    conn.close()

def buscar_usuario_por_id(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE ID = :id', {'id': user_id})
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def atualizar_usuario(user_id, nome, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET NOME = :nome, EMAIL = :email WHERE ID = :id', {'nome': nome, 'email': email, 'id': user_id})
    conn.commit()
    conn.close()