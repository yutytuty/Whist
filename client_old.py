import socket
import pickle
from _thread import *
import pygame
from sys import exit
from math import floor

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("192.168.0.18", 1234))

pygame.init()

screen_width = 1760
screen_height = 990

screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
HEADERSIZE = 10

data = None


def threaded_game():
	global data
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		screen.fill(white)
		if data:
			for i in range(len(data)):
				image = pygame.image.load(data[i])
				image = pygame.transform.scale(image, (131, 200))
				screen.blit(image, (i * 131, screen_height - 200))

		pygame.display.update()


full_msg = b''
new_msg = True
msglen = 0

start_new_thread(threaded_game, ())

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
			print("full msg received")
			data = pickle.loads(full_msg[HEADERSIZE:])
			new_msg = True
			full_msg = b""
			card_pressed = False
			while not card_pressed:
				mouse_pos = pygame.mouse.get_pos()
				mouse_press = pygame.mouse.get_pressed()
				if mouse_press == (1, 0, 0):
					print(mouse_pos[0], len(data) * 131, len(data[0]) * 131, mouse_pos[1], screen_height - 200)
					if mouse_pos[0] < len(data) * 131 and mouse_pos[1] > screen_height - 200:
						server.send(pickle.dumps(floor(mouse_pos[0] / 131)))
