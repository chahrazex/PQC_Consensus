import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server hostname and port
host = socket.gethostname()
port = 12345

# Connect to the server
client_socket.connect((host, port))

while True:
    # Send data to server
    message = input("Enter message: ")
    client_socket.send(message.encode())

    # Receive response from server
    response = client_socket.recv(1024).decode()
    print("Received from server:", response)

# Close the connection
client_socket.close()
