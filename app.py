import json
import socket
import threading
from flask import Flask, render_template, jsonify, request 

app = Flask(__name__)

# Dictionary to store device data
devices = {}

# TCP server configuration (from the hardware code)
TCP_IP = '192.168.1.2'  # Replace with the actual IP address of the W5500 module
TCP_PORT = 12345
BUFFER_SIZE = 1028

def start_hardware_client():
    """Connect to the hardware's TCP server and receive data."""
    global devices

    while True:
        try:
            # Create a socket to connect to the hardware's TCP server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((TCP_IP, TCP_PORT))

            while True:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if data:
                    print(f"Received data: {data}")
                    # Process the received data
                    if "Band connected" in data or "Band disconnected" in data:
                        devices['Band'] = {'BAND_STATUS': 1 if "Band connected" in data else 0}
                    elif "Mat connected" in data or "Mat disconnected" in data:
                        devices['Mat'] = {'MAT_STATUS': 1 if "Mat connected" in data else 0}
                    # Update ESD status
                    esd_status = "Safe" if devices.get('Band', {}).get('BAND_STATUS') == 1 and devices.get('Mat', {}).get('MAT_STATUS') == 1 else "Unsafe"
                    devices['ESD'] = {'ESD_STATUS': esd_status}

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/data')
def get_data():
    return jsonify(devices)

@app.route('/add_device', methods=['POST'])
def add_device():
    global devices
    data = request.json
    device_id = data.get('device_id')
    
    if device_id and device_id not in devices:
        devices[device_id] = {'MAT_STATUS': 0, 'BAND_STATUS': 0, 'ESD_STATUS': 'Unsafe'}
        return jsonify({'status': 'success', 'device_id': device_id}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Device already exists or invalid device ID'}), 400

if __name__ == '__main__':
    # Start the hardware client in a separate thread
    hardware_thread = threading.Thread(target=start_hardware_client)
    hardware_thread.daemon = True
    hardware_thread.start()

    # Start Flask app
    app.run(debug=True)
