import random
import pygame
from pygame.locals import *
from random import randint

CENTER_HANDLE = 4
pygame.init()
FPS = 60
#define some groups
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
players = pygame.sprite.Group()
xPos = [x * 48 for x in range(2,20)]
yPos = [y * 20 for y in range (1,5)]
level = 0



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

	def __init__(self, x, y, screen):
		pygame.sprite.Sprite.__init__(self)
		players.add(self)
		self.screen = screen
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
		self.spritesheet = spritesheet("Sprites/player_Spritesheet.png",8,1)
		self.image = pygame.image.load("Sprites/player collison.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		
		self.index = 7
		
	def update(self):
		if (((self.x + self.xVel) > 90) and ((self.x + self.xVel) < 700)):
			self.x = self.x + self.xVel
			self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		self.spritesheet.draw(self.screen, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		
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

	
	def __init__(self, x, y, screen):
		pygame.sprite.Sprite.__init__(self)
		enemys.add(self)
		self.screen = screen
		self.current_Frame = 0
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
		self.spritesheet = spritesheet("Sprites/enemy3.png",8,1)
		self.image = pygame.image.load("Sprites/enemy collison.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.index = 7
		
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
	
		
	def idle (self):
		if ((self.current_Frame % 10) == 0 and self.index == 6):
			self.index = 7
			self.shoot()
		elif ((self.current_Frame % 10) == 0 and self.index == 7):
			self.index = 6
		
	def update(self):
		if ((self.current_Frame % 12) == 0):
			#self.xVel = (float(randint(1,51))-25)/6
			self.xVel = randint(1,11)-6
		if (((self.x + self.xVel) < 700) and ((self.x + self.xVel) > 90)):
			self.x = self.x + self.xVel
			self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		self.current_Frame = self.current_Frame + 1
		if ((self.current_Frame % 60) == 0):
			self.current_Frame = 0

		self.spritesheet.draw(self.screen, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		self.idle()
	def shoot(self):
		EnemyBullet(self, self.screen)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, player, screen):
		pygame.sprite.Sprite.__init__(self)
		bullets.add(self)
		self.screen = screen
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
		self.spritesheet.draw(self.screen, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		#self.mask.set_at((self.x, self.y))
		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		pygame.sprite.spritecollide(self, enemys, True, pygame.sprite.collide_mask)
		if self.y < -20:
			bullets.remove(self)

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, enemy, screen):
		pygame.sprite.Sprite.__init__(self)
		bullets.add(self)
		self.screen = screen
		self.x = enemy.x
		self.y = enemy.y - 10
		self.xVel = 0
		self.yVel = 5
		self.spritesheet = spritesheet("Sprites/EnemyBullet.png",1,1)
		self.image = pygame.image.load("Sprites/bullet.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.index = 1
		
	def update(self):
		self.spritesheet.draw(self.screen, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		self.x = self.x + self.xVel
		self.y = self.y + self.yVel
		self.rect.center = ((self.x,self.y))
		#pygame.sprite.spritecollide(self, players, True, pygame.sprite.collide_mask)
		if self.y > 500:
			bullets.remove(self)

class Enemy1(Enemy):
	def __init__(self, x, y, screen):
		Enemy.__init__(self, x, y, screen)
		self.spritesheet = spritesheet("Sprites/enemy1.png",8,1)
	
class Enemy2(Enemy):
	def __init__(self, x, y, screen):
		Enemy.__init__(self, x, y, screen)
		self.spritesheet = spritesheet("Sprites/enemy2.png",8,1)
		self.image = pygame.image.load("Sprites/collison2.png")
		
		
class Enemy3(Enemy):
	def __init__(self, x, y, screen):
		Enemy.__init__(self, x, y, screen)
		self.spritesheet = spritesheet("Sprites/enemy3.png",8,1)
		
class Enemy4(Enemy):
	def __init__(self, x, y, screen):
		Enemy.__init__(self, x, y, screen)
		self.spritesheet = spritesheet("Sprites/enemy4.png",8,1)
		self.image = pygame.image.load("Sprites/collison2.png")
	
def GenLevel(screen):
	difficuly = (level * 5) + 10
	if not enemys :
		for x in range (difficuly):
			PickEnemy(randint(0,4),xPos[randint(0,9)],yPos[randint(0,3)],screen)
			level =  level + 1
		
def PickEnemy(i, x, y, screen):
	if i == 0 :
		Enemy1(x, y, screen)
	if i == 1 :
		Enemy2(x, y, screen)
	if i == 2 :
		Enemy3(x, y, screen)
	if i == 3 :
		Enemy4(x, y, screen)
		
		
		

