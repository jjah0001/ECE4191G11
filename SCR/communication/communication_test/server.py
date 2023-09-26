import socket
from cryptography.fernet import Fernet

# Generate a secret key for encryption (keep secret)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Set up a socket using AF_INET interface, streaming protocol (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_address = '127.0.0.1'  # Replace this with your actual IP Address, otherwise you will only accept local com
port = 12345  # Replace with a suitable port

# Bind socket to address and port
server_socket.bind((host_address, port))

# Queue up only 1 connection at a time
server_socket.listen(1)


try:
    # Accept incoming connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()

    while True:
        # Receive an encrypted message from the client
        encrypted_message = client_socket.recv(1024)

        # Decrypt the message
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

        if not decrypted_message:
            break

        print(f"Received: {decrypted_message}")

        # Encrypt a response
        response = input("Enter a message to send back: ")
        encrypted_response = cipher_suite.encrypt(response.encode())

        # Send the encrypted response to the client
        client_socket.send(encrypted_response)

except:
    print("Closing socket")
    # Close the client connection
    client.close()
    # Close the socket
    s.close()
