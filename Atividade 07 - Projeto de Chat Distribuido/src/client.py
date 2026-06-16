# CLIENT

import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from sys import exit
from time import sleep

HOST = "192.168.1.101"
PORT = 5000

# ==========

# Asking server IP & Handle the user's choice
askIP = messagebox.askyesno(title="Entrar IP?", message="Você gostaria de entrar um IP?\t")

if askIP:
    HOST = simpledialog.askstring("Entre um IP", "Enter server IP:")

# ==========
# Ask user name
while True:
    try:
        username = (simpledialog.askstring("Nome", "Enter your name:\t\t\t\t")).strip()
    except Exception as e:
        print(e)
        messagebox.showinfo("Error!", e)
        exit(0)

    if username == "":
        messagebox.showinfo("Atenção!", "Seu nome não pode ser vazio!")
    elif len(username) < 3:
        messagebox.showinfo("Atenção!", "Seu nome não ter menos que 3 catacteres!")
    else:
        break

# ==========

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

# ==========

# Send name first
client.send(username.encode())

window = tk.Tk()
window.title(f"Projeto de Chat Distribuido (Atividade 07) - {username}")

chatArea = ScrolledText(window)
chatArea.configure(state="disabled")
chatArea.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

chatEntry = tk.Entry(window)
chatEntry.pack(
    padx=10,
    pady=10,
    fill=tk.X
)

def insertToChatArea(message):
    chatArea.configure(state="normal")
    chatArea.insert(tk.END, message + "\n")
    chatArea.configure(state="disabled")

def receiveMessages():
    while True:
        try:
            message = client.recv(1024).decode()

            insertToChatArea(message)
            chatArea.see(tk.END)

        except:
            break

def processCommand(command):
    if command == "/ajuda":
        insertToChatArea("-" * 10 + "\n" +
                         "SERVER: Comandos do aplicativo:" + "\n" +
                         "/ajuda \t\t - Lista os comandos do sistema." + "\n" +
                         "/limpar \t\t - Limpa a caixa de mensagens." + "\n" +
                         "/sair \t\t - Encerra a aplicação do usuário." + "\n" +
                         "-" * 10
                         )
    elif command == "/limpar":
        chatArea.configure(state="normal")
        chatArea.delete("1.0", tk.END)
        chatArea.configure(state="disable")
    elif command == "/sair":
        insertToChatArea("SERVER: Desconectando...")
        client.close();
        window.destroy()
        exit(0)
    else:
        insertToChatArea(f"SERVER: Comando não reconhecido: {command}")


def sendMeessage(event=None):
    message = chatEntry.get().strip()

    if message.strip() == "":
        return
    if message.startswith("/"):
        processCommand(message)
        chatEntry.delete(0, tk.END)
        return

    fullMessage = f"{username}: {message}"
    client.send(fullMessage.encode())
    chatEntry.delete(0, tk.END)


chatEntry.bind("<Return>", sendMeessage)

sendButton = tk.Button(
    window,
    text="Enviar",
    command=sendMeessage
)
sendButton.pack(pady=5)

thread = threading.Thread(
    target=receiveMessages,
    daemon=True
)
thread.start()

window.mainloop()
