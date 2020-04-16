from math import floor
import socket
import pickle
from _thread import *
import pygame

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 1234))

pygame.init()

screen_width = 1760
screen_height = 990

# screen: pygame.Surface
# screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
HEADERSIZE = 10


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = None
        self.assign_picture()

    def assign_picture(self):
        if self.value < 11:
            self.image = f"assets/{self.value}{self.suit[0]}.png"

        if self.value == 11:
            self.image = f"assets/J{self.suit[0]}.png"

        elif self.value == 12:
            self.image = f"assets/Q{self.suit[0]}.png"

        elif self.value == 13:
            self.image = f"assets/K{self.suit[0]}.png"

        elif self.value == 14:
            self.image = f"assets/A{self.suit[0]}.png"

    def __str__(self):
        if self.value < 11:
            return f"{self.value} of {self.suit}"
        elif self.value == 11:
            return f"Jack of {self.suit}"
        elif self.value == 12:
            return f"Queen of {self.suit}"
        elif self.value == 13:
            return f"King of {self.suit}"
        elif self.value == 14:
            return f"Ace of {self.suit}"


def threaded_game():
	turn = 0
	clock = pygame.time.Clock()
	new_msg = True
	full_msg = b''
	msglen = None

	while True:
		full_msg = b''
		new_msg = True
		while True:
			msg = server.recv(2046)
			if msg:
				if new_msg:
					print("new msg len:", msg[:HEADERSIZE])
					msglen = int(msg[:HEADERSIZE])
					new_msg = False

				print(f"full message length: {msglen}")

				full_msg += msg

				print(len(full_msg))

				if len(full_msg) - HEADERSIZE == msglen:
					print("full msg recvd")
					print(full_msg[HEADERSIZE:])
					print(pickle.loads(full_msg[HEADERSIZE:]))
					new_msg = True
					full_msg = b""

		for i in range(len(data[0])):
			image = pygame.image.load(data.hand[i].image)
			image = pygame.transform.scale(image, (131, 200))
			screen.blit(image, (i * 131, screen_height - 200))

		# click_card(data, data.name)

		pygame.display.update()


def game():

	start_new_thread(threaded_game, ())

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

				quit()


if __name__ == "__main__":
	game()
