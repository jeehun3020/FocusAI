from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # ✅ CORS 허용 추가

@app.route("/start_focus", methods=["POST"])
def start_focus():
    try:
        subprocess.Popen(["python3", "FocusAI.py"])
        return jsonify({"status": "started", "message": "FocusAI monitoring started."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)