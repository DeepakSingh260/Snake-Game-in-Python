import pygame
import random
import time
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans",50)
WIN = pygame.display.set_mode((800,800))
snake_image = pygame.transform.scale(pygame.image.load('snake.png'),(32,32)) 
fruit_image = pygame.transform.scale(pygame.image.load('fruit.png'),(32,32))
class Snake:
	def __init__(self,x,y):
		self.x= x
		self.y = y
		self.xchange = 0
		self.ychange = 0
	def move(self):
		self.x+=self.xchange
		self.y+=self.ychange


	def change(self,xchange,ychange):
		self.xchange = xchange
		self.ychange = ychange	
	def draw(self,win):
		win.blit(snake_image,(self.x,self.y))


	def get_mask(self):
		return pygame.mask.from_surface(snake_image)	

class Fruit:
	def __init__(self):
			self.x = random.randrange(0,768)
			self.y = random.randrange(0,768)

	def draw(self,win):
		win.blit(fruit_image,(self.x,self.y))	


	def match(self,win , snake):
		snake_mask = snake.get_mask()
		fruit_mask = pygame.mask.from_surface(fruit_image)

		fruit_offset = ((self.x - round(snake.x)),(self.y-round(snake.y)))

		if snake_mask.overlap(fruit_mask,fruit_offset):
			return True

		return False					

def window_draw(win , snake,fruits,score):
	Win = pygame.display.set_mode((800,800))
	snake.draw(Win)
	for fruit in fruits:
		fruit.draw(Win)
	Score = FONT.render('Score :'+ str(score),1,(255,255,255))
	win.blit(Score,(10,10))	
	pygame.display.update()
def main():
	global win 
	win = WIN
	run = True
	snake = Snake(400,400)
	fruits = [Fruit()]
	score =0
	clock = pygame.time.Clock()
	while run:
		clock.tick(30)
		
		lt =[]
		for fruit in fruits:
			if fruit.match(win ,snake):
				score+=1
				lt.append(fruit)
				fruits.append(Fruit())


		for l in lt :
			fruits.remove(l)		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			elif event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_UP:
					snake.change(0,-16)

				elif event.key == pygame.K_DOWN:
					snake.change(0,16)

				elif event.key == pygame.K_LEFT:
					snake.change(-16,0)
				
				elif event.key == pygame.K_RIGHT:
					snake.change(16,0)
		snake.move()			
		window_draw(win , snake,fruits,score)
main()