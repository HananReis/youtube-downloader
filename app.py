import os
import sqlite3
from sqlite3 import OperationalError
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
import uuid

# Caminho fixo do banco (arquivo no volume de dados do ambiente, ex: Railway)
# Usar /data/database-post.db (ABSOLUTO) para persistência em platform volumes
DB_PATH = '/data/database-post.db'
# Garantir que a pasta exista (silenciar erros de permissão quando não aplicável)
try:
    os.makedirs('/data', exist_ok=True)
except PermissionError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Credenciais do admin (usar variáveis de ambiente em produção)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')

# Configurar SQLAlchemy para usar o arquivo no volume de dados (/data)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/database-post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Inicializar SQLAlchemy (não criar tabelas automaticamente aqui)
db = SQLAlchemy(app)


# ============ FUNÇÕES AUXILIARES ============

def get_db():
    """Conectar ao banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorator para proteger rotas admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_all_posts(published_only=False):
    """Obter todos os posts"""
    conn = get_db()
    cursor = conn.cursor()
    
    if published_only:
        cursor.execute('SELECT * FROM posts WHERE published=1 ORDER BY created_at DESC')
    else:
        cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')
    
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    """Obter um post específico"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id=?', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

def create_post(title, content, published=False):
    """Criar novo post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO posts (title, content, published, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
        (title, content, published, datetime.now(), datetime.now())
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def update_post(post_id, title, content, published):
    """Atualizar um post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE posts SET title=?, content=?, published=?, updated_at=? WHERE id=?',
        (title, content, published, datetime.now(), post_id)
    )
    conn.commit()
    conn.close()

def delete_post(post_id):
    """Deletar um post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id=?', (post_id,))
    conn.commit()
    conn.close()

# ============ ROTAS PÚBLICAS ============

@app.route("/")
def index():
    """Página inicial com posts publicados"""
    posts = get_all_posts(published_only=True)
    return render_template("index.html", posts=posts)

@app.route("/modelos")
def modelos():
    return render_template("paginas/modelos.html")

@app.route("/informacoes")
def informacoes():
    return render_template("paginas/informacoes.html")

@app.route("/contato")
def contato():
    return render_template("paginas/contanto.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ============ ROTAS DE AUTENTICAÇÃO ============

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        
        if user == ADMIN_USER and password == ADMIN_PASS:
            session['user'] = user
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=7)
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template("login.html", error="Usuário ou senha incorretos")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Fazer logout"""
    session.clear()
    return redirect(url_for('index'))

# ============ ROTAS DE ADMIN ============

@app.route("/admin")
@login_required
def admin_dashboard():
    """Dashboard de admin - listar todos os posts"""
    posts = get_all_posts(published_only=False)
    return render_template("admin/dashboard.html", posts=posts)

@app.route("/admin/new", methods=['GET', 'POST'])
@login_required
def admin_create():
    """Criar novo post"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        published = request.form.get('published') == 'on'
        
        if not title or not content:
            return render_template("admin/create.html", error="Título e conteúdo são obrigatórios")
        
        create_post(title, content, published)
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin/create.html")

@app.route("/admin/edit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def admin_edit(post_id):
    """Editar um post"""
    post = get_post_by_id(post_id)
    
    if not post:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        published = request.form.get('published') == 'on'
        
        if not title or not content:
            return render_template("admin/edit.html", post=post, error="Título e conteúdo são obrigatórios")
        
        update_post(post_id, title, content, published)
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin/edit.html", post=post)

@app.route("/admin/delete/<int:post_id>", methods=['POST'])
@login_required
def admin_delete(post_id):
    """Deletar um post"""
    delete_post(post_id)
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/publish/<int:post_id>", methods=['POST'])
@login_required
def admin_publish(post_id):
    """Publicar/Despublicar um post"""
    post = get_post_by_id(post_id)
    if post:
        new_state = 1 if post['published'] == 0 else 0
        update_post(post_id, post['title'], post['content'], new_state)
    return redirect(url_for('admin_dashboard'))


# ------- SiteConfig helpers (não criam tabelas automaticamente) -------
def get_config(key, default=None):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT value FROM site_config WHERE key=?', (key,))
        row = cur.fetchone()
        conn.close()
        return row['value'] if row else default
    except OperationalError:
        return default


def set_config(key, value):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO site_config (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()
        return True
    except OperationalError:
        return False


# ------- Upload de imagens via editor -------
@app.route('/admin/upload_image', methods=['POST'])
@login_required
def admin_upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400

    ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
    filename = secure_filename(file.filename)
    if '.' not in filename:
        return jsonify({'error': 'Extensão inválida'}), 400
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({'error': 'Extensão não permitida'}), 400

    os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'uploads'), exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads', unique_name)
    file.save(save_path)

    url = url_for('static', filename=f'uploads/{unique_name}')
    return jsonify({'url': url}), 200


# ------- Controle de tamanho de fonte -------
@app.route('/admin/font_size', methods=['POST'])
@login_required
def admin_font_size():
    action = request.form.get('action')
    current = get_config('font_size', '18px')
    try:
        current_value = int(''.join(filter(str.isdigit, current)))
    except Exception:
        current_value = 18

    if action == 'increase':
        current_value += 1
    elif action == 'decrease':
        current_value = max(12, current_value - 1)
    elif action == 'reset':
        current_value = 18
    else:
        return redirect(url_for('admin_dashboard'))

    set_config('font_size', f"{current_value}px")
    return redirect(url_for('admin_dashboard'))


# ------- Controle de família de fonte -------
@app.route('/admin/font_family', methods=['POST'])
@login_required
def admin_font_family():
    family = request.form.get('font_family', '').strip()
    if not family:
        return redirect(url_for('admin_dashboard'))
    allowed = ['Arial', 'Times New Roman', 'Verdana', 'Georgia']
    if family not in allowed:
        return redirect(url_for('admin_dashboard'))
    set_config('font_family', family)
    return redirect(url_for('admin_dashboard'))


# ------- Injetar variáveis de fonte em todos os templates -------
@app.context_processor
def inject_site_font_size():
    fs = get_config('font_size', '18px')
    family = get_config('font_family', 'Times New Roman')
    return dict(site_font_size=fs, site_font_family=family)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Visualizar post completo"""
    post = get_post_by_id(post_id)
    if not post or post['published'] == 0:
        return render_template('index.html'), 404
    return render_template('post.html', post=post)

# Nota: criação de tabelas é feita manualmente via `init_db.py`.
# Não criar ou recriar tabelas automaticamente na inicialização do app (evita perda de dados).


# ============ TRATAMENTO DE ERROS ============

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("index.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
