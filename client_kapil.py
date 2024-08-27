import socket

def tcp_client(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Attempting to connect to server {server_ip}:{server_port}...")
        print(f"Attempting to connect to server {server_ip}:{server_port}...")
        sock.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")

        while True:
            try:
                data = sock.recv(1024)
                if data:
                    print("Received:", data.decode())
                else:
                    print("Server closed the connection.")
                    break
            except socket.error as e:
                print(f"Error receiving data: {e}")
                break

    except socket.error as e:
        print(f"Connection failed: {e}")

    finally:
        sock.close()
        print("Connection closed.")

if _name_ == "_main_":
    server_ip = '192.168.0.101'  # Replace with the server's IP
    server_port = 12345          # Replace with the server's port
    tcp_client(server_ip, server_port)
