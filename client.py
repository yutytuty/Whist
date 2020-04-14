from math import floor
from classes import *
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((socket.gethostname(), 1234))

pygame.init()

screen_width = 1760
screen_height = 990

screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)

deck = Deck()
deck.shuffle()

table = Table()

players.append(Player("Player 1"))

players[0].draw(deck, 13)
players[0].sort_hand()


positions = []
[positions.append((i * 131, screen_height - 200)) for i in range(len(players[0].hand))]

turn = 0


def game():
	global turn

	def click_card():
		global turn
		# TODO: change turn condition to work for client username
		if event.type == pygame.MOUSEBUTTONDOWN and players[turn % 4].name == "Player 1":
			mouse_pos = pygame.mouse.get_pos()
			mouse_press = pygame.mouse.get_pressed()
			if mouse_press == (1, 0, 0) and mouse_pos[0] < positions[-1][0] and mouse_pos[1] > 790:
				index_hand = floor(mouse_pos[0] / 131)
				turn += players[0].play_card(table, index_hand)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			click_card()

		screen.fill(white)

		for i in range(len(players[0].hand)):
			screen.blit(players[0].hand[i].image, (i * 131, screen_height - 200))

		pygame.display.update()


if __name__ == "__main__":
	game()
