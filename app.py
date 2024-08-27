import json
import socket
import threading
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Dictionary to store device data
devices = {}

BUFFER_SIZE = 1028

def handle_device_connection(ip, port):
    """Connect to the hardware's TCP server and receive data."""
    global devices

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))

            while True:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if data:
                    print(f"Received data from {ip}:{port} - {data}")
                    # Process the received data
                    if "Band connected" in data or "Band disconnected" in data:
                        devices[ip]['BAND_STATUS'] = 1 if "Band connected" in data else 0
                    elif "Mat connected" in data or "Mat disconnected" in data:
                        devices[ip]['MAT_STATUS'] = 1 if "Mat connected" in data else 0

                    # Update ESD status
                    esd_status = "Safe" if devices[ip].get('BAND_STATUS') == 1 and devices[ip].get('MAT_STATUS') == 1 else "Unsafe"
                    devices[ip]['ESD_STATUS'] = esd_status

        except Exception as e:
            print(f"Error with {ip}:{port} - {e}")
        finally:
            client_socket.close()

@app.route('/')
def index():
    return render_template('final.html')

@app.route('/data')
def get_data():
    return jsonify(devices)

@app.route('/add_device', methods=['POST'])
def add_device():
    """Add a new device by IP and Port."""
    global devices
    ip = request.form.get('device_ip')
    port = int(request.form.get('device_port'))

    if ip and port:
        devices[ip] = {
            'BAND_STATUS': 0,
            'MAT_STATUS': 0,
            'ESD_STATUS': 'Unsafe'
        }
        threading.Thread(target=handle_device_connection, args=(ip, port), daemon=True).start()
        return jsonify({"message": f"Device {ip}:{port} added successfully!"}), 200
    else:
        return jsonify({"error": "Device IP and Port are required!"}), 400

@app.route('/remove_device/<device_ip>', methods=['DELETE'])
def remove_device(device_ip):
    """Remove a device by IP."""
    global devices
    if device_ip in devices:
        del devices[device_ip]
        return jsonify({"message": f"Device {device_ip} removed successfully!"}), 200
    else:
        return jsonify({"error": "Device not found!"}), 404

@app.route('/connect_device/<device_ip>', methods=['POST'])
def connect_device(device_ip):
    """Connect to a device by IP."""
    global devices
    if device_ip in devices:
        # Start connection handling thread
        threading.Thread(target=handle_device_connection, args=(device_ip, devices[device_ip]['port']), daemon=True).start()
        return jsonify({"message": f"Device {device_ip} connected successfully!"}), 200
    else:
        return jsonify({"error": "Device not found!"}), 404

if __name__ == '__main__':
    # Start Flask app
    app.run(debug=True)
