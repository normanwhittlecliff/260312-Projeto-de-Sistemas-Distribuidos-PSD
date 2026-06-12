import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

# Recebe mensagens do servidor
def receber_mensagens(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode()

            if mensagem:
                print("\n" + mensagem)

        except:
            print("-CLIENT: Desconectado do servidor.")
            cliente.close()
            break

# Cria socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORT))

# Nome do usuário
while True:
    nome = input("-CLIENT: Digite seu nome:").strip()

    if nome == "":
        print("-CLIENT: O nome não pode ser vazio!")
    elif nome[0] == "-":
        print("-CLIENT: Primeiro caracter é inválido.")
    else:
        break

# Envia nome ao servidor
cliente.send(nome.encode())

# Thread para receber mensagens
thread_receber = threading.Thread(
    target=receber_mensagens,
    args=(cliente,)
)

thread_receber.start()

# Envio de mensagens
while True:
    mensagem = input(">").strip()
    
    if not mensagem == "" and mensagem[0] != "/":
        cliente.send(mensagem.encode())
    if mensagem.lower() == "/exit":
            break
    if mensagem.lower() == "/help":
            print("-CLIENT: Enter the following commands:" + "\n" +
                  "\n" +
                  "/exit  ->  Desconecta do servidor!" +
                  "\n")

cliente.close()
