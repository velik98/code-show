Python client-server scripts for sending files.

The first python script acts as a server and the second python script acts as a client.
The input file contains a list of files which the client sends to the server after it is launched.

Server:
- configurable (ip address, port, work directory, ...)
- after start-up it waits for a client connection
- after client connection is accepted, it receives a file (or multiple files) from the client and saves it into the work directory
- if the received file in the work directory already exists, it is not overwritten but rather renamed (e.g. file.txt to file(1).txt)

Client:
- input arguments: address/port of the server, input file with a list of files to be sent
- during the file transmission, it continuously writes the approximate completion status of the single file transmission (as percentage) to the standard output
