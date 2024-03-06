import socket
import threading
import sys 
import argparse

def start_client(server_ip, port, username, password):
    client_socket = socket.socket()
    client_socket.connect((server_ip, port))
    
    client_socket.send(password.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "Incorrect passcode":
        print(response)
        sys.stdout.flush()
        client_socket.close()
        return
    #print(response)
    sys.stdout.flush()
    client_socket.send(username.encode('utf-8'))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    send_message(client_socket)


def send_message(client_socket):
    while True:
        try:
            message = input()
            if message == ":Exit":
                client_socket.send(message.encode('utf-8'))
                client_socket.close()
                sys.exit()
                break
            client_socket.send(message.encode('utf-8'))
        except Exception:
            break

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            sys.stdout.flush()
        except Exception:
            sys.exit()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="chat room client")
    parser.add_argument("-join", action="store_true", help="join server")
    parser.add_argument("-host", type = str, help="Server IP address")
    parser.add_argument("-port", type=int, help="Server port")
    parser.add_argument("-username", type = str, help="Username")
    parser.add_argument("-passcode", type = str, help="Password to connect with server")
    args = parser.parse_args()

    #if args.host and args.port and args.username and args.passcode:
    start_client(args.host, args.port, args.username, args.passcode)

