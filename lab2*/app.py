from flask import Flask
import os

app = Flask(__name__)
compose_file = os.environ.get("COMPOSE_FILE_NAME", "unknown")

@app.route('/')
def hello():
    return f"Hello from {compose_file}!\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)