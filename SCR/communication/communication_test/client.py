import socket
from cryptography.fernet import Fernet

# Set up a socket using AF_INET interface, streaming protocol (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_address = '127.0.0.1'  # Replace this with your actual IP Address, otherwise you will only accept local com
port = 12345  # Replace with a suitable port

# Try to connect to server
client_socket.connect((host_address, port))
print("CONNECTED TO SERVER")
# First received message is the key
key = client_socket.recv(1024)
print("RECEIVED KEY")
cipher_suite = Fernet(key)

while True:
	# Ask user to enter text to send
	message = input("Enter a message to send to the server: ")

	# Encrypt the message
	# print("Encrypting Message...")
	encrypted_message = cipher_suite.encrypt(message.encode())

	# Send the encrypted message to the server
	# print("Sending Encrypted Message to Server")
	client_socket.send(encrypted_message)
	# print("MESSAGE SENT")

	if message.lower() == 'exit':
		break

	# Receive and decrypt the server's response
	# print("Waiting for Server Response...")
	encrypted_response = client_socket.recv(1024)
	decrypted_response = cipher_suite.decrypt(encrypted_response).decode()

	print(f"Server says: {decrypted_response}")

# Close connection
client_socket.close()
