from flask import Flask
import socket
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <html>
        <head>
            <title>Canary Release</title>
        </head>
        <body style="background-color: lightblue">
            <p>Hello, World! I am at {socket.gethostname()}</p>
        </body>
    </html>"""
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)