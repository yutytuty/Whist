import socket
import pickle
from _thread import *
from time import sleep
from classes import *

x = 100
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	server.bind(("0.0.0.0", 1234))
except socket.error as e:
	str(e)

server.listen(4)
print("waiting for connections")

table = Table()


def input_thread(conn):
	while True:

		card_index = conn.recv(10)
		if card_index:
			card_index = pickle.loads(card_index)
			print(card_index)


def threaded_client(conn: socket.socket, player_id):

	players.append(Player("Player " + str(player_id)))
	start_new_thread(input_thread, (conn, ))
	players[player_id].draw(deck, 13)
	players[player_id].sort_hand()
	HEADERSIZE = 10

	data = [[], []]
	for card in players[player_id].hand:
		data[0].append(card)
	print(data[0])
	z = data[0]
	print(data)
	data_send = pickle.dumps(z)
	print(len(data_send))
	data_send = bytes(f"{len(data_send):<{HEADERSIZE}}", 'utf-8')+data_send
	print(data_send)
	conn.send(data_send)


client_num = 0
connections = []
while len(players) != 4:
	connection, address = server.accept()
	print("Connection established with: ", address)
	client_num += 1

	connections.append(connection)
	players.append(Player("player " + str(client_num)))

deck = Deck()
data = [[], []]
HEADERSIZE = 10
deck.build()
deck.shuffle()

while True:

	for player in players:
		player.draw(deck, 13)

	for i in range(13):
		global data_send
		for player in players:
			player.sort_hand()

			# data_send = pickle.dumps(data[0])
			# data_send = bytes(f"{len(data_send):<{HEADERSIZE}}", 'utf-8') + data_send

			for j in range(len(connections)):
				data = [[], []]
				players[j].sort_hand()
				for card in players[j].hand:
					data[0].append(card.image)

				data_send = pickle.dumps(data[0])
				data_send = bytes(f"{len(data_send):<{HEADERSIZE}}", "utf-8") + data_send

				connections[j].send(data_send)
			card_index = connections[players.index(player)].recv(10)
			card_index = pickle.loads(card_index)
			print(card_index)

			player.play_card(table, card_index)
