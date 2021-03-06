from Tkinter import *
import pygame
from pygame import mixer
from pygame.locals import *
#import sys
import pygame.sprite as sprite
import Spriteslib as Sprites
import shelve
from time import sleep
#import joystickLibv2 as Joystick
Console = "PC"

def read_high_score():
		s = open("score.txt", "r")
		if (s.mode == 'r'):
				data = s.read()
		return data

highscore = read_high_score()


class Menu(Frame):
		def __init__(self,master):
				Frame.__init__(self,master)

				self.startbutton = Button(master, text = "START", fg = "white",bg = "green",  command = self.CreateGame, height = 2)
				self.startbutton.pack(side = TOP,fill = X)

				self.button2 = Button(master, text = "QUIT", fg = "white",bg = "red", command = self.quit, height = 2)
				self.button2.pack(side = TOP, fill = X)

				self.img = PhotoImage(file = "resources/space.gif")
				self.highsc = Label(master, text = "HIGH SCORE : " + highscore, fg = "white", bg = "black", height = 1)
				self.highsc.pack(side = BOTTOM, fill = X)                                
				self.l = Label(master, image = self.img)
				self.l.pack(side = BOTTOM, fill=X)
	
 		def CreateGame(self):
			Game(score= 0, lives= 5, waves = 1)

				

class Game():
	def __init__(self, score, lives, waves):
		pygame.init()
		mixer.init()
		self.laser = pygame.mixer.Sound("resources/Sounds/defaultLaser.ogg")
		self.alienDestroyed = pygame.mixer.Sound("resources/Sounds/galaga_destroyed.ogg")
		self.playerDestroyed = pygame.mixer.Sound("resources/Sounds/explosion.ogg")
		self.ChannelA = pygame.mixer.Channel(0)
		self.ChannelB = pygame.mixer.Channel(1)
		self.ChannelC = pygame.mixer.Channel(2)
		self.background = pygame.image.load('resources/background_image.gif')
		self.background_size = self.background.get_size()
		self.background_rect = self.background.get_rect()
		self.screen = pygame.display.set_mode(self.background_size)
		self.score = score
		self.lives = lives
		self.waves = waves
		self.running = True
		self.gameOver = False
		self.dead = False
		self.play()

	@property
	def score(self):
			return self._score

	@score.setter
	def score(self, value):
			self._score = value

	@property
	def lives(self):
			return self._lives
	
	@lives.setter
	def lives(self, value):
			self._lives = value

	@property
	def waves(self):
			return self._waves
	
	@waves.setter
	def waves(self, value):
			self._waves = value


	def events(self, Console):
			if (Console == "PC"):
					keys = pygame.key.get_pressed()

					if keys[K_RIGHT]:
							self.player.xVel = 5

							
					elif keys[K_LEFT]:
							self.player.xVel = -5


					else:
							self.player.xVel = 0
							self.player.yVel = 0


					for event in pygame.event.get():
							if event.type == pygame.QUIT:
									global highscore
									self.running = False
									if (int(highscore) < self.score):
										self.high_score(self.score)
							if event.type == pygame.KEYDOWN:
									if event.key==pygame.K_SPACE:
										if self.dead == False:
											self.player.shoot()
											self.ChannelA.play(self.laser)
									if event.key ==pygame.K_e:
											Sprites.Enemy1(300, 50, self.screen)
			elif (Console == "PI"):
					mstatus = Joystick.readChannel(1)
					fstatus = Joystick.readChannel(0)
					pygame.event.pump()									
					if fstatus == "YES":
						if self.dead == False:
							self.player.shoot()
							self.ChannelA.play(self.laser)

					if mstatus == "Right":
							self.player.xVel = 5
							
					elif mstatus == "Left":
							self.player.xVel = -5

					else:
							self.player.xVel = 0
							self.player.yVel = 0

					for event in pygame.event.get():
							if event.type == pygame.QUIT: 
									self.running = False
	




#starts the game
	def play(self):
			pygame.font.init()
			theClock = pygame.time.Clock()
			w,h = self.background_size
			x = 0
			y = 0
			x1 = 0
			y1 = -h
			#Sprites.init()
			self.player = Sprites.Player(265,430, self.screen)
			global Console
			self.running = True
			current_frame = 0
			time = 0
			while self.running:
				#screen.blit(background,background_rect) ---- When the FPS was ramped up this was not needed and actually was the cause of our screen tearing
				pygame.display.update()
				y1 += 5
				y += 5
				current_frame = current_frame + 1
				if current_frame % 60 == 0:
					current_frame = 0
					time = time + 1
				self.screen.blit(self.background,(x,y))
				self.screen.blit(self.background,(x1,y1))
				Sprites.players.update()
				Sprites.linkedPlayers.update()
				Sprites.bullets.update()
				Sprites.enemys.update()
				Sprites.enemyBullets.update()
				Sprites.beams.update()
				Sprites.ships.update()
				self.side_panel(self.screen)
				self.score_counter(self.screen, self.score)
				self.life_counter(self.screen, self.lives)
				self.wave_counter(self.screen, self.waves)
				self.events(Console)
				if (len(Sprites.enemys) < 1 and time > 2):
					time = 0
					self.waves += 1
					Sprites.bullets.empty()
					self.dead = True
				elif (len(Sprites.enemys) < 1 and time < 2):
					myfont = pygame.font.Font("resources/Fonts/ScifiAdventure.otf", 24)
					textsurface = myfont.render("WAVE {}".format(self.waves), False, (255, 255, 255))
					self.screen.blit(textsurface,(395,215))
					pygame.display.update()
				elif (len(Sprites.enemys) < 1 and time == 2 and current_frame == 0):
					Sprites.GenLevel(self.screen, self.waves)
					Sprites.enemys.update()
					self.dead = False
				self.events(Console)
				if Sprites.enemyDeath():
					#happens when enemy dies
					self.score = self.score + 5
					self.ChannelB.play(self.alienDestroyed)
				if Sprites.playerDeath(self.player):
					if self.lives > 0:
						#happens when player dies but the game is not over
						self.lives = self.lives - 1
						self.player = Sprites.Player(250,430, self.screen)
					else:
						#happens when game is over
						self.gameOver = True
				if self.gameOver == True:
					self.dead = True
					myfont = pygame.font.Font("resources/Fonts/ScifiAdventure.otf", 24)
					textsurface = myfont.render("GAME OVER", False, (255, 255, 255))
					self.screen.blit(textsurface,(395,215))
				if y > h:
					y = -h
				if y1 > h:
					y1 = -h
				pygame.display.flip()
				pygame.display.update()
				theClock.tick(60)
			Sprites.killAll()
			pygame.display.quit()
			pygame.quit()

	def side_panel(self, screen):
		panel = pygame.Surface((150, 600))
		panel.fill((77, 90, 142))
		screen.blit(panel,(0,0))

	def score_counter(self, screen, score):
			myfont = pygame.font.Font("resources/Fonts/ScifiAdventure.otf", 12)
			textsurface = myfont.render("Score: {}".format(score), False, (255, 255, 255))
			screen.blit(textsurface,(0,0))

	def life_counter(self, screen, lives):
			myfont = pygame.font.Font("resources/Fonts/ScifiAdventure.otf", 12)
			textsurface = myfont.render("Lives: {}".format(lives), False, (255, 255, 255))
			screen.blit(textsurface,(0,25))

	def wave_counter(self, screen, wave):
			myfont = pygame.font.Font("resources/Fonts/ScifiAdventure.otf", 12)
			textsurface = myfont.render("Wave: {}".format(wave), False, (255, 255, 255))
			screen.blit(textsurface,(0,50))


	def high_score(self, score):
			s = open("score.txt","w+")#this opens up the file 
			s.write(str(score))
			s.close()





#########################################################################

#Default window size
WIDTH = 500
HEIGHT = 550
window = Tk()
window.geometry("{}x{}".format(WIDTH,HEIGHT))
window.title("Attack of The Pi !")
menu = Menu(window)
window.mainloop()






#########################################################################
