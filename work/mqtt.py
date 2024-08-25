from flask import Flask, jsonify, render_template # type: ignore
import paho.mqtt.client as mqtt # type: ignore
import threading

app = Flask(__name__)

devices = {}

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("device/+/status")

def on_message(client, userdata, msg):
    # Extract device ID and status type from the topic
    topic_parts = msg.topic.split('/')
    device_id = topic_parts[1]
    status_type = topic_parts[2]
    
    if device_id not in devices:
        devices[device_id] = {'matStatus': False, 'bandStatus': False}
    
    # Update the device's status based on the incoming message
    if status_type == "matStatus":
        devices[device_id]['matStatus'] = msg.payload.decode() == "online"
    elif status_type == "bandStatus":
        devices[device_id]['bandStatus'] = msg.payload.decode() == "online"
    
    # Print the updated device status
    print(f"Updated {device_id}: {devices[device_id]}")

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/status')
def status():
    return jsonify(devices)

def start_flask():
    app.run(host='0.0.0.0', port=5000)

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect("127.0.0.1", 1883, 60)

# Start the MQTT client loop in a separate thread
def start_mqtt():
    mqtt_client.loop_forever()

if __name__ == "__main__":
    threading.Thread(target=start_mqtt).start()
    start_flask()