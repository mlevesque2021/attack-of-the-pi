#main py file
from Tkinter import *

class Game(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        self.startbutton = Button(master, text = "start", fg = "white",bg = "green",  command = self.play, height = 4)
        self.startbutton.pack(side = TOP,fill = X)

        self.button2 = Button(master, text = "quit", fg = "white",bg = "red", command = self.quit, height = 4)
        self.button2.pack(side = TOP, fill = X)
#create play function that starts the game
    def play(self):
        pass
    #create quit function that quits the game
    def quit(self):
        pass


        
