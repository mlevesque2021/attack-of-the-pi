import math, random, sys
import pygame
from pygame.locals import *

pygame.init()
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
current_Frame = 0

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

#define some groups
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()

class spritesheet:
	def __init__(self, filename, cols, rows):
		self.sheet = pygame.image.load(filename).convert_alpha()
		
		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows
		
		self.rect = self.sheet.get_rect()
		self.w = self.cellWidth = self.rect.width / cols
		self.h = self.cellHeight = self.rect.height / rows
		self.hw, self.hh = self.cellCenter = (self.w / 2, self.h / 2)
		
		self.cells = list([(index % cols * self.w, index / cols * self.h, self.w, self.h) for index in range(self.totalCellCount)])
		self.handle = list([
			(0, 0), (-self.hw, 0), (-self.w, 0),
			(0, -self.hh), (-self.hw, -self.hh), (-self.w, -self.hh),
			(0, -self.h), (-self.hw, -self.h), (-self.w, -self.h),])
			
	def get_image (self, index):
		pygame.image.load()
		
	def draw(self, surface, cellIndex, x, y, handle = 0):
		self.current_image = surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])


class Player(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
		self.spritesheet = spritesheet("Sprites/player_Spritesheet.png",8,1)
		
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

class Enemy(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		enemys.add(self)
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
		self.spritesheet = spritesheet("Sprites/enemy3.png",8,1)
		self.image = pygame.image.load("Sprites/enemy collison.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.index = 7
		
	def idle (self):
		if ((current_Frame % 10) == 0 and self.index == 6):
			self.index = 7
		elif ((current_Frame % 10) == 0 and self.index == 7):
			self.index = 6
		
	def update(self):
		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		self.spritesheet.draw(DS, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		self.idle()
		

class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		bullets.add(self)
		self.x = player.x
		self.y = player.y + 10
		self.xVel = 0
		self.yVel = -5
		self.spritesheet = spritesheet("Sprites/bullet.png",1,1)
		self.image = pygame.image.load("Sprites/bullet.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.index = 1
		
	def update(self):
		self.spritesheet.draw(DS, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		#self.mask.set_at((self.x, self.y))
		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		if self.y < -20:
			bullets.remove(self)
class Enemy1(Enemy):
	def __init__(self, x, y):
		Enemy.__init__(self, x, y)
	
player = Player(HW,270)


CENTER_HANDLE = 4
def events():
	keys = pygame.key.get_pressed()
	#pygame.event.pump()



	if keys[K_RIGHT]:
		player.xVel = 1
		
	elif keys[K_LEFT]:
		player.xVel = -1

	else:
		player.xVel = 0
		player.yVel = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()	
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				Bullet()
			if event.key ==pygame.K_e:
				Enemy1(HW, 50)
		
# main loop
while True:
	events()

	player.update()
	bullets.update()
	enemys.update()
	
	current_Frame = current_Frame + 1
	if ((current_Frame % 60) == 0):
		current_Frame = 0
		
	pygame.sprite.groupcollide(enemys, bullets, True, pygame.sprite.collide_mask)
		
	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)
