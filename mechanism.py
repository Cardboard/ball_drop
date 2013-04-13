import pygame

class Mechanism:
	def __init__(self, rect_stationary, rect_move, max_left=-1, max_right=-1, max_top=-1, max_bottom=-1):
		self.rect_stat = pygame.Rect(rect_stationary)
		self.rect_move = pygame.Rect(rect_move)
		self.rect_conn = pygame.Rect(0,0, 45,45)
		self.max_left = max_left
		self.max_right = max_right
		self.max_top = max_top
		self.max_bottom = max_bottom

		self.attachments = None

	def draw(self, DISPLAY):
		pygame.draw.rect(DISPLAY, (200,200,200), self.rect_stat)
		pygame.draw.rect(DISPLAY, (200,200,200), self.rect_move)
		self.rect_conn = self.calculateConnector()
		self.rect_conn = self.rect_conn.inflate(15,15)
		pygame.draw.rect(DISPLAY, (128,128,128), self.rect_conn)
		# draw all attachments
		if self.attachments != None:
			for attachment in self.attachments:
				if attachment.shape != None: # attachment uses shapes rather than images
					
					if attachment.shape == 'rect':
						pygame.draw.rect(DISPLAY, attachment.color, attachment.rect)
					elif attachment.shape == 'polygon':
						pygame.draw.polygon(DISPLAY, attachment.color, attachment.rect)
					elif attachment.shape == 'ellipse':
						pygame.draw.ellipse(DISPLAY, attachment.color, attachment.rect)
					else:
						print('undefined shape? -->{0}'.format(attachment.shape))

				else:
					DISPLAY.blit(attachment.images[attachment.currentImage], attachment.rect)

				# draw all attachments to attachments
				if attachment.link != None:
					if attachment.link.shape != None: # attachment uses shapes rather than images
					
						if attachment.link.shape == 'rect':
							pygame.draw.rect(DISPLAY, attachment.link.color, attachment.link.rect)
						elif attachment.link.shape == 'polygon':
							pygame.draw.polygon(DISPLAY, attachment.link.color, attachment.link.rect)
						elif attachment.link.shape == 'ellipse':
							pygame.draw.ellipse(DISPLAY, attachment.link.color, attachment.link.rect)
						else:
							print('undefined shape? -->{0}'.format(attachment.link.shape))

					else:
						DISPLAY.blit(attachment.images[attachment.currentImage], attachment.rect)

	def move(self, dir_LR=0, dir_UD=0, speed=3):
		self.rect_move = self.rect_move.move(dir_LR * speed, dir_UD * speed)
		if self.rect_move.right > self.max_right and self.max_right != -1:
			self.rect_move.right = self.max_right
		elif self.rect_move.left < self.max_left and self.max_left != -1:
			self.rect_move.left = self.max_left
		elif self.rect_move.top < self.max_top and self.max_top != -1:
			self.rect_move.top = self.max_top
		elif self.rect_move.bottom > self.max_bottom and self.max_bottom != -1:
			self.rect_move.bottom = self.max_bottom

	def moveAttachments(self):
	# move attachments
		if self.attachments != None:
			for attachment in self.attachments:
				if attachment.location == 'topright':
					attachment.rect.topleft = self.rect_move.topright
				elif attachment.location == 'topleft':
					attachment.rect.topright = self.rect_move.topleft
				attachment.rect.x = attachment.rect.x + attachment.offsetx
				attachment.rect.y = attachment.rect.y + attachment.offsety

				if attachment.link != None:
					if attachment.link.location == 'topright':
						attachment.link.rect.topleft = attachment.rect.topright
					elif attachment.link.location == 'topleft':
						attachment.link.rect.topright = attachment.rect.topleft
					attachment.link.rect.x = attachment.link.rect.x + attachment.link.offsetx
					attachment.link.rect.y = attachment.link.rect.y + attachment.link.offsety

	def calculateConnector(self):
		return self.rect_stat.clip(self.rect_move)

	def attach(self, attachments):
		self.attachments = attachments


class Attachment:
	def __init__(self, images, location, shape=None, color=(128,128,128), offsetx=0, offsety=0):
		self.location = location
		self.currentImage = 0
		self.images = []
		self.link = None
		self.offsetx = offsetx
		self.offsety = offsety
		# if not using images (using shapes)
		if shape != None:
			self.rect = pygame.Rect(images)
			assert shape != None, "shape not specified"
			self.shape = shape
			self.color = color
		# if using images
		else:
			for image in images:
				newimage = pygame.image.load(image).convert_alpha()
				self.images.append(newimage)
			self.rect = self.images[0].get_rect()
			self.shape = None

	def attach(self, linkto):
		self.link = linkto

	def moveAttachments(self):
	# move attachments
		if self.link != None:
			if link.location == 'topright':
				link.rect.topleft = self.rect_move.topright
			elif link.location == 'topleft':
				link.rect.topright = self.rect_move.topleft


class Hand(Attachment):
	pass