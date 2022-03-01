import socket
import random

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    address = ('localhost', 1025)     # family is deduced to be 'AF_INET'
    s.bind(address)
    s.listen()
    conn, addr = s.accept()
    print('Got client')

    while True:
        print('Waiting')
        msg = conn.recv(4096)
        if len(msg)>0:
            print('Got message')
        # do something with msg
            msg = str(msg)[2:-1]
            print("Robot got " + msg)
        robpos = [random.random() for _ in range(7)]
        
        msg = f'{robpos[0]} {robpos[1]} {robpos[2]} {robpos[3]} {robpos[4]} {robpos[5]} {robpos[6]}'
        conn.send(bytes(msg, 'utf-8'))
        
    