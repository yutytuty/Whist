import socket
import pickle
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server.bind((socket.gethostname(), 1234))
except socket.error as e:
	str(e)

server.listen(4)
print("waiting for connections")


class DataPackage:
	def __init__(self, player, table):
		self.hand = player.hand
		self.on_table = table.on_table
		self.turn = 0


def threaded_client(connection: socket.socket):
	connection.send(str.encode("Connection established"))
	while True:
		pass
