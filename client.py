import socket
import threading
import os

# Connection Data
host = '127.0.0.1'
port = 55555

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'OK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        user_input = input('')
        #send a file
        if user_input.lower() == "/file":
            file_path = input("Enter the path of the file you want to send: ")
            # file_path = "./data/logo.jpg"

            print("Opening file:", file_path)

            fileSize = os.stat(file_path).st_size
            chunkSize = 1024
            chunksNum = fileSize // chunkSize
            remainder =  1 if fileSize > chunkSize else 0
            try:
                protocol = b"F"
                # 100GB capacity
                totalChunks = "{:09d}".format(chunksNum + remainder).encode('ascii')

                client.send(protocol + totalChunks)

                with open(file_path, 'rb') as file:
                    print("File opened successfully.")
                    for i in range(chunksNum):
                        client.send( "{:012d}".format(chunkSize).encode('ascii'))
                        chunk = file.read(chunkSize)
                        client.send(chunk)
                        print("sending -> ", i)

                    if remainder > 0:
                        client.send("{:012d}".format(remainder).encode('ascii'))
                        chunk = file.read(remainder)
                        client.send(chunk)
                        print("sending remainder -> ")


            except FileNotFoundError:
                print("File not found.")
            except Exception as e:
                print("An error occurred while opening the file:", e)

        #send a message
        else:
            #send M protocol
            protocol = "M"
            client.send(protocol.encode('ascii'))
            #send the 1024 bytes message
            message = '{}: {}'.format(nickname, user_input)
            client.send(message.encode('ascii'))




# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


