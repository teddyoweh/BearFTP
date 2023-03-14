from Node import Node
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File server")
    parser.add_argument("-s", dest='server', type=str, help="P2P Server ")
    parser.add_argument("-p",  dest="port", default=4455, type=int, help="Port to listen on default = 4455")
    parser.add_argument("action", help="Action to perform", choices=["add", "list", "fetch"])
    parser.add_argument("file", help="Name of the file to add/fetch")
    args = parser.parse_args()
    
    server = Node(args.server, args.port)
    
    if args.action == "add":
        server.add_file(args.file)
    elif args.action == "list":
        server.list_files(args.file)
    elif args.action == "fetch":
        server.fetch_file(args.file)
    
    server.close()

