import math, random, sys
import pygame
from pygame.locals import *

# exit the program
def events():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_LEFT:
				player.xVel = -1
			if event.key==pygame.K_RIGHT:
				player.xVel = 1
			if event.key==pygame.K_SPACE:
				Bullet()
		else:
			player.xVel = 0
			player.yVel = 0

# define display surface			
W, H = 600, 280
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Sprite Sheets")
FPS = 60

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

class spritesheet:
	def __init__(self, filename, cols, rows):
		self.sheet = pygame.image.load(filename).convert_alpha()
		
		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows
		
		self.rect = self.sheet.get_rect()
		w = self.cellWidth = self.rect.width / cols
		h = self.cellHeight = self.rect.height / rows
		hw, hh = self.cellCenter = (w / 2, h / 2)
		
		self.cells = list([(index % cols * w, index / cols * h, w, h) for index in range(self.totalCellCount)])
		self.handle = list([
			(0, 0), (-hw, 0), (-w, 0),
			(0, -hh), (-hw, -hh), (-w, -hh),
			(0, -h), (-hw, -h), (-w, -h),])
		
	def draw(self, surface, cellIndex, x, y, handle = 0):
		surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])


class Player(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
		self.spritesheet = spritesheet("player_Spritesheet.png",8,1)
		self.index = 7
		
	def update(self):
		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		self.spritesheet.draw(DS, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		
	@property
	def xVel(self):
		return self._xVel
	
	@xVel.setter
	def xVel(self, value):
		self._xVel = value
		
	@property
	def yVel(self):
		return self._yVel
	
	@yVel.setter
	def yVel(self, value):
		self._yVel = value
		

class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		bullets.append(self)
		self.x = player.x
		self.y = player.y + 10
		self.xVel = 0
		self.yVel = -1
		self.spritesheet = spritesheet("bullet.png",1,1)
		self.index = 7
		
	def update(self):
		self.spritesheet.draw(DS, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)

		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		if self.y < -10:
			bullets.remove(self)

		
player = Player(HW,270)
bullets = []
enemys = []

CENTER_HANDLE = 4

# main loop
while True:
	events()

	player.update()
	
	for i in bullets:
		i.update()
		print len(bullets)
	

	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)
