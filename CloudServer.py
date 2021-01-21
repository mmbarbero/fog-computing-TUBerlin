import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
	try:
		message = socket.recv()
		print("Average is "+ message.decode())
		socket.send(b"Message Received")
	except:
		print("FAIl")
	time.sleep(1)

