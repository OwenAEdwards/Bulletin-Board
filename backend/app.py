from flask import Flask
import threading
from socket_server import start_server

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Bulletin Board System!"

def run_socket_server():
    start_server('localhost', 12345)

if __name__ == "__main__":
    # Start the socket server in a separate thread
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()
    
    # Start the Flask application
    app.run(port=5000)