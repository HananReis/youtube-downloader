from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)
