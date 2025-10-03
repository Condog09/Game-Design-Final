#-----------------------------------------------
#Import

import pygame as py
from enum import Enum
import random
#-----------------------------------------------
#States

#===============================================
class GroundState(Enum):			#
	GROUNDED = 1				#
	AIR = 2					#
	WALL = 3				#
#===============================================
#===============================================
class ScreenState(Enum):			#
	GAMEPLAY = 1				#
	PAUSED = 2				#
#===============================================
class AnimationState(Enum):			#
	IDLE = 0				#
	MOVING = 1				#
	JUMPING = 2				#
	FALLING = 3				#
	LANDING = 4				#
	ATTACK = 5				#
#===============================================
class MouseState(Enum):				#
	DOWN = 1				#
	UP = 2					#
#===============================================
#===============================================
class EnemyState(Enum):				#
	IDLE = 1				#
	MOVING = 2				#
	JUMPING = 3				#
#===============================================

#Classes
#=======================================================================
class Platforms:							#
	def __init__(self,image):					#
		self.image = image					#
		self.list = []						#	
	def place(self,x,y,w,h):					#
		shape = py.Rect(x,y,w,h)				#
		self.list.append(shape)					#
	def draw(self,world):						#
		for i in self.list:					#
			x_val = i.x					#
			y_val = i.y					#
			warp = py.transform.scale(self.image,(i.w,i.h))	#
			world.blit(warp,(x_val,y_val))			#
									#
	def update(self,player):					#
		dx = player.x_vel					#
		dy = player.y_vel					#
		bool = False						#
		p_rect = player.get_rect()				#
		New_rect = p_rect.move(dx,dy)				#
		for i in self.list:					#
			T_rect = i					#
			if i.colliderect(p_rect.move(0,dy)):		#
		#Do something; Handle Vertical Collision		#
				dy = 0					#
				bool = True				#
									#
			if i.colliderect(p_rect.move(dx,0)):		#
		#Do something; Handle Horazontal Collision		#
				dx = 0					#
				bool = True				#
		return dx,dy,bool					#
#=======================================================================
class Tiles(Platforms):
	def __init__(self,image,grid,world):
		super().__init__(image)
		self.worldW, self.worldH = world.get_size()
		self.grid = grid
		self.block_sizeX = self.worldW//len(grid)
		self.block_sizeY = self.worldH//len(grid[0])
		
	def create(self):
	#By adding a world object directory you can have diffrent looking
	#objects based off of what # is in the grid.
		countI = 0
		countJ = 0
		
		#print(self.block_sizeX)
		for i in range(len(self.grid)):
			self.block_sizeX = self.worldW//len(self.grid[i])
			self.block_sizeY = self.worldH//len(self.grid)
			for j in range(len(self.grid[i])):
				
				if self.grid[i][j] == 1:
					super().place(j*self.block_sizeX,i*self.block_sizeY,self.block_sizeX,self.block_sizeY)
				
#=======================================================================
#===============================================================
	#Creates Image object					#
def loadSprite(fname):						#
	player_image = py.image.load(fname).convert_alpha()	#
	topleft = player_image.get_at((0,0))			#
	player_image.set_colorkey(topleft)			#
	return player_image					#
#===============================================================
#=======================================================================
def frame_from_sheet(sheet,r,c,f_sizeX,f_sizeY,object_size):		#
	frame = py.Surface((21,24), py.SRCALPHA)			#
	area = py.Rect(r*f_sizeX,c*f_sizeY, object_size,object_size)	#
	frame.blit(sheet,(0,0),area)					#
	return py.transform.scale(frame,(59,59))			#
#=======================================================================
#=======================================================================
class MySprite:								#			
	ANIM_HOLD_FRAMES = 10						#
									#
	def __init__( self, anim_dict , x, y , hitbox):			#
									#
		self.anim_dict = anim_dict				#
		self.x = x						#
		self.x_vel = 0						#
		self.y = y						#
		self.y_vel = 0						#
		self.hitbox = hitbox					#
		self.anim_timer = MySprite.ANIM_HOLD_FRAMES		#
		self.anim_frame = 0					#
		self.state = AnimationState.IDLE			#
									#
	def get_location(self):						#
		return [self.x,self.y]					#
									#
	def get_rect(self):						#
		return self.hitbox.move(self.x,self.y)			#
									#
	def set_state(self,new_state):					#
		self.state = new_state					#
									#
	def update(self):						#
		self.x += self.x_vel					#
		self.y += self.y_vel					#
		self.anim_timer -= 1					#
		if self.anim_timer <= 0:				#
			self.anim_timer = MySprite.ANIM_HOLD_FRAMES	#
			self.anim_frame += 1				#
	def draw(self,world,bool):					#
									#
		curr_anim = self.anim_dict[self.state]			#
		curr_frame = curr_anim[self.anim_frame % len(curr_anim)]#
		if bool == True:					#
			curr_frame = py.transform.flip(curr_frame,
True,False)								#
		world.blit(curr_frame,(self.x,self.y))			#
#=======================================================================
#===============================================================================
class Enemy(MySprite):								#
	MOVEACCEL = 1								#
	MAX_MOVESPEED = 1							#
	def __init__(self, anim_dict , x, y , hitbox, player_location=None,KnockBack_Res = 0):	#
		super().__init__( anim_dict , x, y , hitbox)			#
		self.player_location = player_location				#
		self.state = EnemyState.IDLE					#
		self.left = False						#
		self.directionX = 0						#
		self.drectionY = 0						#
		self.KnockBack_res = KnockBack_Res				#
	def new_playerLocation(self,player_Location):				#
		self.player_location = player_Location				#
	def knockback(self,strength,Player):						#
		self.directionX = int(self.x - Player.x)		#
		self.directionY = int(self.y - Player.y)		#
		knockback_x, knockback_y = (0,0)				#
		if self.KnockBack_res < strength:				#
			if self.directionX > 0:					#
				knockback_x = strength - self.KnockBack_res	#
			elif self.directionX < 0:				#
				knockback_x = -strength + self.KnockBack_res	#
			if self.directionY > 0:					#
				knockback_y = -strength + self.KnockBack_res	#
			elif self.directionY < 0:				#
				knockback_y = strength - self.KnockBack_res	#
		return knockback_x,knockback_y					#
	def enemy_Move(self):							#
		MAX_MOVESPEED = self.MAX_MOVESPEED				#
		MOVEACCEL = self.MOVEACCEL					#
		self.directionX = int(self.x - self.player_location[0])		#
		self.directionY = int(self.y - self.player_location[1])		#
		if self.directionX == 0:					#
			self.x_vel = 0						#
			self.state = EnemyState.IDLE				#
		if self.directionY == 0:					#
			self.y_vel = 0						#
		if self.directionX == 0:					#
			self.state = EnemyState.IDLE				#
		if self.directionX > 0:						#
			if self.x_vel > -MAX_MOVESPEED:				#
				self.state = EnemyState.MOVING			#
				self.x_vel -= self.MOVEACCEL			#
				self.left = False				#
			if self.x_vel < -MAX_MOVESPEED:				#
				self.x_vel = -MAX_MOVESPEED			#
		if self.directionX < 0:						#
			if self.x_vel < MAX_MOVESPEED:				#
				self.state = EnemyState.MOVING			#
				self.x_vel += self.MOVEACCEL			#
				self.left = True				#
			if self.x_vel > MAX_MOVESPEED:				#
				self.x_vel = MAX_MOVESPEED			#
		if self.directionY > 0:						#
			if self.y_vel < MAX_MOVESPEED:				#
				self.state = EnemyState.MOVING			#
				self.y_vel -= self.MOVEACCEL			#
			if self.y_vel > MAX_MOVESPEED:				#
				self.y_vel = MAX_MOVESPEED			#
		if self.directionY < 0:						#
			if self.y_vel > -MAX_MOVESPEED:				#
				self.state = EnemyState.MOVING			#
				self.y_vel += self.MOVEACCEL			#
			if self.y_vel < MAX_MOVESPEED:				#
				self.y_vel = MAX_MOVESPEED			#
	def update(self,tiles):							#
		if ScreenState == ScreenState.GAMEPLAY:				#		
			self.enemy_Move()					#
			self.x_vel,self.y_vel,bool = tiles.update(self)	#
			self.x += self.x_vel					#
			self.y += self.y_vel					#
			self.anim_timer -= 1					#
			if self.anim_timer <= 0:				#
				self.anim_timer = MySprite.ANIM_HOLD_FRAMES	#
				self.anim_frame += 1				#
			if EnemyState == EnemyState.IDLE:			#
				self.state = EnemyState.IDLE			#
			elif EnemyState == EnemyState.MOVING:			#
				self.state = EnemyState.MOVING			#
#===============================================================================
class pause:
	def __init__(self,bool,screen,world):
		if bool == True:
			world.fill((0,155,200))
			screen.fill((255,255,0))
			screen.blit(paused_surf,(280,200))
			screen.blit(paused_continue,(280,220))
			screen.blit(paused_quit,(280,260))
		if bool == False:
			world.fill((0,155,200))
			screen.fill((100,110,100))

#===============================================================================
#-----------------------------------------------
world_Grid = [
[0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1],
[0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
[0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1],
[1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1],
[0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,1,1,1,0,0,0,0,1,0,1],
[1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#-----------------------------------------------
#Start of Global Variables
LIGHT_GRAV = 0.5
STANDARD_GRAV = 1
HEAVY_GRAV = 2 

STANDARD_FRIC = 1

py.init()
#-----------------------------------------------
world = py.Surface((1280,480))
world_width,world_height = world.get_size()
screen = py.display.set_mode((640,480))
screen_cords = [0,0]
#screen_cords = (0,0)
#-----------------------------------------------
ScreenState = ScreenState.GAMEPLAY
mouse_loc = py.mouse.get_pos()
Gravity = STANDARD_GRAV
clock = py.time.Clock()
 
#-----------------------------------------------
#Hitboxes

P_hitbox = py.Rect(20,20,16,16)
E_hitbox = py.Rect(0,0,32,32)
ES_hitbox = py.Rect(16,8,16,16)

continue_hitbox = py.Rect(20,20,70,30)
quit_hitbox = py.Rect(20,20,70,30)
#-----------------------------------------------
#Create Fonts

font = py.font.SysFont("ariel",20)
paused_surf = font.render("PAUSED", True,(220,220,220))
paused_cont = font.render("Continue", True,(220,220,220))
paused_q = font.render("Quit", True,(220,220,220))
#---Continue
paused_continue = py.Surface((70,30))
py.draw.rect(paused_continue,(0,0,0),(0,0,70,30))
paused_continue.blit(paused_cont,(4,12))
#---Quit
paused_quit = py.Surface((70,30))
py.draw.rect(paused_quit,(255,0,0),(0,0,70,30))
paused_quit.blit(paused_q,(4,12))
#-----------------------------------------------
#Sprites

#create image surfaces
player_sheetInc = loadSprite("Old hero.png")
enemy_sheetInc = loadSprite("Old enemies.png")

#set up Player Animation Directory
left = False
idle_anim= []
moving_anim =[]
jump_anim = []
fall_anim = []
land_anim = []
attack_anim = []
# IDLE
for r in range(4):
	frame = frame_from_sheet(player_sheetInc,r,0,16,16,17)
	idle_anim.append(frame)	
#MOVING	
for r in range(6):
	frame = frame_from_sheet(player_sheetInc,r,1.1,16,16,17)
	moving_anim.append(frame)
#JUMPING
frame = frame_from_sheet(player_sheetInc,0,2.1,16,16,17)
jump_anim.append(frame)
#LANDING
frame = frame_from_sheet(player_sheetInc,1,2.1,16,16,17)
land_anim.append(frame)
frame = frame_from_sheet(player_sheetInc,2,2.1,16,16,17)
land_anim.append(frame)
#FALLING	
frame = frame_from_sheet(player_sheetInc,3,2.1,16,16,17)
fall_anim.append(frame)
for r in range(3):
	frame = frame_from_sheet(player_sheetInc,r,4.1,16,16,17)
	attack_anim.append(frame)


Player_direct = {AnimationState.IDLE : idle_anim, AnimationState.MOVING : moving_anim, AnimationState.JUMPING : jump_anim, AnimationState.FALLING : fall_anim, AnimationState.LANDING : land_anim,AnimationState.ATTACK : attack_anim }

Player = MySprite(Player_direct,50,200,P_hitbox)

#set up Enemy Animation Directory
moving_animE=[]
idle_animE = []
enemy_list = []
for r in range(1):
	frame = frame_from_sheet(enemy_sheetInc,r,1,16,16,15.5)
	idle_animE.append(frame)
t = 216
for i in range(3):
	for r in range(6):
		frame = frame_from_sheet(enemy_sheetInc,r,1,16,16,15.5)
		moving_animE.append(frame)
	Enemy_direct = {EnemyState.IDLE : idle_animE, EnemyState.MOVING : moving_animE}
	enemy = Enemy(Enemy_direct,t,100,E_hitbox)
	enemy_list.append(enemy)
	t += 50

#Enemy = Enemy(Enemy_direct,216,100,E_hitbox,Player.get_location())
#-----------------------------------------------
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Make Platforms
base_Plat = py.Surface((120,30))
base_Plat.fill((255,255,0))
#constructor = Platforms(base_Plat,120,30)
#constructor.place(0,300)
#constructor.place(200,220)
#constructor.place(400,200)
constructor = Tiles(base_Plat,world_Grid,world)
constructor.create()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Game Loop
released = False
running = True
Jumped = False
attack = False
attackBox = py.Surface((5,5))
attackBox.fill((155,0,10))
py.draw.rect(attackBox,(255,255,255),(100,100,50,50))	
while running: #game loop
	Player.y_vel += STANDARD_GRAV
		#process input
	if GroundState == GroundState.GROUNDED:
		Jumped = False
	if Player.x_vel != 0 and released == True:
		if Player.x_vel > 0:
			Player.x_vel -= STANDARD_FRIC
			if  Player.x_vel < 0:
				Player.x_vel = 0 
		elif Player.x_vel < 0:
			Player.x_vel += STANDARD_FRIC
			if Player.x_vel > 0:
				Player.x_vel = 0




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


					
			if ScreenState == ScreenState.GAMEPLAY:
				
				if event.key == py.K_RIGHT:
					released = False
					if Player.x_vel != 0:
						Player.x_vel = 0
					left = False
					Player.state = AnimationState.MOVING
					Player.x_vel += 8

				elif event.key == py.K_LEFT:
					if Player.x_vel != 0:
						Player.x_vel = 0
					left = True
					released = False
					Player.state = AnimationState.MOVING
					Player.x_vel -= 8

				if event.key == py.K_SPACE:
					Player.state = AnimationState.JUMPING
					if Jumped != True:
						Player.y_vel -= 20
						Jumped = True
				if event.key == py.K_e:
					Player.state = AnimationState.ATTACK
					attack = True
															 	
#Release--------------
		elif event.type == py.KEYUP:
					

								
			if ScreenState == ScreenState.GAMEPLAY:
				if event.key == py.K_RIGHT:
					
					if Player.x_vel >= 0:
						released = True
					Player.state = AnimationState.IDLE
				elif event.key == py.K_LEFT:
					if Player.x_vel <= 0:
						released = True
					Player.state = AnimationState.IDLE
				#elif event.key == py.K_DOWN:

					#Player.state = AnimationState.IDLE
					#Player.y_vel = 0

				elif event.key == py.K_SPACE:
					#Player.state = AnimationState.FALLING
					if Player.y_vel < 0:
						Player.y_vel += .5
				if event.key == py.K_e:
					Player.state = AnimationState.IDLE
					attack = False
		elif event.type == py.MOUSEBUTTONDOWN:
			MouseState = MouseState.DOWN
			mouse_loc = py.mouse.get_pos()

		elif event.type == py.MOUSEBUTTONUP:
			MouseState = MouseState.UP
	
						
		
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
#Update Sprites
	
	Player.x_vel , Player.y_vel, bool = constructor.update(Player)
	#print(Player.y_vel)
	if  Player.y_vel != 0:
		GroundState = GroundState.AIR
	if  bool == True:
		GroundState = GroundState.GROUNDED
				
	Player.update()
	
	p_loc = Player.get_location()
	P_hitbox.move(p_loc)
	boxw,boxh = attackBox.get_size()
	Px,Py = p_loc
	if left == False:
		attackRect = py.Rect(Px+45,Py+22,boxw,boxh)
	if left == True:
		attackRect = py.Rect(Px+10,Py+22,boxw,boxh)
	for i in enemy_list:
		if attack ==True:
			if attackRect.colliderect(i.get_rect()):
				ex,ey = i.knockback(5,Player) 
				i.x_vel +=  ex
				i.y_vel +=  ey
	temp = None
	for i in enemy_list:
		
		if temp !=None and i.get_rect().colliderect(temp.get_rect()) :
			ex,ey = i.knockback(2,temp)
			i.x_vel += ex
			i.y_vel += ey
		temp = i

	for i in enemy_list:
		i.new_playerLocation(p_loc)
		i.update(constructor)
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Camera POS:
	#x_value
	screen_width = screen.get_width()
	screen_cords[0] = Player.x - (screen_width/2)
	if  screen_cords[0] < 0: 
		screen_cords[0] = 0
	if screen_cords[0] > world_width - screen_width:
		screen_cords[0] = world_width - screen_width
	#y_value(WIP)
	screen_height= screen.get_height()
	screen_cords[1] = Player.y - (screen_width/2)
	if  screen_cords[1] < 0: 
		screen_cords[1] = 0
	if screen_cords[1] > world_height - screen_height:
		screen_cords[1] = world_height - screen_height 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Pause Menu Buttons
	if MouseState == MouseState.DOWN:
		if ScreenState == ScreenState.PAUSED:		 
			if continue_hitbox.move(260,200).collidepoint(mouse_loc):			
				ScreenState = ScreenState.GAMEPLAY
			elif quit_hitbox.move(260,250).collidepoint(mouse_loc):
				py.quit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Drawing
	if ScreenState == ScreenState.PAUSED:
		pause(True,screen,world)
	elif ScreenState == ScreenState.GAMEPLAY:
		pause(False,screen,world)
		screen_rect = py.Rect(screen_cords[0],screen_cords[1],screen.get_width(),screen.get_height())
		constructor.draw(world)
		Player.draw(world,left)
		for i in enemy_list:
			i.draw(world,i.left)
		#if attack == True:
		#	Px,Py,Pw,Ph = attackRect
		#	world.blit(attackBox,(Px,Py))	
		screen.blit(world,(0,0),screen_rect)
		

		
	

	py.display.update() 
	
	clock.tick(30)  
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#End Loop
py.quit()








