import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

HOST = "192.168.1.101"
PORT = 5000

# Asking server IP & Handle the user's choice
askIP = messagebox.askyesno(title="Entrar IP?", message="Você gostaria de entrar um IP?\t")

if askIP:
    HOST = simpledialog.askstring("Entre um IP", "Enter server IP:")


# Ask user name
username = simpledialog.askstring(
    "Name",
    "Enter your name:"
)

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

# Send name first
client.send(username.encode())

window = tk.Tk()
window.title(f"Projeto de Chat Distribuido (Atividade 07) - {username}")

chatArea = ScrolledText(window)
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


def receiveMessages():
    while True:
        try:
            message = client.recv(1024).decode()

            chatArea.insert(tk.END, message + "\n")
            chatArea.see(tk.END)

        except:
            break


def sendMeessage(event=None):
    message = chatEntry.get()

    if message.strip() == "":
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
