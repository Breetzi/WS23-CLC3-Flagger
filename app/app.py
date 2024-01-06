from flask import Flask
import socket
app = Flask(__name__)

@app.route('/')
def home():
    return f"<p>Hello, World! I am at {socket.gethostname()}</p>"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)