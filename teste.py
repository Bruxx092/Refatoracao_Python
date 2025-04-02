from models.user_model import UserModel

def main():
    try:
        print("Testando conexão com a database...")
        from database.oracle_db import conectar
        conn = conectar()
        conn.close()
        
        print("\nCriando Tabela...")
        UserModel.criar_tabela()
        
        print("\nInserindo usuário...")
        user_id = UserModel.inserir_usuario("John Doe", "john@exemplo.com")
        print(f"Inserindo ID de usuário: {user_id}")
        
        print("\nListando usuários...")
        users = UserModel.listar_usuarios()
        print("Users:", users)
        
    except Exception as e:
        print(f"\nErro no teste: {str(e)}")

if __name__ == "__main__":
    main()