import socket
import falcon

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and define a port
host = socket.gethostname()
port = 12345
sk = falcon.SecretKey(512)
pk = falcon.PublicKey(sk)
print(sk)
# Bind to the port
server_socket.bind((host, port))

# Listen for incoming connections (max of 1)
server_socket.listen(1)

print("Server is listening on {}:{}".format(host, port))

# Accept a connection from client
client_socket, client_address = server_socket.accept()

print("Connection established with", client_address)

while True:
    # Receive data from client
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print("Received from client:", data)

    # Send response back to client
    response = input("Enter response: ")
    client_socket.send(response.encode())

# Close the connection
client_socket.close()
server_socket.close()
