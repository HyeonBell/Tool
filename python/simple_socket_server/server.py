import socket
from _thread import *
import json



def global_logging(type_d, data):
    if type_d == "v":
        print("[*] VERBOSE :" + str(data))
    elif type_d == "i":
        print("[I] INFO :" + str(data))
    elif type_d == 'd':
        print("[D] DEBUG :" + str(data))
    elif type_d == "a":
        print("[A] AERLT :" + str(data))
    elif type_d == "e":
        print("[E] ERROR :" + str(data))
    else:
        print("로깅 예외")


class Menu:

    def __init__(self):
        self.menu = """Welcome, It's Problem Anwser Server.\n\n 1. Start up server\n 2. Exit
         
        """
        self.choice = None

    def show_menu(self):
        print(self.menu)

    def select_menu(self):
        self.choice = input("> ")

    def return_choice(self):
        return self.choice

class Server:
    def __init__(self):
        self.SERVER_IP = '127.0.0.1'
        self.SERVER_PORT = 8820
        self.server_data_buffer_size = 1024
        self.server_socket = None

    def __del__(self):

        # Closing communication
        if self.server_socket is not None:
            self.server_socket.close()

    def start_server(self):
        global_logging("v", "Start up Server")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        global_logging("v", "BIND IP")
        self.server_socket.bind((self.SERVER_IP, self.SERVER_PORT))
        self.server_socket.listen()
        global_logging("i", "Server State : listening")

    def thread_communication_main(self, client_socket, addr):
        global_logging("i", ("Connected by :" + str(addr[0]) + ":" + str(addr[1])))

        while True:
            try:
                data = client_socket.recv(self.server_data_buffer_size)
                if not data:
                    global_logging("i", ("Disconnected by " + str(addr[0]) + ":" + str(addr[1])))
                    break
                global_logging("i", ("Received from " + str(addr[0]) + ":" + str(addr[1]) + " data:" + data.decode()))

                client_socket.send(data)
            except ConnectionResetError as e:
                global_logging("i", ("Disconnected by " + str(addr[0]) + ":" + str(addr[1])))
                break
        client_socket.close()

    def run_loop(self):
        while True:
            global_logging("v", "Server State: Waiting for client")

            client_socket, addr = self.server_socket.accept()
            start_new_thread(self.thread_communication_main, (client_socket, addr))

    def received_data(self):
        pass

    def parsing_data(self):
        pass


if __name__ == "__main__":
    menu = Menu()
    server = Server()
    ch = None
    while True:
        menu.show_menu()
        menu.select_menu()
        ch = menu.return_choice()
        if ch == "1":
            server.start_server()
            server.run_loop()
        elif ch == "2":
            global_logging("v", "exit program bye!")
            break
        else:
            pass