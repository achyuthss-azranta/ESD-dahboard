import json
from flask import Flask, render_template, jsonify # type: ignore
from flask_mqtt import Mqtt # type: ignore

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '127.0.0.1' 
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_CLIENT_ID'] = 'flask_app'

mqtt = Mqtt(app)

devices = {
    
}

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/mytopic')  

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global devices
    data = json.loads(message.payload.decode('utf-8'))
    devices.update(data)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    return jsonify(devices)

if __name__ == '__main__':
    app.run(debug=True)
