#!/usr/bin/env python3
## TCP AI Chat Room 
## (c) 2021-2023  Kerry Fraser-Robinson

import socket
import threading

def broadcast(message, sending_client=None, clients={}):
    """ This function broadcasts a message to all connected users. """
    with clients_lock:
        for client_socket in clients.keys():
            if client_socket != sending_client:  # Exclude sending client from broadcast
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"> Error broadcasting to a client: {e}")

def handle_client(client_socket, username, clients, shutdown_event):
    client_socket.settimeout(1)  # Set timeout for recv method
    try:
        while not shutdown_event.is_set():
            try:
                msg = client_socket.recv(1024).decode()
                if not msg:
                    break

                if username == 'SysOp' and msg == '/shutdown':
                    print("\n> Remote shutdown requested.")
                    shutdown_event.set()
                    break

                broadcast_msg = f"{username}: {msg}"
                if(msg!='<listens>'): broadcast(broadcast_msg, client_socket, clients)
                print(f"{broadcast_msg}")
            except socket.timeout:
                pass

    except Exception as e:
        print(f"> Error with client {username}: {e}")
    finally:
        broadcast(f"> {username} has disconnected", client_socket, clients)
        with clients_lock:
            del clients[client_socket]
        client_socket.close()
        print(f"> {username} has disconnected")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    server.settimeout(1)  # Set timeout for accept method
    
    clients = {}
    shutdown_event = threading.Event()

    print("> Server started, waiting for clients...")
    
    try:
        while not shutdown_event.is_set():
            try:
                client_sock, addr = server.accept()
                client_username = client_sock.recv(1024).decode() 
                with clients_lock:
                    clients[client_sock] = client_username
                broadcast(f"> {client_username} has connected", client_sock, clients)
                thread = threading.Thread(target=handle_client, args=(client_sock, client_username, clients, shutdown_event))
                thread.start()
                print(f"> {client_username} has connected")
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print("\n> Shutting down the server due to keyboard interrupt...")
        shutdown_event.set()

    # Graceful shutdown
    with clients_lock:
        for client_socket in clients.keys():
            client_socket.close()
    server.close()

if __name__ == "__main__":
    clients_lock = threading.Lock()
    start_server()
