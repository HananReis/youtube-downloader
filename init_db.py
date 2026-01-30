import sqlite3
import os

# Criar banco de dados (arquivo na raiz do projeto: database-post.db)
import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'database-post.db')

os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela de posts (APENAS se não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        published INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Criar tabela de configurações do site (APENAS se não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS site_config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')

# Inserir valores padrão sem apagar dados
cursor.execute('SELECT value FROM site_config WHERE key=?', ('font_size',))
if not cursor.fetchone():
    cursor.execute('INSERT INTO site_config (key, value) VALUES (?, ?)', ('font_size', '18px'))

cursor.execute('SELECT value FROM site_config WHERE key=?', ('font_family',))
if not cursor.fetchone():
    cursor.execute('INSERT INTO site_config (key, value) VALUES (?, ?)', ('font_family', 'Times New Roman'))

conn.commit()
conn.close()

print(f"✓ Banco de dados criado/verificado em: {db_path}")
