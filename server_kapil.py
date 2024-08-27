import network
import machine
import time
import socket

def w5500_init():
    nic = network.WIZNET5K()
    nic.active(True)
    nic.ifconfig('dhcp')
    while not nic.isconnected():
        time.sleep(1)
    print("Connected with IP:", nic.ifconfig()[0])
    return nic.ifconfig()[0]

def is_band_connected():
    band_status = machine.Pin(11, machine.Pin.IN).value()
    return band_status

def is_mat_connected():
    mat_status = machine.Pin(10, machine.Pin.IN).value()
    return mat_status

def start_tcp_server(ip, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)
    print(f"Listening on {ip}:{port}")

    return sock

def main():
    # Initialize W5500 module and get IP address
    ip_address = w5500_init()

    # Define TCP/IP port for communication
    tcp_port = 12345

    # Start TCP/IP server
    server_socket = start_tcp_server(ip_address, tcp_port)

    try:
        while True:
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()
            print("Connection from", client_address)

            try:
                while True:
                    # Check Band status
                    band_status = 'Band connected' if is_band_connected() else 'Band disconnected'
                    print(band_status)
                    connection.sendall(band_status.encode())

                    # Check Mat status
                    mat_status = 'Mat disconnected' if is_mat_connected() else 'Mat connected'
                    print(mat_status)
                    connection.sendall(mat_status.encode())

                    # Delay for 1 second
                    time.sleep(0.5)

            finally:
                connection.close()

    finally:
        server_socket.close()

if __name__ == "_main_":
    main()