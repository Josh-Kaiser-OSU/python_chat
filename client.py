# CS 371 Project 1
# Author:
#   Joshua Kaiser
# Description:
#   A simple web client using sockets
# Notes:
#
# Citations:
#   Computer Networks by Kurose and Ross Pg. 168-169
#   My submission of CS 372 Project: Sockets and HTTP
#   https://docs.python.org/3.4/howto/sockets.html
#   https://realpython.com/python-sockets/
import socket


def get_message(client_socket):
    """
    Params:
    Return:
        The string of the received message
    Notes:
    """
    # Get message length
    header = client_socket.recv(8)
    if header == b'':
        print("connection closed")
    msg_length = int(header.decode())
    # Get rest of message
    incoming = client_socket.recv(msg_length)
    if incoming == b'':
        print("connection closed")
    return incoming.decode()


def send_message(client_socket, msg):
    """
    Params:
    Returns:
    Notes:
    """
    coded_msg = msg.encode()
    coded_msg_len = len(coded_msg)

    coded_msg_str_len = len(str(coded_msg_len))
    header = '0' * (8 - coded_msg_str_len) + str(coded_msg_len)
    msg = header + msg

    # Send the encoded message to the server
    sent = client_socket.send(msg.encode())
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


# Server and port to request from
serverName = '127.0.0.1'
serverPort = 15000

first_connection = True


while True:
    # Establish a socket and connect it to the server name at the designated port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverName, serverPort))

    # Type prompt for the first message
    if first_connection:
        print("Connected to:", serverName, "on port:", serverPort)
        print("Type /q to quit")
        print("Enter message to send...")
        first_connection = False

    # Get user's message
    msg = input("> ")
    send_message(client_socket, msg)

    if is_quit(msg):
        # Close the connection
        client_socket.close()
        break

    # Receive the response and print it
    response = get_message(client_socket)
    if is_quit(response):
        client_socket.close()
        break
    print(response)
