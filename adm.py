import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

# Configurações do servidor (máquina de testes)
SERVER_PORT = 443

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Client App")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.command_entry = tk.Entry(master, width=30)
        self.command_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Enviar Comando", command=self.send_command)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Cria um socket IPv4 e TCP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Inicia uma thread para conectar ao servidor
        threading.Thread(target=self.connect_to_server).start()

    def connect_to_server(self):
        try:
            # Conecta ao servidor (máquina de testes)
            self.client_socket.connect(("0.0.0.0", SERVER_PORT))
            self.display_text("Conexão estabelecida com sucesso!")

            # Inicia uma thread para receber feedback do servidor
            threading.Thread(target=self.receive_feedback).start()

        except Exception as error:
            self.display_text(f"Erro ao conectar ao servidor: {error}")

    def send_command(self):
        # Obtém o comando do usuário
        command = self.command_entry.get()

        # Envia o comando para o servidor
        try:
            self.client_socket.send(command.encode())
            self.display_text(f"Comando enviado: {command}")

        except Exception as error:
            self.display_text(f"Erro ao enviar comando: {error}")

        # Limpa a entrada de comando
        self.command_entry.delete(0, tk.END)

    def receive_feedback(self):
        try:
            while True:
                # Aguarda a resposta do servidor
                response = self.client_socket.recv(4096).decode()

                if not response:
                    break

                # Exibe o feedback na interface
                self.display_text(f"Resposta do servidor: {response}")

        except Exception as error:
            self.display_text(f"Erro ao receber feedback: {error}")

    def display_text(self, text):
        # Adiciona texto à área de texto
        self.text_area.insert(tk.END, text + "\n")
        # Auto rola para baixo
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
