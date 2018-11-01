from Tkinter import *
import pygame
from pygame.locals import *
#import sys
import pygame.sprite as sprite
import Spriteslib as Sprites
import shelve
#import joystickLibv2 as Joystick
Console = "PC"


def read_high_score():
        s = open("score.txt", "r")
        if (s.mode == 'r'):
                data = s.read()
        return data


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
highscore = read_high_score()

#Sprites.init()
FPS = 60
class Game(Frame):
        def __init__(self,master, score, lives, waves):
                Frame.__init__(self,master)

                self.startbutton = Button(master, text = "START", fg = "white",bg = "green",  command = self.play, height = 2)
                self.startbutton.pack(side = TOP,fill = X)

                self.button2 = Button(master, text = "QUIT", fg = "white",bg = "red", command = self.quit, height = 2)
                self.button2.pack(side = TOP, fill = X)

                self.img = PhotoImage(file = "space.gif")
                self.highsc = Label(master, text = "HIGH SCORE : " + highscore, fg = "white", bg = "black", height = 1)
                self.highsc.pack(side = BOTTOM, fill = X)

                self.l = Label(master, image = self.img)
                self.l.pack(side = BOTTOM, fill=X)
                self.score = score
                self.lives = lives
                self.waves = waves
                self.dead = False

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
                                        global running
                                        global highscore
                                        running = False
                                        if (int(highscore) < self.score):
                                            self.high_score(self.score)  
                                if event.type == pygame.KEYDOWN:
                                        if event.key==pygame.K_SPACE:
                                            if self.dead == False:
                                                Sprites.Bullet(self.player, screen)
                                        if event.key ==pygame.K_e:
                                                Sprites.Enemy1(300, 50, screen)
                elif (Console == "PI"):
                        mstatus = Joystick.readChannel(1)
                        fstatus = Joystick.readChannel(0)
                        pygame.event.pump()                                 
                        if fstatus == "YES":
                            if self.dead == False:
                                Sprites.Bullet(self.player, screen)

                        if mstatus == "Right":
                                self.player.xVel = 1
                                
                        elif mstatus == "Left":
                                self.player.xVel = -1

                        else:
                                self.player.xVel = 0
                                self.player.yVel = 0

                        for event in pygame.event.get():
                                if event.type == pygame.QUIT: 
                                        global running
                                        running = False
        




#starts the game
        def play(self):
                theClock = pygame.time.Clock()
                background = pygame.image.load('background_image.gif')
                background_size = background.get_size()
                background_rect = background.get_rect()
                global screen
                screen = pygame.display.set_mode(background_size)
                w,h = background_size
                x = 0
                y = 0
                x1 = 0
                y1 = -h
                #Sprites.init()
                self.player = Sprites.Player(250,430, screen)
                global running
                global Console
                running = True
                while running:
                    #screen.blit(background,background_rect) ---- When the FPS was ramped up this was not needed and actually was the cause of our screen tearing
                    pygame.display.update()
                    y1 += 5
                    y += 5
                    screen.blit(background,(x,y))
                    screen.blit(background,(x1,y1))
                    self.score_counter(screen, self.score)
                    self.life_counter(screen, self.lives)
                    self.events(Console)
                    Sprites.GenLevel(screen, self.waves)
                    self.events(Console)
                    Sprites.players.update()
                    Sprites.bullets.update()
                    Sprites.enemys.update()
                    Sprites.enemyBullets.update()
                    if Sprites.enemyDeath():
                        self.score = self.score + 5
                        print "enemy died"
                    if Sprites.playerDeath():
                        if self.lives > 0:
                            self.lives = self.lives - 1
                            self.player = Sprites.Player(250,430, screen)
                            print "player died"
                        else:
                            self.dead = True
                            print "GAME OVER"
                    if y > h:
                        y = -h
                    if y1 > h:
                        y1 = -h
                    pygame.display.flip()
                    pygame.display.update()
                    theClock.tick(FPS)
                pygame.quit()

        def score_counter(self, screen, score):
                textsurface = myfont.render("Score = {}".format(score), False, (255, 255, 255))
                screen.blit(textsurface,(0,420))

        def life_counter(self, screen, lives):
                textsurface = myfont.render("Lives = {}".format(lives), False, (255, 255, 255))
                screen.blit(textsurface,(700,420))
                
        def high_score(self, score):
                s = open("score.txt","w+")#this opens up the file 
                s.write(str(score))
                s.close()
 
        
#ends and exits the game
        def quit(self):
                self.master.destroy()





#########################################################################

#Default window size
WIDTH = 500
HEIGHT = 550
window = Tk()
window.geometry("{}x{}".format(WIDTH,HEIGHT))
window.attributes("-toolwindow",1)
window.title("Attack of The Pi !")
menu = Game(window, score= 0, lives= 5, waves = 1)
window.mainloop()






#########################################################################
