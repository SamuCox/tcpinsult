import time
import socket

sock = socket.create_connection(('127.0.0.1', 8888))
sock.sendall(b'Test\r\n')

while True:
	read = 0
	start = time.time()
	while True:
		chunk = sock.recv(102400)
		read += len(chunk)
		if read > 1e6:
			break

	duration = time.time() - start
	rate = read / duration / 1000
	print(f'Rate: {rate:.1f}KBps')
