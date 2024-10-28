import os
from flask import Flask
import threading
from socket_server import start_server

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Bulletin Board System!"

def run_socket_server():
    host = os.getenv("SOCKET_SERVER_HOST", "localhost")
    port = int(os.getenv("SOCKET_SERVER_PORT", 12345))
    start_server(host, port)

if __name__ == "__main__":
    # Start the socket server in a separate thread
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()
    
    # Start the Flask application
    app.run(port=5000)