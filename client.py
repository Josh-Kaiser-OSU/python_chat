# CS 371 Project 1
# Author:
#   Joshua Kaiser
# Description:
#   A simple web client using sockets
# Notes:
#
# Citations
#   Computer Networks by Kurose and Ross Pg. 166
#   My submission of CS 372 Project: Sockets and HTTP
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
    msg_length = int(header.decode())
    # Get rest of message
    incoming = client_socket.recv(msg_length)
    return incoming


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
    client_socket.send(msg.encode())


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
        print("Type /q to quit")
        print("Enter message to send...")
        first_connection = False

    # Get user's message
    msg = input("> ")
    send_message(client_socket, msg)

    # Receive the response and print it
    response = get_message(client_socket)
    print(response.decode())


# Close the connection
client_socket.close()
