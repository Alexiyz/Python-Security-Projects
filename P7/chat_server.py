import socket
import threading
import random
import sys

HOST = 'localhost'
PORT = 12345
MAX_CLIENTS = 16

clients = {}  # Dictionary to store client sockets and their nicknames

colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Black", "White"]
animals = ["Tiger", "Eagle", "Shark", "Lion", "Wolf", "Fox", "Bear", "Hawk"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CLIENTS)
print(f"Server started on {HOST}:{PORT}. Waiting for up to {MAX_CLIENTS} clients to connect.")

def generate_nickname():
    """Generate a unique nickname for each client by combining color and animal."""
    color = random.choice(colors)
    animal = random.choice(animals)
    return f"{color} {animal}"

# Broadcast a message to all connected clients
def broadcast_message(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")

# Handle individual client connection
def handle_client(client_socket, address):
    nickname = generate_nickname()
    clients[client_socket] = nickname
    welcome_message = f"User {nickname} has joined the chat."
    print(welcome_message)
    broadcast_message(welcome_message)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == "exit":  # Client disconnect command
                leave_message = f"User {nickname} has left the chat."
                print(leave_message)
                broadcast_message(leave_message)
                del clients[client_socket]
                client_socket.close()
                break
            elif message:
                formatted_message = f"{nickname}: {message}"
                print(f"({address}, {nickname}) sent: {message}")
                broadcast_message(formatted_message)
        except Exception as e:
            print(f"Error handling client {address} ({nickname}): {e}")
            break

# Admin thread to listen for "exit" command to shut down server
def server_admin():
    while True:
        command = input()
        if command.lower() == "exit":
            print("Shutting down server...")
            broadcast_message("Server is shutting down. Disconnecting all clients.")
            # Disconnect all clients
            for client_socket in clients.keys():
                try:
                    client_socket.sendall("Server is shutting down.".encode('utf-8'))
                    client_socket.close()
                except Exception as e:
                    print(f"Error closing client connection: {e}")
            clients.clear()
            server_socket.close()
            sys.exit(0)

# Main loop to accept incoming clients
def accept_clients():
    while True:
        try:
            client_socket, address = server_socket.accept()
            if len(clients) < MAX_CLIENTS:
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
                client_thread.start()
            else:
                print("Maximum users reached, waiting for slots to open.")
        except Exception as e:
            print("Server is shutting down.")
            break

# Start the server's main threads
admin_thread = threading.Thread(target=server_admin)
admin_thread.start()

accept_clients()  # Start accepting clients
