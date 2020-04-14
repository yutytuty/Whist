import socket


class Network:

	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = ""
		self.port = 1234
		self.address = (self.server, self.port)

	def connect(self):
		try:
			self.client.connect(self.address)
			return self.client.recv(2048).decode()
		except:
			pass
