import socket
import threading

HOST = 'localhost'
PORT = 12345
SHUTDOWN_MESSAGE = "Server is shutting down."

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to the chat server. Type 'exit' to quit.")

# Flag to indicate whether the client should continue running
running = True

# Function to send messages and handle user input
def send_messages():
    global running
    while running:
        message = input()  # Blocking call to get user input
        if message.lower() == "exit":
            print("Disconnecting from chat...")
            if running:
                client_socket.sendall("exit".encode('utf-8'))
                running = False  # Signal the other thread to stop
            else:
                return
        else:
            client_socket.sendall(message.encode('utf-8'))

# Thread for receiving messages
def receive_messages():
    global running
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == SHUTDOWN_MESSAGE:  # Check for exact shutdown message
                print("Server has shut down. Type exit to close the program.")
                running = False  # Signal the send thread to stop
                return
            elif message:
                print(message)
        except Exception as e:
            if not running:
                return  # Exit if shutdown is initiated
            print(f"Error receiving message: {e}")
            return

# Start threads for sending and receiving
send_thread = threading.Thread(target=send_messages)
receive_thread = threading.Thread(target=receive_messages)

send_thread.start()
receive_thread.start()

# Ensure both threads are joined before exiting


receive_thread.join()
send_thread.join()

client_socket.close()
print("Chat closed.")
