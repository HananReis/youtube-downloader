from flask import Flask, render_template, abort
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/page/<name>')
def page(name):
    mapping = {
        'index': 'index.html',
        'modelos': 'paginas/modelos.html',
        'informacoes': 'paginas/informacoes.html',
        'contato': 'paginas/contanto.html'
    }
    template = mapping.get(name)
    if not template:
        abort(404)
    
    try:
        # Renderizar o template completo
        html = render_template(template)
        
        # Extrair conteúdo entre <main id="main-content"> e </main>
        match = re.search(r'<main\s+id=["\']main-content["\'][^>]*>(.*?)</main>', html, re.DOTALL)
        
        if match:
            content = match.group(1)
            # Remove tags script que possam estar no conteúdo
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            return content
        
        return html
    except Exception as e:
        return f'<p>Erro ao carregar página: {str(e)}</p>', 500

if __name__ == "__main__":
    import os
    # Para Railway, a porta é definida pela variável de ambiente PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
