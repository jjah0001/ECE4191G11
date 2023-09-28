import socket
from cryptography.fernet import Fernet
import threading

'''
1. Create 1 server
2. Create 2 clients
    - Store the two client's IP Address / Device Address
3. Both clients will receive a key from the server so that
    both of them can encrypt and decrypt messages to and from the server.
4. Each client will send their message to the central server and then
    the server will send their message to the other client.
5. Send and Receive JSON Data in the form of:
    JSON_Message: {
        "location": [x, y],
        "status": "IDLE, MOVING, LOADING, UNLOADING",
        "bin_number": [1, 2, 3]
        "current_path": [LIST[x, y]]
    }
6. Use json.dumps(message) then encrypt then send (Central server does not need
    to decrypt the message as it is being sent to the other client)
'''

# Generate a secret key for encryption (keep secret)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Set up a socket using AF_INET interface, streaming protocol (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_address = '127.0.0.1'  # Replace this with your actual IP Address, otherwise you will only accept local com
port = 12345  # Replace with a suitable port

# Bind socket to address and port
server_socket.bind((host_address, port))

# Queue up 2 connections at a time
server_socket.listen(2)

clients = []


def handle_client(client_socket):
    print("hi")
    client_socket.send(key)

    while True:
        try:
            # Receive an encrypted message from the client
            # print("Waiting For Message From CLIENT...")
            encrypted_message = client_socket.recv(1024)
            # print(encrypted_message)
            # Decrypt the message
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

            if not decrypted_message:
                break

            print(f"Received: {decrypted_message}")

            # Encrypt a response
            response = input("Enter a message to send back: ")

            # print("Encrypting Message...")
            encrypted_response = cipher_suite.encrypt(response.encode())

            # Send the encrypted response to the client
            # print("Sending Encrypted Message to CLIENT...")
            client_socket.send(encrypted_response)
            # print("MESSAGE SENT")

        except Exception as e:
            print(f"Error: {str(e)}")
            break

    # Remove the client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()


print("Server is listening...")
while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    clients.append(client_socket)

    # Start a thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
