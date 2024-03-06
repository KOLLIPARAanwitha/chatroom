import socket
import threading
import sys 
import datetime
import argparse

# Use sys.stdout.flush() after print statements
allClients = {}

def handle_command(data, client_address, client_socket):
    global allClients
    command = data.split(" ")[0]
    if command == ":)":
        message = f"{allClients[client_address][0]}: [feeling happy]"
        print(f"{allClients[client_address][0]}: [feeling happy]")
        sys.stdout.flush()
        broadcast(message, client_address, client_socket)
    elif command == ":(":
        message = f"{allClients[client_address][0]}: [feeling sad]"
        print(f"{allClients[client_address][0]}: [feeling sad]")
        sys.stdout.flush()
        broadcast(message, client_address, client_socket)
    elif command == ":mytime":
        time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        print(f"{allClients[client_address][0]}: {time}")
        sys.stdout.flush()
        broadcast(f"{allClients[client_address][0]}: {time}", client_address, client_socket)
    elif command == ":+1hr":
        one_hour = datetime.datetime.now() + datetime.timedelta(hours = 1)
        time = one_hour.strftime("%a %b %d %H:%M:%S %Y")
        print(f"{allClients[client_address][0]}: {time}")
        sys.stdout.flush()
        broadcast(f"{allClients[client_address][0]}: {time}", client_address, client_socket)
    elif command == ":dm":
        receiver_username = data.split(" ")[1]
        message = ' '.join(data.split(" ")[2:])
        print(f"{allClients[client_address][0]} to {receiver_username}: {message}")
        sys.stdout.flush()
        direct_message(message, client_address, receiver_username)
    elif command == ":Exit":
        message = f"{allClients[client_address][0]} left the chatroom"
        broadcast(message, client_address, client_socket)
        del allClients[client_address]
        return False
    return True

def handle_client(client_socket, client_address):
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if data.startswith(":"):
                    if not handle_command(data, client_address, client_socket):
                        return
                    
                else:
                    print(f"{allClients[client_address][0]}: {data}")
                    sys.stdout.flush()
                    broadcast(f"{allClients[client_address][0]}: {data}", client_address, client_socket)
            except Exception:
                break
        

def broadcast(message, client_address, client_socket):
    #global allClients
    sent_from = allClients[client_address][0]
    for address, sock in allClients.items():
        if address != client_address:
            allClients[address][1].send(f"{message}".encode('utf-8'))

def direct_message(message, client_address, receiver_username):
    #global allClients
    sent_from = allClients[client_address][0]
    for address, sock in allClients.items():
        if allClients[address][0] == receiver_username:
            allClients[address][1].send(f"{sent_from}: {message}".encode('utf-8'))

def start_server(port, passcode):
    global allClients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on port {port}. Accepting connections")
    sys.stdout.flush()
    while True:
        client_socket, client_address = server.accept()
        client_passcode = client_socket.recv(1024).decode('utf-8')
        if passcode == client_passcode:
            client_socket.send("Passcode accepted".encode('utf-8'))
            client_name = client_socket.recv(1024).decode('utf-8')
            print(f"{client_name} joined the chatroom")
            sys.stdout.flush()
            allClients[client_address] = (client_name, client_socket)
            
            client_socket.send(f"Connected to 127.0.0.1 on port {port}".encode('utf-8'))
            broadcast(f"{client_name} joined the chatroom", client_address, client_socket)
            client = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client.start()
        else:
            client_socket.send("Incorrect passcode".encode('utf-8'))
            #client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat server")
    parser.add_argument("-start", action="store_true", help="Start server")
    parser.add_argument("-port", type=int, help="Port")
    parser.add_argument("-passcode", type = str, help="Passcode to connect clients")
    args = parser.parse_args()

    if args.start and args.port and args.passcode:
        start_server(args.port, args.passcode)
    else:
        print("Error")
        sys.stdout.flush()
