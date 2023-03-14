import socket
import argparse
import os

class Node:
    
    FORMAT = "utf-8"
    SIZE = 1024
    
    def __init__(self, server, port=4455):
        self.IP = server
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
    
    def add_file(self, file_name):
        if os.path.exists(file_name):
            file = open(file_name, "r")
            data = file.read()
            self.client.send(f"add {file_name}".encode(self.FORMAT))
            msg = self.client.recv(self.SIZE).decode(self.FORMAT)
            print(f"[SERVER]: {msg}")
            self.client.send(data.encode(self.FORMAT))
            msg = self.client.recv(self.SIZE).decode(self.FORMAT)
            print(f"[SERVER]: {msg}")
            file.close()
            self.client.close()
        else:
            print("File not found")
    
    def list_files(self, file_name):
        self.client.send(f"list {file_name} ".encode(self.FORMAT))
        msg = self.client.recv(self.SIZE).decode(self.FORMAT)
        print(f"[SERVER]: {msg}")
        self.client.close()
    
    def fetch_file(self, file_name):
        self.client.send(f"fetch {file_name}".encode(self.FORMAT))
        msg = self.client.recv(self.SIZE).decode(self.FORMAT)
        if msg != 'File not found':
            directory, filename = os.path.split(msg)
            os.makedirs(directory, exist_ok=True)
            self.client.send("Filename received.".encode(self.FORMAT))
            data = self.client.recv(self.SIZE)
            print(f"[RECV] Receiving the file data.")
            with open(os.path.join(directory, filename), "w") as f:
                f.write(data.decode(self.FORMAT))
            self.client.send("File data received".encode(self.FORMAT))
        else:
            print(f"File not found - [{file_name}]")
    
    def close(self):
        self.client.close()

 