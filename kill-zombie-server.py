import os
def kill_process():
    with open('proc.txt', 'r') as fp:
        for line in fp:
            wordnum = 0
            for word in line.split():
                if(wordnum == 1):
                    command = "kill " + word
                    try:
                        os.system(command) 
                    except:
                        pass
                wordnum += 1
    return
def write_proc_id():
    os.system('ps aux | grep "python3.8 server.py" >proc.txt')
    return
if __name__ == "__main__":
    write_proc_id() # make file containing all process ids containing "python3.8 server.py"
    kill_process() # kill all processes ( zombie servers )
