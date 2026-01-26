from flask import Flask, request, jsonify, send_from_directory
from downloader import baixar_video
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL não enviada"}), 400

    url = data["url"]

    try:
        filename = baixar_video(url)
        return jsonify({
            "status": "ok",
            "file": filename
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/file/<filename>")
def get_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run()
