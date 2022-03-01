from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')
conn.send('pincett')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()