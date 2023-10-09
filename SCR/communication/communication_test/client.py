import socket
from cryptography.fernet import Fernet
import json
import random
import threading
import time

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

#Location
#Status
#Bin
#Path

JSON_object = {"robot_id": client_socket.getsockname(), "location": [2, 2], "status": "MOVING", "Bin": 1, "Path": [[2,2], [2, 6], [2, 12]]}
JSON_object_str_1 = json.dumps(JSON_object)

JSON_object = {"robot_id": client_socket.getsockname(), "location": [0, 0], "status": "Idle", "Bin": 2, "Path": [[0,0], [4, 6], [8, 12]]}
JSON_object_str_2 = json.dumps(JSON_object)

JSON_object = {"robot_id": client_socket.getsockname(), "location": [8, 12], "status": "UNLOADING", "Bin": 2, "Path": [[]]}
JSON_object_str_3 = json.dumps(JSON_object)

JSON_object = {"robot_id": client_socket.getsockname(), "location": [0, 6], "status": "LOADING", "Bin": 1, "Path": [[]]}
JSON_object_str_4 = json.dumps(JSON_object)

JSON_object_str_arr = [JSON_object_str_1, JSON_object_str_2, JSON_object_str_3, JSON_object_str_4]


# Function to continuously receive messages
def receive_messages(client_socket, cipher_suite):
    while True:
        try:
            # Attempt to receive a message from the server (non-blocking)
            encrypted_message = client_socket.recv(1024)

            if encrypted_message:
                # Decrypt and print the received message
                decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
                print(f"\nReceived from other Robot: {decrypted_message}")

        except Exception as e:
            # Handle exceptions (e.g., socket errors)
            print(f"Error: {str(e)}")
            break


# Start a thread to continuously receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cipher_suite))
receive_thread.daemon = True  # Allow the thread to exit when the main program ends
receive_thread.start()

client_send = input("Send Message? ")

if client_send == "Y":
	while True:
		# Ask user to enter text to send
		# location = input("Location: ")
		# status = input("Status: ")
		# bin = int(input("Bin: "))
		# path = input("Path: ")

		# Select a random index from the list
		random_index = random.choice(range(len(JSON_object_str_arr)))

		# Get the random JSON object string using the selected index
		random_JSON_object_str = JSON_object_str_arr[random_index]

		message = random_JSON_object_str

		# Encrypt the message
		# print("Encrypting Message...")
		encrypted_message = cipher_suite.encrypt(message.encode())

		# Send the encrypted message to the server
		# print("Sending Encrypted Message to Server")
		client_socket.send(encrypted_message)
		# print("MESSAGE SENT")
		time.sleep(3)

	# # Receive and decrypt the server's response
	# # print("Waiting for Server Response...")
	# encrypted_response = client_socket.recv(1024)
	# decrypted_response = cipher_suite.decrypt(encrypted_response).decode()
	# print(f"Received from other Robot: {decrypted_response}")

# Close connection
client_socket.close()
