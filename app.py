from flask import Flask, request, jsonify, send_from_directory, render_template
from downloader import baixar_video
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

# Rota principal (pra não dar Not Found)
@app.route("/")
def home():
    return render_template("index.html")

# Rota para baixar o vídeo (POST)
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL não enviada"}), 400

    url = data["url"]

    try:
        # garante que a pasta existe
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        # baixa o vídeo dentro da pasta downloads
        filename = baixar_video(url, DOWNLOAD_DIR)

        return jsonify({
            "status": "ok",
            "file": filename
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Rota para acessar o arquivo e baixar
@app.route("/file/<filename>")
def get_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
