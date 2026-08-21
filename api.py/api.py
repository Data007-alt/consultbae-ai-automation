from flask import Flask, jsonify
import subprocess
import sys

app = Flask(__name__)

@app.route("/run-pipeline", methods=["GET"])
def run_pipeline():
    try:
        result = subprocess.run(
            [sys.executable, "src/pipeline.py"],
            capture_output=True,
            text=True
        )

        return jsonify({
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "ConsultBae API is running"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)