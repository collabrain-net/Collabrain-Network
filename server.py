
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
# the socket is of the type Internet socket and is  using TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
# wait client to connect
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)



# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            protocol = client.recv(1)

            if protocol == b'M':
                message = client.recv(1024)
                broadcast(message)
            elif protocol == b'F':
                fileData = b''
                totalChunks = int(client.recv(9).decode('ascii'))
                print("Total Chunks:", totalChunks)
                for i in range(totalChunks):
                    chunkSize = int(client.recv(12).decode('ascii'))
                    # print("Receiving Chunk", i, "Chunk Size:", chunkSize)
                    chunk = client.recv(chunkSize)
                    print("Receiving Chunk", i, "Chunk Size:", chunkSize)
                    # print("receiving <- ", i)
                    fileData += chunk

                #save file in server
                with open("./new_file.jpg", 'wb') as file:
                    file.write(fileData)
                    print("File saved")

            else:
                print("Errror header: ",protocol)
            # message = client.recv(1024)
            # broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    print("""
            █▀▀ █▀▀█ █░░ █░░ █▀▀█ █▀▀▄ █▀▀█ █▀▀█ ░▀░ █▀▀▄ 
            █░░ █░░█ █░░ █░░ █▄▄█ █▀▀▄ █▄▄▀ █▄▄█ ▀█▀ █░░█ 
            ▀▀▀ ▀▀▀▀ ▀▀▀ ▀▀▀ ▀░░▀ ▀▀▀░ ▀░▀▀ ▀░░▀ ▀▀▀ ▀░░▀ """)
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('OK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


#start server
receive()




