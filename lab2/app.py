from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    app_name = os.environ.get('APP_NAME', 'Unknown App')
    return f"Hello from {app_name} (Container: {os.environ.get('HOSTNAME', 'Unknown')})!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port)