from flask import Flask, render_template, abort

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
    return render_template('base.html', **{'content_template': template})

if __name__ == "__main__":
    app.run(debug=True)
