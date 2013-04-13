import pygame

class Game:
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.gravity = 9.8
		self.width = 800
		self.height = 600
		self.display = pygame.display.set_mode((self.width, self.height))
		self.display.fill((255,255,255))

	def draw(self, DRAWLIST):
		self.display.fill((255,255,255))
		for func in DRAWLIST:
			func.draw(self.display)
		#pygame.display.update()