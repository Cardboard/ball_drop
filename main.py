# DO NEXT:
'''
- add simple ball physics!
- add score system
- add AI for basket
'''

import pygame, sys

# seperate .py game-related files
from game import *
from mechanism import *
from ball import *
###############################################################################
game = Game()

mech_player = Mechanism((40,70,25,530), (-400,110,700,25), -600, 710, 110, 135)
a_hand = Hand(['hand_idle.png'], 'topright')
mech_player.attach([a_hand])

# set up hoop and rim
mech_hoop = Mechanism((700, 0, 25, 550), (500, 490, 700, 25), 220, 1280, 250, 520)
# Attachment( images, location, shape=None, color=(128,128,128), offsetx=0, offsety=0)
a_rim_L = Attachment((0,0,25,25), 'topleft', 'rect', (128,128,128), -125)
a_hoop = Attachment((0,0,100,25), 'topleft', 'rect', (255,255,255), -25)
a_rim_R = Attachment((0,0,25,25), 'topleft', 'rect', (128,128,128))
a_backboard = Attachment((0,0,25,200), 'topleft', 'rect', (128,128,128), offsetx=150, offsety=-250)
rims = [a_rim_L, a_rim_R, a_backboard]
mech_hoop.attach([a_hoop, a_rim_L, a_rim_R, a_backboard])


ball = Ball((600,20), 15, a_hand) # ( (xpos, ypos), radius, hand to hold ball)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		# DEBUGGING
		if event.type == pygame.MOUSEBUTTONUP:
			print(pygame.mouse.get_pos())

	key = pygame.key.get_pressed()
	# PLAYER MOVEMENT
	if key[pygame.K_RIGHT]:
		mech_player.move(1)
	elif key[pygame.K_LEFT]:
		mech_player.move(-1)
	if key[pygame.K_DOWN]:
		mech_hoop.move(0,1)
	elif key[pygame.K_UP]:
		mech_hoop.move(0,-1)
	# BALL CONTROL
	if key[pygame.K_SPACE]:
		if ball.held == True:
			if key[pygame.K_RIGHT]:
				ball.xvel = 1
			elif key[pygame.K_LEFT]:
				ball.xvel = -1
			ball.held = False # drop ball if held and space pressed

	mech_player.moveAttachments()
	mech_hoop.moveAttachments()

	ball.gravity(game.gravity)
	ball.hold()
	points = ball.collide(a_hoop, rims)
	# delete ball if off screen, create new ball
	if ball.y > game.height:
		ball = None
		ball = Ball((a_hand.rect.x+60, -50), 15, a_hand)

	# DRAWING THINGS
	game.draw([mech_player, mech_hoop, ball])
	pygame.draw.rect(pygame.display.get_surface(), (0,255,128), a_hoop.rect)
	if points != []:
		for point in points:
			pygame.draw.rect(pygame.display.get_surface(), (0,128,255), (point[0], point[1], 5, 5))
	pygame.display.update()
	game.clock.tick(game.FPS)