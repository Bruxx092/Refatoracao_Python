from database.oracle_db import conectar
import oracledb

class UserModel:
    @staticmethod
    def criar_tabela():
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            
            cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE usuarios (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        nome VARCHAR2(100) NOT NULL,
                        email VARCHAR2(100) NOT NULL UNIQUE
                    )';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE = -955 THEN NULL; -- table already exists
                        ELSE RAISE;
                        END IF;
                END;
            """)
            conn.commit()
            print("Table created successfully")
            
        except oracledb.DatabaseError as e:
            print(f"Error creating table: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def inserir_usuario(nome, email):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            out_var = cursor.var(oracledb.NUMBER)
            cursor.execute(
                "INSERT INTO usuarios (nome, email) VALUES (:1, :2) RETURNING id INTO :3",
                [nome, email, out_var]
            )
            conn.commit()
            return out_var.getvalue()[0]
            
        except oracledb.DatabaseError as e:
            if conn:
                conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:  
                raise ValueError("Email already exists") from e
            print(f"Error inserting user: {e}")
            raise
        finally:
            if conn:
                conn.close()
