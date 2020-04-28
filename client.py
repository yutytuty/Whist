import pygame
import socket
import pickle
from _thread import *
from math import floor
from sys import exit

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("192.168.0.18", 1234))

pygame.init()

screen_width = 1760
screen_height = 990

screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
HEADERSIZE = 10


def game():
	global data
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("hello")
				pygame.quit()
				exit()

		screen.fill(white)

		if data:
			for card in data:
				# TODO: when sending table switch to data[0][i]
				image = pygame.image.load(card)
				image = pygame.transform.scale(image, (131, 200))
				screen.blit(image, (data.index(card) * 131, screen_height - 200))

		pygame.display.update()


data = None
full_msg = b""
new_msg = True
msg_len = 0

start_new_thread(game, ())

while True:
	msg = server.recv(2046)
	if new_msg:
		if msg:
			msg_len = int(msg[:HEADERSIZE])
			new_msg = False

	full_msg += msg

	if len(full_msg) - HEADERSIZE == msg_len:
		data = pickle.loads(full_msg[HEADERSIZE:])
		new_msg = True
		full_msg = b""

		print(data)
		mouse_pressed = False

		while not mouse_pressed:
			click = pygame.event.wait()
			mouse_pos = pygame.mouse.get_pos()
			mouse_press = pygame.mouse.get_pressed()
			if mouse_press == (1, 0, 0):
				print(mouse_pos)
				if mouse_pos[0] < len(data) * 131 and mouse_pos[1] > screen_height - 200:
					data_send = pickle.dumps(floor(mouse_pos[0] / 131))
					data_send = bytes(f"{len(data_send):<{HEADERSIZE}}", "utf-8") + data_send
					server.send(data_send)
					mouse_pressed = True
