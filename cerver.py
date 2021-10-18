import socket
import threading
from _thread import *
''' USAGE ERROR MESSAGE ''' 
c_get = '\tget <key> \\r\\n\n\n'
c_set = '\tset <key> <value-size-bytes> \\r\\n\n\t<value> \\r\\n\n'
usage = '\nCOMMANDS:\n' + c_get + c_set
''' END OF MESSAGE '''

#mutex so only one client accesses the file at the same time
mutex = threading.Lock() # makes only one client access the file at a time
def thread_work(conn):
    while True:
            data = conn.recv(256).decode() #get message from client
            while((args := argparsing(data,conn)) == '0'):
                conn.send(usage.encode()) #sending usage message 
                data = conn.recv(256).decode() #get message from client
            if(args == 'close'):
                conn.close()
                return
            #check data does not have spaces, newlines, or special characters
            if(args['command'] == 'set'):
                print('set: ', args)
                # store into file system
                try:
                    with mutex:
                        replaceline = 0
                        try:
                            with open('filesystem.txt', 'r') as File: #checks for existing key
                                file_data = File.readlines() # put all data in file_data
                                File.seek(0,0) # put pointer to start of file
                                for line_num,line in enumerate(File): # check each key,val
                                    key,value = line.split(' ')
                                    #print(f"existingkey: {key}\nnewkey: {args['key']}")
                                    if key == args['key']: # if same key
                                        replaceline = 1 # change this line
                                        break
                        except Exception as e: # file does not exist
                            #print(e)
                            replaceline = 0
                            pass
                        if(replaceline): # if line needs replaced
                            #print('line is being replaced')
                            file_data[line_num] = args['key'] + ' ' + args['value'] +'\n'
                            with open('filesystem.txt', 'w') as File:
                                File.writelines(file_data)
                                passed = 1
                        else: # if line needs appended (no occurance)
                            with open('filesystem.txt', 'a') as File:
                                to_write = str(args['key']) + ' ' + str(args['value']) + '\n'
                                File.write(to_write)
                                passed = 1
                except Exception as e:
                    #print(e)
                    passed = 0
                    pass
                if(passed): # if successfully written
                    conn.send('STORED\r\n'.encode())
                else:
                    conn.send('NOT-STORED\r\n'.encode())
            elif(args['command'] == 'get'):
                #print('get', args)
                try:
                    found = 0
                    with open('filesystem.txt', 'r') as File: #checks for existing key
                        for line_num,line in enumerate(File): # check each key,val
                            key,value = line.split(' ')
                            #print(f"existingkey: {key}\nnewkey: {args['key']}")
                            if key == args['key']: # if same key
                                data_block = line_num
                                s_bytes = len(value)
                                found = 1
                                break
                    if(found):
                        message = str(value) + ' ' + str(key) + ' ' + str(s_bytes)
                        conn.send(message.encode())
                        #conn.send(value.encode())
                        conn.send('END'.encode())
                    else:
                        conn.send('END'.encode())
                except Exception as e:
                    #print(e)
                    #print('get fail')
                    conn.send('END'.encode())
    conn.close()    


def tcp_server(host,port):
    try:
        port = int(port)  # initiate port no above 1024
        listening = 1 # server starts with ability to listen
        n_clients = 0
        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind host address and port together
        print("Hello, I am a server.");
        server_socket.listen(3) # 2 possible clients
        while True:
                conn, address = server_socket.accept()# accept new connection
                n_clients += 1 # one more client connected 
                print("connection from " + str(address[0]) )
                start_new_thread(thread_work, (conn,)) 
        conn.close()  # close the connection
        return
    except Exception as e:
        pass
        #print(e)
        #server_socket.shutdown(1)
def argparsing(argv,conn):
    #arg = argv # in the case of only sending one input
    parsed = {}
    try:
        arg, args = argv.split(' ',1)
        if(arg == 'get'):
            parsed['command'] = str(arg)
            parsed['key'] = str(args) 
            return parsed # should only contain ['command': 'get', 'key': <key>]
        if(arg == 'set'):
            parsed['command'] = str(arg)
            key, s_bytes = args.split(' ',1) # splitting <key> <value-size-bytes>
            parsed['key'] = str(key) # adding <key> to list
            parsed['bytes'] = str(s_bytes) # adding <value-size-bytes> to list
            value = conn.recv(int(s_bytes)).decode() # getting <value> from client
            parsed['value'] = str(value) # adding <value> to list
            return parsed # returning args in a list
    except Exception as e: # if the clients message is not in correct format return error
        if(argv == "terminate"):
            return 'close'
        #print(f'incorrect format\n{e}')
        pass
    return '0'
if __name__ == "__main__":
    tcp_server('',12345) # empty string for host listens to clients from all ips 
