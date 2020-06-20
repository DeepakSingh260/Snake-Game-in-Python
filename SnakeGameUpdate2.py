import pygame
import random
import time
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans",50)
WIN = pygame.display.set_mode((800,800))
snake_image = pygame.transform.scale(pygame.image.load('snake.png'),(32,32)) 
fruit_image = pygame.transform.scale(pygame.image.load('fruit.png'),(32,32))
tail_image = pygame.transform.scale(pygame.image.load('tail.png'),(32,32))
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
		if self.xchange == 32:
			win.blit(snake_image,(self.x,self.y))
		if self.xchange == -32:
			win.blit(pygame.transform.rotate(snake_image,180),(self.x,self.y))	
		if self.ychange == 32:
			win.blit(pygame.transform.rotate(snake_image,270),(self.x,self.y))

		if self.ychange == -32:
			win.blit(pygame.transform.rotate(snake_image,90),(self.x,self.y))

	def get_mask(self):
		return pygame.mask.from_surface(snake_image)	
class Tail:
	def __init__(self,x,y):
		self.x = x
		self.y = y


	def draw(self , win):
		win.blit(tail_image,(self.x , self.y))	


	def move(self,x,y):
		self.x=x
		self.y = y	

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

def window_draw(win , snake,fruits,score,tails):
	Win = pygame.display.set_mode((800,800))
	snake.draw(Win)
	for fruit in fruits:
		fruit.draw(Win)

	for tail in tails:
		tail.draw(Win)	
	Score = FONT.render('Score :'+ str(score),1,(255,255,255))
	win.blit(Score,(10,10))	
	pygame.display.update()
def main():
	global win 
	win = WIN
	run = True
	tails = []
	snake = Snake(400,400)
	fruits = [Fruit()]
	score =0
	clock = pygame.time.Clock()
	while run:
		clock.tick(15)
		
		lt =[]
		for fruit in fruits:
			if fruit.match(win ,snake):
				score+=1
				lt.append(fruit)
				fruits.append(Fruit())
				if snake.xchange == -32:
					tails.append(Tail(snake.x+32*len(tails)+32,snake.y))
				if snake.xchange == 32:
					tails.append(Tail(snake.x-32*len(tails)-32,snake.y))
				if snake.ychange == -32:
					tails.append(Tail(snake.x,snake.y+32*len(tails)+32))
				if snake.ychange == -16:
					tails.append(Tail(snake.x,snake.y-32*len(tails)-32))		
		for l in lt :
			fruits.remove(l)	


		i=len(tails)
		while i>=1:
				if i == 1:
					tails[0].move(snake.x,snake.y)

				else:
					tails[i-1].move(tails[i-2].x,tails[i-2].y)		
				i-=1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			elif event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_UP:
					snake.change(0,-32)

				elif event.key == pygame.K_DOWN:
					snake.change(0,32)

				elif event.key == pygame.K_LEFT:
					snake.change(-32,0)
				
				elif event.key == pygame.K_RIGHT:
					snake.change(32,0)
		snake.move()			
		window_draw(win , snake,fruits,score,tails)
main()