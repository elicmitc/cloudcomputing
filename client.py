import socket
import sys
c_get = '\tget <key> \\r\\n\n\n'
c_set = '\tset <key> <value-size-bytes> \\r\\n\n\t<value> \\r\\n\n\n'
terminate = '\tterminate\n'
usage = '\nCOMMANDS:\n' + c_get + c_set + terminate

def tcp_client(Host, Port):
    try:
        host = socket.gethostname()  # only on same system
        port = int(Port)  # socket server port number
        client_socket = socket.socket()  # instantiate
        client_socket.connect((Host, port))  # connect to the server
        print("Hello, I am a client");

        while True:
            message = str(input('send: '))  # take input
            command = ''
            try:
                command, more = message.split(' ',1)
                #print(f'command: {command}')
            except Exception as e:
                if(message == 'terminate'):
                    client_socket.send(message.encode())
                    client_socket.close()
                    print("terminating connection")
                    return
                print(e)
                pass
            if(command == 'set'):
                try:
                    key, s_bytes = more.split(' ')
                    if(s_bytes.isnumeric() == False):
                        raise Exception("bytes invalid form. Integer required")
                    client_socket.send(message[0:256].encode())  # send: set <key> <size>
                    message = str(input("value: "))
                    client_socket.send(message[0:int(s_bytes)].encode())  # send <value>
                    state = client_socket.recv(256).decode()
                    print(state,end='')
                    continue
                except:
                    pass
            elif(command == 'get'):
                try:
                    msg_num = 0
                    size = 256
                    client_socket.send(message[0:256].encode())  # send message
                    while True:
                        info = client_socket.recv(size).decode()  # receive response
                        if(info == 'END'):
                            break
                        if(msg_num == 0):
                            print(info)
                            msg_num +=1
                            temp1,temp2,n_size = info.split(' ',2)
                            size = int(n_size)
                            continue
                        if(msg_num == 1):
                            print(info,end='')
                    continue
                except Exception as e:
                    print(e)
                    pass
            print(usage)
        client_socket.close()  # close the connection
    except Exception as e:
        print(e)
        client_socket.send('END'.encode())
        client_socket.close()  # close the connection
if __name__ == "__main__":
    serverip = str(sys.argv[1])#socket.gethostbyname(socket.gethostname())
    tcp_client(serverip,12345) # need to put the output of gethostname from server into the host argument
