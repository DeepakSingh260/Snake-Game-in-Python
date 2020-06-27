import pygame
import random
import time
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans",50)
WIN = pygame.display.set_mode((800,800))
snakes = pygame.transform.scale(pygame.image.load('snake.png'),(32,32))
tail_image = pygame.transform.scale(pygame.image.load('tail.png'),(32,32))
fruites = pygame.transform.scale(pygame.image.load('fruit.png'),(32,32))
change= 1	
gameOver_img = pygame.transform.scale(pygame.image.load('download.png'),(148,72))

class Snake:

	def __init__(self,x,y):
		self.x=x
		self.y= y
		self.xchange = 0
		self.ychange = 0


	def change(self,xchange,ychange):
		self.xchange=xchange
		self.ychange=ychange	
	def move(self):
		self.x+=self.xchange
		self.y+=self.ychange



	def draw(self,win):

		if self.xchange == -32:
			win.blit(pygame.transform.rotate(snakes,180),(self.x,self.y))

		if self.xchange == 32:
			win.blit(snakes,(self.x,self.y))
		if self.ychange == -32:
			win.blit(pygame.transform.rotate(snakes,90),(self.x,self.y))
		if self.ychange == 32:
			win.blit(pygame.transform.rotate(snakes,270),(self.x,self.y))			
	def get_mask(self):
		return pygame.mask.from_surface(snakes)

class Tail:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		print('tail created')

	def move(self,x,y):
		self.x=x
		self.y=y

	def draw(self,win):	
		win.blit(tail_image,(self.x,self.y))

	def match(self,snake):

		snake_mask = snake.get_mask()
		tail_mask = pygame.mask.from_surface(tail_image)

		tail_offest = (self.x - round(snake.x),self.y - round(snake.y))

		if snake_mask.overlap(tail_mask,tail_offest):
			return True	

		
		return False	


class Fruit:
	def __init__(self):
		self.x = random.randrange(32,764)
		self.y= random.randrange(32,764)

	def draw(self,win):
		win.blit(fruites,(self.x,self.y))



	def match(self,snake):
		snake_mask = snake.get_mask()

		fruit_mask = pygame.mask.from_surface(fruites)
		fruit_offset = (self.x - round(snake.x),self.y - round(snake.y))

		if snake_mask.overlap(fruit_mask,fruit_offset):
			return True

		return False	

def gameLoose(snake,fruits,tails,score):
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_SPACE:
				return False

	window_draw(snake,fruits,tails,score,loose=True)			
	return True							

def window_draw(snake,fruits,tails,score , loose = None):
	Win = pygame.display.set_mode((800,800))
	for fruit in fruits:
		fruit.draw(Win)
	snake.draw(Win)
	for tail in tails:
		tail.draw(Win)
	Score = FONT.render('Score'+str(score),1,(255,255,255))
	Win.blit(Score,(10,10)) 
	if loose:
		Win.blit(gameOver_img,(300,400))	

	pygame.display.update()
def main():
	global win
	win = WIN
	clock = pygame.time.Clock()	
	snake = Snake(400,400)
	fruits = [Fruit()]
	score =0
	tails =[]
	run =True
	while run:
		clock.tick(15)
		lt = []
		List = []
		for fruit in fruits:
			if fruit.match(snake):
				score+=1
				lt.append(fruit)
				fruits.append(Fruit())
				if snake.xchange == -32:
					tails.append(Tail(snake.x+32*len(tails)+32,snake.y))
				if snake.xchange == 32:
					tails.append(Tail(snake.x-32*len(tails)-32,snake.y))
				if snake.ychange == -32:
					tails.append(Tail(snake.x,snake.y+32*len(tails)+32))
				if snake.ychange == 32:
					tails.append(Tail(snake.x,snake.y-32*len(tails)-32))

		for l in lt:
			fruits.remove(l) 
		i = len(tails)
		while i>=1:
			if i==1:
				tails[0].move(snake.x,snake.y)
			else :	
				tails[i-1].move(tails[i-2].x,tails[i-2].y)
			i-=1
		for event in pygame.event.get():

			if event.type  == pygame.QUIT:

				run = False

			if event.type == pygame.KEYDOWN:	

				if event.key == pygame.K_DOWN:
					snake.change(0,32)
					

				if event.key == pygame.K_UP:
					snake.change(0,-32)
					
				
				if event.key == pygame.K_RIGHT:
					snake.change(32,0)
					
					
				if event.key == pygame.K_LEFT:
					snake.change(-32,0)
							

		
		
		snake.move()
		for tail in tails:
			if tail.match(snake):
				score = 0
				i = len(tails)	
				while i>1:
					tails.remove(tails[i-1])
					i=i-1

				tails.remove(tails[0])
				snake.xchange=0
				snake.ychange=0

				while gameLoose(snake,fruits,tails,score):
					pass


		
		window_draw(snake,fruits,tails,score)



main()		