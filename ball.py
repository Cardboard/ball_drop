import pygame, math

class Ball():
	def __init__(self, (x,y), size, hand):
		self.x = x
		self.y = y
		self.size = size
		self.color = (0, 0, 255)
		self.thickness = 1

		self.xvel = 0
		self.xvel_max = 10
		self.yvel = 0
		self.yvel_max = 10

		self.hand = hand
		self.held = True

	def draw(self, DISPLAY):
		pygame.draw.circle(DISPLAY, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
		#pygame.draw.rect(DISPLAY, (128,128,255), (self.x-self.size, self.y-self.size, self.size*2, self.size*2))


	def gravity(self, g):
		self.yvel += g / 100
		self.yvel = self.math_clamp(-self.yvel_max, self.yvel, self.yvel_max)
		self.xvel = self.math_clamp(-self.xvel_max, self.xvel, self.xvel_max)
		self.y += self.yvel
		self.x += self.xvel

	def math_clamp(self, _min, value, _max):
		if value < _min:
			return _min
		elif value > _max:
			return _max
		else:
			return value

	def hold(self):
		if self.held == True:
			self.x = self.hand.rect.x + 60
			self.y = self.hand.rect.y + 30
			self.yvel = 0
			self.xvel = 0

	def collide(self, HOOP, RIMS):
		points = [] # holds points where balls's perimeter and rim collide
		collisionDegrees = [] # holds degrees where point collided for calculating mean collision point
		collide_rect = pygame.Rect(self.x-self.size, self.y-self.size, self.size*2, self.size*2)
		if HOOP.rect.colliderect(collide_rect):
			if collide_rect.x > HOOP.rect.x and (collide_rect.x + collide_rect.width) < (HOOP.rect.x + HOOP.rect.width) and collide_rect.top > HOOP.rect.top:
				print('SCORE!')
				self.x = -100
		# ball collides with rim
		for rim in RIMS:
			if rim.rect.colliderect(collide_rect):
				# check every point on ball's perimeter to see if it collides with rim
				for degree in range(270, 630):
					pointx = self.x + self.size * math.cos((degree * math.pi) / 180)
					pointy = self.y + self.size * math.sin((degree * math.pi) / 180)
					# point collides with rim
					if rim.rect.collidepoint((pointx, pointy)):
						# add point to list (only needed for drawing collidion points?)
						points.append((pointx, pointy))
						# add degree at which point collision occured to list
						collisionDegrees.append(degree)
				if len(collisionDegrees) != 0:
					medianDegree = sum(collisionDegrees) / len(collisionDegrees)
					print(medianDegree)
					self.yvel += - (self.size * math.sin((medianDegree * math.pi) / 180)) / 5
					self.xvel += - (self.size * math.cos((medianDegree * math.pi) / 180)) / 10

		return points