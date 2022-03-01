from queue import Queue
from threading import Thread
from multiprocessing.connection import Listener
import socket 


# A thread that produces data
def voice_listenener(q):
    address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'secret password')

    while True:
        conn = listener.accept()
        msg = conn.recv()
        # do something with msg
        print(msg)
        conn.close()
        if msg == 'pincett':
            q.put(1)
            print("Put 1")
        
        if msg == 'nålförare':
            q.put(2)
            print("Put 2")
        
        if msg == 'diatermi':
            q.put(3)
            print("Put 3")
    
          
# A thread that consumes data
def send2robot(q):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = socket.socket()          
  
        # Define the port on which you want to connect 
        
        
        # connect to the server on local computer 
        #s.connect(('127.0.0.1', port))
        print("hi")
        address = ('192.168.125.1', 1025)
        #address = ('localhost', 1025)
        try:
            s.connect(address) 
        except:
            while True:
                if (s.connect(address) != True ):
                    break
                print("trying to connect")
        while True:
            cmd = q.get()
            print("Sending " + str(cmd))
            s.send(bytes(str(cmd), 'utf-8'))
            data = s.recv(4096)
            if len(data)>0:
                res=str(data)
                print(res[2:len(res)-1])
        



    
            
          
# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target = voice_listenener, args =(q, ))
t2 = Thread(target = send2robot, args =(q, ))
t1.start()
t2.start()