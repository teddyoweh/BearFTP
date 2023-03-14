from Node import Node

server = Node("0.0.0.0", 4455)
server.list_files("/")
server.add_file("example.txt")
server.fetch_file("example.txt")
server.close()