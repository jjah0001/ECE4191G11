import socket
from cryptography.fernet import Fernet
import threading


def Server():
    # Generate private keys to send to clients
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    # Set up a socket using AF_INET interface, streaming protocol (TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_address = '127.0.0.1'  # Replace with actual machine it is on
    port = 12345
    # Bind socket to address and port
    server_socket.bind((host_address, port))
    # Queue up 2 connections at a time
    server_socket.listen(2)
    clients = []

    def handle_client(client_socket):
        client_socket.send(key)
        while True:
            try:
                # Receive an encrypted message from the client_socket
                encrypted_message = client_socket.recv(1024)
                # Broadcast the message to all other clients
                for client in clients:
                    if client != client_socket:
                        client.send(encrypted_message)
            except Exception as e:
                break

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        # Start a thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

Server()