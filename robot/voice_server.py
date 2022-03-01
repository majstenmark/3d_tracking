from multiprocessing.connection import Listener

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')

while True:
    conn = listener.accept()
    msg = conn.recv()
    # do something with msg
    print(msg)
    conn.close()
    
    
listener.close()