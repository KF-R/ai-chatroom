#!/usr/bin/env python3
## TCP AI Chat Room 
## (c) 2021-2023  Kerry Fraser-Robinson

import socket
import threading
import sys

def receive_messages(disconnect_event):
    try:
        while True:
            data = client.recv(1024)
            if not data:  # server closed the connection
                print("\nServer has disconnected. Closing the client.")
                disconnect_event.set()
                break

            # Clear the current line and move cursor to the beginning
            sys.stdout.write("\033[K")
            # Print the received message
            print('\n' + data.decode())
            # Reprint the prompt
            sys.stdout.write("> ")
            sys.stdout.flush()

    except socket.error:
        # This can happen if there's a network issue or the server forcibly closed the connection.
        print("\nConnection lost to the server. Closing the client.")
        disconnect_event.set()
    finally:
        client.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

username = input("Enter your username: ")
client.send(username.encode())  # Send username immediately after connection

disconnect_event = threading.Event()
threading.Thread(target=receive_messages, args=(disconnect_event,), daemon=True).start()

try:
    while True:
        msg = input("> ")
        if disconnect_event.is_set():
            break
        if not msg:
            continue  # Skip sending empty messages
        client.send(msg.encode())
except (KeyboardInterrupt, EOFError, socket.error):
    print("\nClosing the client.")
    client.close()
    sys.exit(0)  # exit the client program

if disconnect_event.is_set():
    print("Disconnect event detected. Exiting...")
    sys.exit(0)
