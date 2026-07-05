from flask import Flask, request, jsonify
from flask_cors import CORS
from generator import generate_dockerfile

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "DockerGen API",
        "version": "v1",
        "status": "Running"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP"
    })

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    language = data.get("language")

    dockerfile = generate_dockerfile(language)

    return jsonify({
        "dockerfile": dockerfile
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)