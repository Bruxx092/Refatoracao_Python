from models.user_model import UserModel

def main():
    try:
        print("Testing database connection...")
        from database.oracle_db import conectar
        conn = conectar()
        conn.close()
        
        print("\nCreating table...")
        UserModel.criar_tabela()
        
        print("\nInserting user...")
        user_id = UserModel.inserir_usuario("John Doe", "john@example.com")
        print(f"Inserted user ID: {user_id}")
        
        print("\nListing users...")
        users = UserModel.listar_usuarios()
        print("Users:", users)
        
    except Exception as e:
        print(f"\nError in test: {str(e)}")

if __name__ == "__main__":
    main()