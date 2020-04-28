import socket
import pickle
from _thread import *
from classes import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	server.bind(("0.0.0.0", 1234))
except socket.error as e:
	str(e)

server.listen(4)
print("waiting for connections")

table = Table()

connections = []
while len(connections) != 4:
	connection, address = server.accept()
	print("connections established with ", address[0])

	connections.append(connection)
	players.append(Player("Player " + str(connections.index(connection))))

deck = Deck()
data = [[], []]
HEADERSIZE = 10
deck.build()
deck.shuffle()

full_msg = b""
new_msg = True
msg_len = 0

while True:
	for player in players:
		player.draw(deck, 13)

	for i in range(13):
		for player in players:
			player.sort_hand()

			for j in range(len(connections)):
				data = [[], []]
				players[j].sort_hand()
				for card in players[j].hand:
					data[0].append(card.image)

				data_send = pickle.dumps(data[0])
				data_send = bytes(f"{len(data_send):<{HEADERSIZE}}", "utf-8") + data_send

				connections[j].send(data_send)

			print("waiting for ", player.name)
			card_index = connections[players.index(player)].recv(20)
			if new_msg:
				msg_len = int(card_index[:HEADERSIZE])
				new_msg = False

			full_msg += card_index

			if len(full_msg) - HEADERSIZE == msg_len:
				data = pickle.loads(full_msg[HEADERSIZE:])
				print(data)
				new_msg = True
				full_msg = b""

			player.play_card(table, data)
