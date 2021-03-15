# CS 371 Project 1 Question 3
# Author:
#   Joshua Kaiser
# Description:
#   A simple web server that will be run on localhost. The server receives messages on port 12000 and responds to any
# Notes:
#
# Citations:
#   Computer Networks by Kurose and Ross Pg. 168-169
#   My submission of CS 372 Project: Sockets and HTTP
#   https://docs.python.org/3.4/howto/sockets.html
#   https://realpython.com/python-sockets/
import socket


def get_message(connectionSocket):
    """
    Params:
    Returns:
    Notes:
    """
    # Get message length
    header = connectionSocket.recv(8)
    if header == b'':
        return ''
    msg_length = int(header.decode())
    # Get rest of message
    incoming = connectionSocket.recv(msg_length)
    if incoming == b'':
        return ''
    return incoming.decode()


def send_message(server_socket, msg):
    """
    Params:
    Returns:
    Notes:
    """
    # For testing
    coded_msg = msg.encode()
    coded_msg_len = len(coded_msg)

    coded_msg_str_len = len(str(coded_msg_len))
    header = '0' * (8 - coded_msg_str_len) + str(coded_msg_len)
    msg = header + msg
    # Send the encoded message to the server
    sent = server_socket.send(msg.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")


def is_quit(message):
    """
    returns:
        True if the the string is the quit command, False otherwise
    """
    quit_string = '/q'
    if message == quit_string:
        return True
    else:
        return False


# Create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to localhost and a specified port (12000)
ip = '127.0.0.1'
serverPort = 15000
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((ip, serverPort))


# Accept one client at a time
serverSocket.listen(1)

# Show server is running in CLI
print('Server listening on: ', ip, ':', serverPort, sep='')

first_connection = True
first_message = True
connection_is_alive = False

# Keep accepting connections while the server is running
while True:
    if not connection_is_alive:
        # Accept a connection
        connectionSocket, addr = serverSocket.accept()
        connection_is_alive = True

    if first_connection:
        print("connected by", addr)
        print("Waiting for message...")
        first_connection = False

    # Read incoming message
    incoming = get_message(connectionSocket)

    if is_quit(incoming):
        connectionSocket.close()
        break
    elif incoming == '':
        connection_is_alive = False
    else:
        # Print message received from client
        print(incoming)

    # Print prompt for the first message received
    if first_message:
        print("Type /q to quit")
        print("Enter message to send...")
        first_message = False

    if connection_is_alive:
        # Get message be sent sent back to client
        msg = input("> ")

        # Send message to client
        send_message(connectionSocket, msg)

        if is_quit(msg):
            # Close the connection
            connectionSocket.close()
            break
