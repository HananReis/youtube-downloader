"""Modelo simples para configurações do site (uso com SQLite puro).
Embora o aplicativo principal manipule site_config diretamente em `app.py`, este módulo fornece
uma API leve que pode ser usada por outras partes do projeto no futuro.
"""
import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database.db'))

class SiteConfig:
    @staticmethod
    def get(key, default=None):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT value FROM site_config WHERE key=?', (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else default

    @staticmethod
    def set(key, value):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO site_config (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()
