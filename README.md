# BearFTP
 
### Installation
You can install the required modules by running:

```sh
$ python3 pip install -r requirements.txt
```
### Usage
To start the server:
```sh
$ python3 BearFTP.py -s <server_ip> -p <server_port>
```
- ```<server_ip>``` is the IP address that the server will listen to.
- ```<server_port>``` is the port number that the server will listen on. The default port number is 4455.

## Node
To use the client Node, you need to create an instance of the Node call the desired method.

## Using Arguments 
```sh
$ python# client_node.py [-h] [-s SERVER] [-p PORT] {add,list,fetch} file
```
### Usage
The script can be used to perform the following actions:

- add: Add a file to the server. Usage: python file_server.py -s SERVER -p PORT add file_path
- list: List all files available on the server. Usage: python file_server.py -s SERVER -p PORT list
- fetch: Fetch a file from the server. Usage: python file_server.py -s SERVER -p PORT fetch file_name

### Arguments:
```sh
-s, --server: The address of the P2P server. Required for all actions.
-p, --port: The port to listen on. Default is 4455.
action: The action to perform. Must be one of "add", "list", or "fetch".
file: The name of the file to add/fetch.
```
Example
To add a file named "example.txt" to the server at address "localhost" on port "1234", use the following command:

### List files
To list files in the server:
```py
from Node import Node

client = Node(server="127.0.0.1", port=4455)
client.list_files("path/to/folder")
```
- Note that the path to the folder must be relative to the server's directory. 

### Add a file
To add a file to the server:

```py
from Node import Node

client = Node(server="127.0.0.1", port=4455)
client.add_file("path/to/file")

```


### Fetch a file
To fetch a file from the server:
```py
from Node import Node
client = Node(server="127.0.0.1", port=4455)
client.fetch_file("path/to/file")

```
