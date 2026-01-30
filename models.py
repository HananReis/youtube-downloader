"""Modelo simples para configurações do site (uso com SQLite puro).
Embora o aplicativo principal manipule site_config diretamente em `app.py`, este módulo fornece
uma API leve que pode ser usada por outras partes do projeto no futuro.
"""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.abspath('/data/database-post.db')

from sqlite3 import OperationalError

class SiteConfig:
    @staticmethod
    def get(key, default=None):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute('SELECT value FROM site_config WHERE key=?', (key,))
            row = cur.fetchone()
            conn.close()
            return row[0] if row else default
        except OperationalError:
            return default

    @staticmethod
    def set(key, value):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute('INSERT OR REPLACE INTO site_config (key, value) VALUES (?, ?)', (key, value))
            conn.commit()
            conn.close()
            return True
        except OperationalError:
            return False

# Helper para posts (uso via sqlite3 direto; manter compatibilidade com o app atual)
class Post:
    @staticmethod
    def all(published_only=False):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            if published_only:
                cur.execute('SELECT * FROM posts WHERE published=1 ORDER BY created_at DESC')
            else:
                cur.execute('SELECT * FROM posts ORDER BY created_at DESC')
            rows = cur.fetchall()
            conn.close()
            return rows
        except OperationalError:
            return []

    @staticmethod
    def get(post_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM posts WHERE id=?', (post_id,))
            row = cur.fetchone()
            conn.close()
            return row
        except OperationalError:
            return None


# SQLAlchemy model (opcional) — adicionado para permitir db.create_all sem alterar helpers existentes
try:
    from app import db
    class PostSQL(db.Model):
        __tablename__ = 'posts'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.Text, nullable=False)
        content = db.Column(db.Text, nullable=False)
        published = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
except Exception:
    # db pode não estar disponível em tempo de importação (p.ex. durante testes); continuar sem erro
    pass

