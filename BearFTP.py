import argparse
import os
import threading
from datetime import datetime
import socket
import logging
from colorama import Fore, Style

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s %(message)s')

    def log(self, message,color='green'):
        if(color=='green'):
            print(f"{Fore.GREEN}[INFO] {message}{Style.RESET_ALL}")
        elif(color=='red'):
            print(f"{Fore.RED}[INFO] {message}{Style.RESET_ALL}")
        elif(color=='yellow'):
            print(f"{Fore.YELLOW}[INFO] {message}{Style.RESET_ALL}")
        elif(color=='blue'):
            print(f"{Fore.BLUE}[INFO] {message}{Style.RESET_ALL}")

        logging.info(message)

class BearFTP:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.size = 1020
        self.format = "utf-8"
        self.logger = Logger('server.log')

    def handle_client(self, conn, addr):
        now = datetime.now().strftime('%I:%M:%S%p')

        self.logger.log(f"[NEW CONNECTION] {addr} connected. at {now}",'green')
        filename = conn.recv(self.size).decode(self.format)
        if(filename.split()[0]=='add'):
            file = open(f'./store/{filename.split()[1]}', "w")
            conn.send("Filename received.".encode(self.format),'blue')
            data = conn.recv(self.size)
            self.logger.log(f"[RECV] Receiving the file data from {addr}.",'blue')
            file.write(data.decode(self.format))
            conn.send("File data received".encode(self.format))
            file.close()
        elif(filename.split()[0]=='list'):
            pathname  = f'./store{filename.split()[1]}'
            if(os.path.exists(pathname)):
                files = os.listdir(pathname)
                for i in range(len(files)):
                    path = os.path.join(pathname, files[i])
                    if os.path.isdir(path):
                        files[i] = '/' + files[i]
                files = " ".join(files)
                conn.send(files.encode(self.format))
            else:
                conn.send("Directory not found".encode(self.format))
        elif(filename.split()[0]=='fetch'):
            fileax = filename.split()[1].strip('/')
            
            pathname  = f'./store/{fileax}'
            if(os.path.isfile(pathname)):
                file = open(pathname,'r')
                data = file.read()
                conn.send(f"{pathname.replace('./store','.')}".encode(self.format))
                msg = conn.recv(self.size).decode(self.format)
                self.logger.log(f"[SERVER]: {msg}",'blue')
                conn.send(data.encode(self.format))
                msg = conn.recv(self.size).decode(self.format)
                self.logger.log(f"[SERVER]: {msg}",'blue')
                file.close()
            else:
                conn.send("File not found".encode(self.format))
        conn.close()
        now = datetime.now().strftime('%I:%M:%S%p')
        self.logger.log(f"[DISCONNECTED] {addr} disconnected. at {now}",'red')

    def start(self):
        self.logger.log("[STARTING] Server is starting.")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.addr)
        server.listen()
        self.logger.log("[LISTENING] Server is listening.",'yellow')
     
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File server")
    parser.add_argument("-s", dest='server', type=str, help="P2P Server ")
    parser.add_argument("-p",  dest="port", default=4455, type=int, help="Port to listen on default = 4455")

    args = parser.parse_args()
    
    IP = args.server
    PORT = args.port
 
  
    server = BearFTP(IP, PORT)
    server.start()
