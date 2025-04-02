from database.oracle_db import conectar
import oracledb
from difflib import SequenceMatcher

class ProdutoModel:
    @staticmethod
    def criar_tabela():
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE produtos (
                        produto_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        nome VARCHAR2(100) NOT NULL,
                        descricao VARCHAR2(500),
                        preco NUMBER(10,2) NOT NULL CHECK (preco > 0),
                        estoque NUMBER(9) DEFAULT 0 CHECK (estoque >= 0),
                        ativo NUMBER(1) DEFAULT 1,
                        data_criacao TIMESTAMP DEFAULT SYSTIMESTAMP,
                        data_atualizacao TIMESTAMP DEFAULT SYSTIMESTAMP,
                        CONSTRAINT uk_produto_nome UNIQUE (nome)
                    )';
                    
                    EXECUTE IMMEDIATE 'CREATE OR REPLACE TRIGGER trg_produto_atualizacao
                        BEFORE UPDATE ON produtos
                        FOR EACH ROW
                        BEGIN
                            :NEW.data_atualizacao := SYSTIMESTAMP;
                        END;';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE = -955 THEN NULL;
                        ELSE RAISE;
                        END IF;
                END;
            """)
            conn.commit()
        except oracledb.DatabaseError:
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def _nome_existe(nome: str, exclude_id: int = None) -> bool:
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            if exclude_id:
                cursor.execute(
                    "SELECT 1 FROM produtos WHERE UPPER(nome) = UPPER(:1) AND produto_id != :2",
                    [nome.strip(), exclude_id]
                )
            else:
                cursor.execute(
                    "SELECT 1 FROM produtos WHERE UPPER(nome) = UPPER(:1)",
                    [nome.strip()]
                )
            return cursor.fetchone() is not None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def inserir_produto(nome: str, preco: float, descricao: str = None, estoque: int = 0) -> int:
        if ProdutoModel._nome_existe(nome):
            raise ValueError(f"Já existe um produto com o nome '{nome}'")

        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            out_var = cursor.var(oracledb.NUMBER)
            cursor.execute(
                """INSERT INTO produtos (nome, descricao, preco, estoque)
                VALUES (:1, :2, :3, :4)
                RETURNING produto_id INTO :5""",
                [nome.strip(), descricao, preco, estoque, out_var]
            )
            conn.commit()
            return out_var.getvalue()[0]
        except oracledb.DatabaseError:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(produto_id: int):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT produto_id, nome, descricao, preco, estoque, ativo,
                       TO_CHAR(data_criacao, 'DD/MM/YYYY HH24:MI:SS'),
                       TO_CHAR(data_atualizacao, 'DD/MM/YYYY HH24:MI:SS')
                FROM produtos WHERE produto_id = :1
            """, [produto_id])
            row = cursor.fetchone()
            if row:
                columns = [col[0].lower() for col in cursor.description]
                return dict(zip(columns, row))
            return None
        except oracledb.DatabaseError:
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def listar_produtos(ativos: bool = True, ordenar_por: str = 'nome'):
        valid_order_fields = {'nome', 'preco', 'estoque', 'data_criacao'}
        if ordenar_por not in valid_order_fields:
            ordenar_por = 'nome'
            
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = f"""
                SELECT produto_id, nome, descricao, preco, estoque, ativo,
                       TO_CHAR(data_criacao, 'DD/MM/YYYY HH24:MI:SS'),
                       TO_CHAR(data_atualizacao, 'DD/MM/YYYY HH24:MI:SS')
                FROM produtos
                {'WHERE ativo = 1' if ativos else ''}
                ORDER BY {ordenar_por}
            """
            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor]
        except oracledb.DatabaseError:
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def atualizar_produto(produto_id: int, **kwargs) -> int:
        campos_validos = {'nome', 'descricao', 'preco', 'estoque', 'ativo'}
        campos = {k: v for k, v in kwargs.items() if k in campos_validos}
        
        if not campos:
            raise ValueError("Nenhum campo válido para atualização")
        
        if 'nome' in campos and ProdutoModel._nome_existe(campos['nome'], produto_id):
            raise ValueError(f"Já existe outro produto com o nome '{campos['nome']}'")
        
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = :{i+1}" for i, k in enumerate(campos.keys())])
            valores = list(campos.values())
            valores.append(produto_id)
            
            cursor.execute(
                f"UPDATE produtos SET {set_clause} WHERE produto_id = :{len(campos)+1}",
                valores
            )
            conn.commit()
            return cursor.rowcount
        except oracledb.DatabaseError:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def remover_produto(produto_id: int, fisico: bool = False) -> int:
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            if fisico:
                cursor.execute("DELETE FROM produtos WHERE produto_id = :1", [produto_id])
            else:
                cursor.execute("UPDATE produtos SET ativo = 0 WHERE produto_id = :1", [produto_id])
            conn.commit()
            return cursor.rowcount
        except oracledb.DatabaseError:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def ajustar_estoque(produto_id: int, quantidade: int) -> int:
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT estoque FROM produtos WHERE produto_id = :1 AND ativo = 1",
                [produto_id]
            )
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Produto não encontrado ou inativo")
            estoque_atual = resultado[0]
            novo_estoque = estoque_atual + quantidade
            if novo_estoque < 0:
                raise ValueError("Estoque não pode ficar negativo")
            cursor.execute(
                "UPDATE produtos SET estoque = :1 WHERE produto_id = :2",
                [novo_estoque, produto_id]
            )
            conn.commit()
            return novo_estoque
        except oracledb.DatabaseError:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def buscar_similares(nome: str, limiar: float = 0.7):
        conn = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT produto_id, nome FROM produtos")
            produtos = []
            for row in cursor:
                similarity = SequenceMatcher(None, nome.lower(), row[1].lower()).ratio()
                if similarity >= limiar:
                    produtos.append({
                        'produto_id': row[0],
                        'nome': row[1],
                        'similaridade': similarity
                    })
            return sorted(produtos, key=lambda x: x['similaridade'], reverse=True)
        finally:
            if conn:
                conn.close()