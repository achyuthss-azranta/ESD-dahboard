import network
import machine
import time
from umqtt.simple import MQTTClient

def w5500_init():
    nic = network.WIZNET5K()
    nic.active(True)
    nic.ifconfig('dhcp')
    while not nic.isconnected():
        time.sleep(1)

def connect_mqtt(server, port, client_id):
    client = MQTTClient(client_id, server, port)
    client.connect()
    return client

def is_band_connected():
    band_status = machine.Pin(11, machine.Pin.IN).value()
    return band_status

def is_mat_connected():
    mat_status = machine.Pin(10, machine.Pin.IN).value()
    return mat_status

def main():
    # Initialize W5500 module
    w5500_init()

    # MQTT Broker details
    mqtt_server = '192.168.1.14'
    mqtt_port = 1883
    mqtt_client_id = 'YOUR_MQTT_CLIENT_ID'

    # Connect to MQTT broker
    mqtt_client = connect_mqtt(mqtt_server, mqtt_port, mqtt_client_id)

    try:
        while True:
            # Check Band status
            if is_band_connected():
                print('Band connected')
            else:
                print('Band disconnected')

            # Check Mat status
            if is_mat_connected():
                print('Mat disconnected')
            else:
                print('Mat connected')

            # Publish Band status to MQTT
            topic_band = 'topic/Band_Status'
            message_band = 'Band connected' if is_band_connected() else 'Band disconnected'
            mqtt_client.publish(topic_band, message_band)

            # Publish Mat status to MQTT
            topic_mat = 'topic/Mat_Status'
            message_mat = 'Mat disconnected' if is_mat_connected() else 'Mat connected'
            mqtt_client.publish(topic_mat, message_mat)

            # Delay for 1 second
            time.sleep(0.1)

    finally:
        # Disconnect from MQTT broker
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()