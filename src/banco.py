import duckdb

# banco.py
import duckdb

def criar_banco(banco_path="face_db.duckdb"):
    con = duckdb.connect(banco_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            nome TEXT,
            caminho_imagem TEXT,
            embedding BLOB
        )
    """)
    con.close()