import json
import socket
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Dictionary to store device data
devices = {}

# TCP server configuration
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

def start_tcp_server():
    """Start a TCP server to receive data."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(1)

    print(f"TCP server listening on {TCP_IP}:{TCP_PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from: {addr}")
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if data:
            print(f"Received data: {data}")
            update_devices(data)
        conn.close()

def update_devices(data):
    """Update devices dictionary with received data."""
    global devices
    try:
        # Assuming data is received in JSON format
        parsed_data = json.loads(data)
        devices.update(parsed_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    return jsonify(devices)

if __name__ == '__main__':
    # Start TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()

    # Start Flask app
    app.run(debug=True)
