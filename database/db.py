import os
from dotenv import load_dotenv
import oracledb

load_dotenv()

def conectar():
    oracledb.init_oracle_client()
    conn = oracledb.connect(
        user = os.getenv("ORACLE_USER"),
        password = os.getenv("ORACLE_PASSWORD"),
        host = os.getenv("ORACLE_HOST"),
        port = os.getenv("ORACLE_PORT"),
        service_name = os.getenv("ORACLE_SERVICE")
    )
    print("connectado")
    return conn