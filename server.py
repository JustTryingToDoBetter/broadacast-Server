import socket
import threading

host = "127.0.0.1" # localhost
port = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f"{name} left the chat!".encode("ascii"))
            names.remove(name)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NAME".encode("ascii"))
        name = client.recv(1024).decode("ascii")
        names.append(name)
        clients.append(client)

        print(f"name of client is {name}")
        broadcast(f"{name} joined the chat".encode("ascii"))
        client.send("conneted to server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start() 
    
print("Server is listening")
receive()