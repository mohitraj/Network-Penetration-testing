import socket 
host = "0.0.0.0"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
while True :
	conn,addr=s.accept()
	print ("Connected", addr)
	conn.send("Thank for connecting".encode())
	conn.close()

