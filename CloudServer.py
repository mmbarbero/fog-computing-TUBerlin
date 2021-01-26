import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def setStoplightPriority(avg):
	lane1 = float(avg.split(",")[0])
	lane2 = float(avg.split(",")[1])
	reply = ""
	if (lane1 > lane2):
		reply = "Prioritize lane 1"
	elif (lane1 < lane2):
		reply = "Prioritize lane 2"
	else:
		reply = "Equal priority"

	return reply

while True:
	try:
		message = socket.recv().decode()
		priority = setStoplightPriority(message)
		print("Priority is: " + priority)
		socket.send(priority.encode())
	except:
		print("FAIL")
	time.sleep(1)

