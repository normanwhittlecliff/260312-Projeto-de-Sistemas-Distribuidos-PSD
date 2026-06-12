import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clientes = []

# Função para enviar mensagem para todos
def broadcast(mensagem):
    for cliente in clientes:
        try:
            cliente["socket"].send(mensagem.encode())
        except:
            cliente["socket"].close()
            clientes.remove(cliente)

# Função que trata cada cliente
def tratar_cliente(cliente_socket, endereco):
    print(f"SERVER: Nova conexão: {endereco}")

    try:
        # Recebe o nome do cliente
        nome = cliente_socket.recv(1024).decode()

        cliente_info = {
            "socket": cliente_socket,
            "nome": nome
        }

        clientes.append(cliente_info)

        mensagem_entrada = f"SERVER: {nome} entrou no chat!"
        print(mensagem_entrada)
        broadcast(mensagem_entrada)

        while True:
            mensagem = cliente_socket.recv(1024).decode()

            if not mensagem:
                break

            mensagem_formatada = f"{nome}: {mensagem}"

            print(mensagem_formatada)

            broadcast(mensagem_formatada)

    except:
        print(f"SERVER: {endereco} desconectado.")

    finally:
        cliente_socket.close()

        # Remove cliente da lista
        for cliente in clientes:
            if cliente["socket"] == cliente_socket:
                clientes.remove(cliente)
                break

        mensagem_saida = f"SERVER: {nome} saiu do chat."
        print(mensagem_saida)
        broadcast(mensagem_saida)

# Configuração do servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"SERVER: Servidor iniciado na porta {PORT}")

while True:
    cliente_socket, endereco = servidor.accept()

    thread = threading.Thread(
        target=tratar_cliente,
        args=(cliente_socket, endereco)
    )

    thread.start()
