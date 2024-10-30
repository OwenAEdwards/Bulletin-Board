import os
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import threading
from socket_server import start_server

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')  # Adjust path if needed
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files like JS, CSS
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'message': 'Welcome to the Bulletin Board System!'})

@socketio.on('bulletin_post')
def handle_bulletin_post(data):
    print(f"Received bulletin post: {data}")
    emit('bulletin_response', {'status': 'success', 'data': data}, broadcast=True)

def run_socket_server():
    host = os.getenv("SOCKET_SERVER_HOST", "localhost")
    port = int(os.getenv("SOCKET_SERVER_PORT", 12345))
    start_server(host, port)

if __name__ == "__main__":
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()
    socketio.run(app, port=5000)