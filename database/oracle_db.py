import oracledb
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def conectar():
    try:
        print("Attempting connection with:")
        print(f"User: {os.getenv('ORACLE_USER')}")
        print(f"DSN: {os.getenv('ORACLE_DSN')}")
        
        if os.getenv("ORACLE_THICK_MODE", "False").lower() == "true":
            oracledb.init_oracle_client()
        
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )
        print("Connection successful!")
        return conn
        
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        raise

if __name__ == "__main__":
    connection = conectar()
    if connection:
        connection.close()