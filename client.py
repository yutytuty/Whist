import pygame

pygame.init()


screen = pygame.display.set_mode((1800, 900))

white = (255, 255, 255)
black = (0, 0, 0)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	screen.fill(white)
	pygame.display.update()
