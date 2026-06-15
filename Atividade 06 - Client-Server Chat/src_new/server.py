import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
names = []

# =========

# Create a temporary connection to find the primary network interface IP. I got thise method online to help me out
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually establish a connection, but triggers the routing layer
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        # Fallback method if not connected to any network
        local_ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return local_ip

print("Local IP Address:", get_local_ip())


# =========

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            removeClient(client)


def removeClient(client):
    if client in clients:
        index = clients.index(client)

        clients.remove(client)
        client.close()

        username = names[index]
        names.remove(username)

        print(f"SERVER: {username} disconnected.")

        # Some silly easter eggs.
        if username.lower() == "emily":
            broadcast(f"SERVER: {username} is away.")
        else:
            broadcast(f"SERVER: {username} disconnected.")


def handleClient(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            broadcast(message)

        except:
            break

    removeClient(client)


def receiveConnections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on port {PORT}")

    while True:
        client, address = server.accept()

        # First message = client name
        name = client.recv(1024).decode()

        clients.append(client)
        names.append(name)

        print(f"{name} connected from {address}")

        broadcast(f"SERVER: {name} joined the chat.")

        thread = threading.Thread(
            target=handleClient,
            args=(client,)
        )
        thread.start()


receiveConnections()
