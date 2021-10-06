#!/usr/bin/python3
#use to write app
from tkinter import *
#random is a library in python, i used to randomize number  
from random import random
#library to run //
import threading, time
#list1*list2=>list3
from itertools import product

class App():
	def __init__(self, canvas_size=600):
		self.canvas_size	= canvas_size
		self.width 			= self.canvas_size+105
		self.height			= self.canvas_size

        #where is the buttons
		self.init_layout()
        #what will these button do
		self.init_handlers()
        #defaut values
		self.init_defaults()


	def init_layout(self):
        #create main window, in fact there is just one
		self.root = Tk()
		self.root.title("Jeu de la vie")
		self.root.geometry(f'{self.width}x{self.height}')
		
		self.canvas = Canvas(self.root, width=self.canvas_size, height=self.canvas_size, background='white')
		self.canvas.grid(row=0,column=0)

		self.frame_control = Frame(self.root)
		self.frame_control.grid(row=0, column=1)

		buttons			= ('Initialiser', self.initialize), ('Lancer',self.launch), ('Arreter',self.stop), ('Quitter', self.quit)
		self.buttons	= [ Button(self.frame_control,text=name,command=f) for (name,f) in buttons]

		scales			= ('Taille dela grille', 'n_cell'), ('%de Vie', 'p_alive'), ('Vitesse','speed')
		self.scales		= { key : Scale(self.frame_control, from_=2, to=100, orient='horizontal', label=label) for label,key in scales}

		widgets			= self.buttons[:-1] + list(self.scales.values()) + [self.buttons[-1]]
		
		for i, widget in enumerate(widgets):
			widget.grid(row=i, column=0, sticky='nesw')

		
	def init_handlers(self):
		self.root.protocol("WM_DELETE_WINDOW", self.quit)


	def init_defaults(self):
		self.scales['n_cell'].set(30)
		self.scales['p_alive'].set(20)
		self.scales['speed'].set(1)


	def initialize(self):
		self.stop()
		self.n_cell = int(self.scales['n_cell'].get())
		self.cell_size 		= self.canvas_size/self.n_cell		
		self.p_alive	= self.scales['p_alive'].get()/100
		
		print("Initialize grid.")
		self.state = [[random()<self.p_alive for _ in range(self.n_cell)] for _ in range(self.n_cell)]
		self.draw_state()

	
	def launch(self):
		def periodic_update():
			print("Start updating forever.")
			while True:
				if self.update_loop_stop:
					print("No longer updating.")
					return
				self.update()
                #max is 5 seconds, 0.05 for not chaotic
				delta_t = round (0.05+self.scales['speed'].get()/20.0 , 2)
				print(f"Updated. Next update in {delta_t} seconds")
                #go sleep
				time.sleep(delta_t)

		if not hasattr(self, 'state'):
			print("Please initialize first.")
			return
		
		if self.update_loop_stop:
			self.update_loop_stop = False
			print("Start OR Continue")
			self.thread = threading.Thread(target=periodic_update)		
			self.thread.start()
		else:
			print("Already running")		



	def	stop(self):
		self.update_loop_stop = True


	def update(self):	
		flip_indices = []
		
		for i,j in product(range(self.n_cell), range(self.n_cell)):
			alive = self.state[i][j]
			neighbors = (i-1, j-1), (i-1,j), (j-1, j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)
			n_alive_neighbors = sum([self.state[i][j] if 0<=i<self.n_cell and 0<=j<self.n_cell else 0 for i,j in neighbors])
			under_population 	= alive and n_alive_neighbors < 2
			over_population 	= alive and n_alive_neighbors > 3
			reproduction		= not alive and n_alive_neighbors == 3
			
			if under_population or over_population or reproduction:
				flip_indices.append((i,j))

		for i,j in flip_indices:
			self.state[i][j] = not self.state[i][j]
		
		self.draw_state(flip_indices)


	def draw_state(self, changes=None):
		if changes == None:
			changes = product(range(self.n_cell), range(self.n_cell))
		for i,j in changes:
			rectangle = i*self.cell_size, j*self.cell_size, (i+1)*self.cell_size, (j+1)*self.cell_size
			color = "red" if self.state[i][j] else "white"
			self.canvas.create_rectangle(*rectangle, fill=color)


	def quit(self):
		self.update_loop_stop = True
		self.root.destroy()


if __name__ == "__main__":
	app = App()
	app.root.mainloop()
