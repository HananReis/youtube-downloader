from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("index.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
