import pygame as py
from enum import Enum
import random
#=====================================

class PlayerState(Enum):
	YOUR = 1
	OPPONENTS = 2
	BATTLE = 3
#=====================================
class CardState(Enum):
	KING = 1
	PRISONER = 2
	PEASENT = 3


#=====================================

class ScreenState(Enum):
	GAMEPLAY = 1
	PAUSED = 2
	OVER_W = 3
	OVER_L = 4

#=====================================
class MouseState(Enum):
	DOWN = 1
	UP = 2
#=====================================
def count_remaining(card_count):
	cards_left_temp = 3
	card_list = []
	kings_left = cards_left_temp - card_count[0]
	prisoners_left = cards_left_temp - card_count[1]
	peasents_left = cards_left_temp - card_count[2]
	for i in range(kings_left):
		card_list.append(CardState.KING)
	for i in range(prisoners_left):
		card_list.append(CardState.PRISONER)
	for i in range(peasents_left):
		card_list.append(CardState.PEASENT)
	return card_list
class SpriteSheet:
	def __innit__(self,image,w,h,target = None):
		self.sheet = image
		self.w = w
		self.h = h
		self.target = target

	def frame_from_sheet(self,r,c):
		frame = py.Surface((27,22), py.SRCALPHA)
		area = py.Rect(c*19,r*8, 35,35)
		frame.blit(self,(0,0),area)
		return py.transform.scale(frame,(60,60))

#=====================================

class Cards:
	def __init__(self):
		self.list = []
	def update_list(self,list):
		super.list = list
	def make_card_in_hand(self,x,y):
		card = py.Rect(x,y,23.5,33.4)
		self.list.append(card)
		return card
	def play(self):
		

class MySprite:
#anim_dict = { (<State1>: | , | , | ) , (<State2>: \,\,\) }
	ANIM_HOLD_FRAMES = 10

	def __init__( self, anim_dict):
		
		self.anim_dict = anim_dict
		self.anim_timer = MySprite.ANIM_HOLD_FRAMES
		self.anim_frame = 0
		self.state = PlayerState.YOURTURN



	def update(self):
		self.anim_timer -= 1
		if self.anim_timer <= 0:
			self.anim_timer = MySprite.ANIM_HOLD_FRAMES
			self.anim_frame += 1
		
	def get_location(self):
		return [self.x,self.y]	


	#Draws image to Surface
	def draw(self,window):
		offset = 30 * len(self.card_list)
		
		for i in self.card_list:
			curr_anim = self.anim_dict[i]
			window.blit(curr_anim,320-(offset/2),300)
			offset +=30
		



	def get_rect(self):
		return self.hitbox.move(self.x,self.y)

#End of class

#=====================================

class Enemy(MySprite):
	
	MOVESPEED = 1
	def __init__(self, anim_dict):
		super().__init__( anim_dict)
		self.card_count= [0,0,0]
		self.cards_in_hand = 9
		self.card = 0
		self.card_list = []
	def enemy_Move(self,card=int(random.random(1,3))):
		if card >= 4:
			return 0
		if PlayerState == PlayerState.OPPONENTS:
			if card == 1 and self.card_count[0] != 3:
				self.card_count[0] +=1
				return card
			elif card == 2 and self.card_count[0] != 3:
				self.card_count[1] +=1
				return card
			elif card == 3 and self.card_count[0] != 3:
				self.card_count[2] +=1
				return card
			else:
				self.enemy_move(card+1)
				self.enemy_move(card-1)
			
	def update(self):
			card =self.enemy_Move()
			if card == 0:
				return None
			elif card == CardState.KING:
				self.card = CardState.KING
				self.cards_in_hand -=1
			elif card == CardState.PRISONER:
				self.card = CardState.PRISONER
				self.cards_in_hand -=1
			elif card == CardState.PEASENT:
				self.card = CardState.PEASENT
				self.cards_in_hand -=1
			
	def draw(self,window):
			offset = 30 * len(self.card_list)
			for i in self.card_list:
				curr_anim = self.anim_dict[i]
				window.blit(curr_anim,320-(offset/2),300)
				offset +=30
			

			
			
			





#=====================================

#start of global variables

#Set up game Window
py.init()
window = py.display.set_mode((640,480))
ScreenState = ScreenState.GAMEPLAY

#Paused  Fonts
font = py.font.SysFont("ariel",20)
paused_surf = font.render("PAUSED??", True,(220,220,220))
paused_cont = font.render("Continue!", True,(220,220,220))
paused_q = font.render("Quit :(", True,(220,220,220))
#Game Over Fonts
winner_text = font.render("WINNER",True,(0,0,0))
loser_text = font.render("YOU LOSE :(",True,(0,0,0))
#---Continue
paused_continue = py.Surface((70,30))
py.draw.rect(paused_continue,(255,0,255),(0,0,70,30))
paused_continue.blit(paused_cont,(4,12))
#---Quit
paused_quit = py.Surface((70,30))
py.draw.rect(paused_quit,(255,0,255),(0,0,70,30))
paused_quit.blit(paused_q,(4,12))
#---Paused Buttons HitBoxs
continue_hitbox = py.Rect(20,20,70,30)
quit_hitbox = py.Rect(20,20,70,30)

#Time
clock = py.time.Clock()

#=====================================


	#Creates Image object
def loadSprite(fname):
	player_image = py.image.load(fname).convert_alpha()
	topleft = player_image.get_at((0,0))
	player_image.set_colorkey(topleft)
	
	return player_image



#=====================================
def frame_from_sheet(sheet,r,c):
	frame = py.Surface((32,32), py.SRCALPHA)
	area = py.Rect(r*24,c*33, 24,33)
	frame.blit(sheet,(0,0),area)
	return py.transform.scale(frame,(30,45))
#=====================================
#Create Mouse Global
#==== mouse_vis = py.mouse.set_visible(True) Default
mouse_loc = py.mouse.get_pos()
#=====================================

#create image surface
player_sheetInc = loadSprite("cards.png")


#=====================================
#set up Player anim_directory
player_anim= []
for r in range(4):
	frame = frame_from_sheet(player_sheetInc,r,0)
	player_anim.append(frame)
enemy_anim=[]
for r in range(4):
	frame = frame_from_sheet(player_sheetInc,r,1)
	enemy_anim.append(frame)
#=====================================
# convert images to sprites
Player = MySprite(player_anim)

enemy = Enemy(enemy_anim)


#=====================================

# Game Loop
running = True
while running: #game loop

		#process input
	for event in py.event.get():
		if event.type == py.QUIT:
			running = False
			break
#Press------------
		elif event.type == py.KEYDOWN:
			
			if event.key == py.K_ESCAPE:
				if ScreenState != ScreenState.PAUSED:
					Player.x_vel=0
					Player.y_vel=0
					ScreenState = ScreenState.PAUSED
					#running = False
				else:
					ScreenState = ScreenState.GAMEPLAY
					
#Release--------------
		
		elif event.type == py.MOUSEBUTTONDOWN:
			MouseState = MouseState.DOWN
			mouse_loc = py.mouse.get_pos()
		elif event.type == py.MOUSEBUTTONUP:
			MouseState = MouseState.UP
						
#update after player input
	Player.update()
	

#=====================================
	if MouseState == MouseState.DOWN:
			
	
		if ScreenState == ScreenState.PAUSED:
			 
			 
			if continue_hitbox.move(260,200).collidepoint(mouse_loc):
				
				ScreenState = ScreenState.GAMEPLAY
			elif quit_hitbox.move(260,250).collidepoint(mouse_loc):
				
				py.quit()
		elif ScreenState == ScreenState.GAMEPLAY:
			for i in Player.card_list:
				if i.collidepoint(mouse_loc):
					player_card = i.play()
					enemy_card = enemy.update()
			gamelogic = Cards.compare(player_card,enemy_card)
			if gamelogic == 1: # Player Wins
				player_Wins += 1
			elif gamelogic == 2: # Player Loses
				enemy_Wins += 1
			
				
#=====================================
#render/draw
#window = (640,480) 
#ADD Player wins and enemy wins animation
# reset cards with updated information
#Optinal: add Instructions
	if ScreenState == ScreenState.PAUSED:
		window.fill((255,255,0))
		window.blit(paused_surf,(280,200))
		window.blit(paused_continue,(280,220))
		window.blit(paused_quit,(280,260))
	elif ScreenState == ScreenState.GAMEPLAY:
		window.fill((0,110,100))

		Player.draw(window)
		enemy.draw(window)
		if player_Wins >= 3:
				screen = py.Surface(100,100)
				screen.fill((255,255,255))
				screen.blit(winner_text,(45,35))
				ScreenState= ScreenState.OVER_W
		if enemy_Wins >= 3:
				screen = py.Surface(100,100)
				screen.fill((255,255,255))
				screen.blit(loser_text,(45,35))
				ScreenState= ScreenState.OVER_L
	py.display.update() 

	clock.tick(30)  
#===================================== 
#end of loop
py.quit()