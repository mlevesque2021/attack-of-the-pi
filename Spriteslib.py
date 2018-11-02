import random
import pygame
from pygame.locals import *
from random import randint
from pygame import mixer

CENTER_HANDLE = 4
pygame.init()
mixer.init()
#define some groups


bullets = pygame.sprite.Group()
enemyBullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()
players = pygame.sprite.Group()
xPos = [x * 48 for x in range(2,20)]
yPos = [y * 20 for y in range (1,5)]



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


	def __init__(self, x, y, screen, level):
		pygame.sprite.Sprite.__init__(self)
		self.ChannelD = pygame.mixer.Channel(3)
		self.bulletSound = pygame.mixer.Sound("laser_widebeam.ogg") 
		enemys.add(self)
		self.screen = screen
		self.level = level
		self.current_Frame = 0
		self.x = x
		self.xStart = 0
		self.y = y
		self.yStart = 0
		self.xVel = 1
		self.yVel = 0
		self.spritesheet = spritesheet("Sprites/enemy3.png",8,1)
		self.image = pygame.image.load("Sprites/enemy collison.png")
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.index = 7
		self.moving = 0
		self.lock = 1

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
		elif ((self.current_Frame % 10) == 0 and self.index == 7):
			self.index = 6

	def update(self):
		if ((self.current_Frame % 12) == 0):
			self.xVel = randint(1,11)-6

		if (((self.x + self.xVel) < 700) and ((self.x + self.xVel) > 90) and self.lock == 1):
			self.x = self.x + self.xVel
			self.y = self.y + self.yVel

		self.rect.center = ((self.x,self.y))
		self.current_Frame = self.current_Frame + 1
		if ((self.current_Frame % 60) == 0):
			self.current_Frame = 0

		self.spritesheet.draw(self.screen, self.index % self.spritesheet.totalCellCount, self.x, self.y, CENTER_HANDLE)
		self.idle()
		self.shoot()
		ran = randint(0,((20-self.level)+1000))
		if (ran == 7 and self.lock == 1):
			self.xStart = self.x
			self.yStart = self.y
			self.dropDown(self.xStart,self.yStart)
			self.lock = 0
		elif (self.lock == 0 and self.moving < 100):
			self.dropDown(self.xStart,self.yStart)
			self.moving = self.moving + 1
		else:
			self.moving = 0
			self.lock = 1

	def shoot(self):
		ran = randint(0,((20-self.level)+10))
		if ran == 1:
			self.ChannelD.play(self.bulletSound)
			EnemyBullet(self, self.screen)

			#self.dropDown(self.x, self.y)
	
		ran = randint(0,((200-self.level)+100))
		if ran == 5:
			EnemyBullet(self, self.screen)

	def dropDown(self, x, y):
		xMove = 0
		self.xVel = 1
		if self.y < 350:
			#print self.x
			self.x = self.x + self.xVel
			xMove = self.x - x
			self.y = 0.02*(xMove ** 2) + y
			print"{},{}".format(self.x, self.y)

		

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
		#pygame.sprite.spritecollide(self, enemys, True, pygame.sprite.collide_mask)
		if self.y < -20:
			bullets.remove(self)


class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, enemy, screen):
		pygame.sprite.Sprite.__init__(self)
		enemyBullets.add(self)
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
	def __init__(self, x, y, screen, level):
		Enemy.__init__(self, x, y, screen, level)
		self.spritesheet = spritesheet("Sprites/enemy1.png",8,1)
	
class Enemy2(Enemy):
	def __init__(self, x, y, screen, level):
		Enemy.__init__(self, x, y, screen, level)
		self.spritesheet = spritesheet("Sprites/enemy2.png",8,1)
		self.image = pygame.image.load("Sprites/collison2.png")
		
		
class Enemy3(Enemy):
	def __init__(self, x, y, screen, level):
		Enemy.__init__(self, x, y, screen, level)
		self.spritesheet = spritesheet("Sprites/enemy3.png",8,1)
		
class Enemy4(Enemy):
	def __init__(self, x, y, screen, level):
		Enemy.__init__(self, x, y, screen, level)
		self.spritesheet = spritesheet("Sprites/enemy4.png",8,1)
		self.image = pygame.image.load("Sprites/collison2.png")
	
def GenLevel(screen, level):
	difficuly = (level * 5) + 10
	if not enemys :
		for x in range (difficuly):
			PickEnemy(randint(0,4),xPos[randint(0,9)],yPos[randint(0,3)],screen,level)
			level =  level + 1
		
def PickEnemy(i, x, y, screen, level):
	if i == 0 :
		Enemy1(x, y, screen, level)
	if i == 1 :
		Enemy2(x, y, screen, level)
	if i == 2 :
		Enemy3(x, y, screen, level)
	if i == 3 :
		Enemy4(x, y, screen, level)
		
def enemyDeath():
	if pygame.sprite.groupcollide(bullets, enemys, True, pygame.sprite.collide_mask):
		return True
	else:
		return False
		
def playerDeath():
	if pygame.sprite.groupcollide(enemyBullets, players, True, pygame.sprite.collide_mask):
		return True
	else:
		return False
	
def killAll():
	enemys.empty()
	players.empty()
	bullets.empty()
	enemyBullets.empty()
