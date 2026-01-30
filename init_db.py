import os
import sqlite3
from app import app, db

# Caminho do arquivo em /data para persistência de volume
db_path = '/data/database-post.db'

# Garantir pasta /data (silenciar erros de permissão quando não aplicável)
try:
    os.makedirs('/data', exist_ok=True)
except PermissionError:
    pass

# Registrar modelos e criar tabelas (APENAS se não existirem)
with app.app_context():
    # Importar models para garantir que as classes SQLAlchemy sejam registradas
    import models  # noqa: F401
    db.create_all()

# Inserir/garantir valores padrão em site_config sem apagar tabelas/dados
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS site_config (
    key TEXT PRIMARY KEY,
    value TEXT
)
''')
cur.execute('SELECT value FROM site_config WHERE key=?', ('font_size',))
if not cur.fetchone():
    cur.execute('INSERT INTO site_config (key, value) VALUES (?, ?)', ('font_size', '18px'))
cur.execute('SELECT value FROM site_config WHERE key=?', ('font_family',))
if not cur.fetchone():
    cur.execute('INSERT INTO site_config (key, value) VALUES (?, ?)', ('font_family', 'Times New Roman'))
conn.commit()
conn.close()

print(f"✓ Banco criado/verificado em: {db_path}")
print("Rode este script manualmente: python init_db.py. Este script NÃO roda automaticamente no start do app.")
