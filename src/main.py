import pygame
from sys import exit
from random import randint, choice

class Farah(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		farah_walk_1 = pygame.image.load('graphics/farah/farah_walk_1.png').convert_alpha()
		farah_walk_2 = pygame.image.load('graphics/farah/farah_walk_2.png').convert_alpha()
		self.farah_walk = [farah_walk_1,farah_walk_2]
		self.farah_index = 0
		self.farah_jump = pygame.image.load('graphics/farah/jump.png').convert_alpha()

		# Kneeling image (optional separate sprite). If it doesn't exist yet, fall back to a standing frame.
		try:
			self.farah_kneel = pygame.image.load('graphics/farah/farah_kneel.png').convert_alpha()
		except Exception:
			self.farah_kneel = self.farah_walk[0]

		# State flag for kneeling
		self.is_kneeling = False

		self.image = self.farah_walk[self.farah_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def farah_input(self):
		keys = pygame.key.get_pressed()
		# Reset kneeling every frame, then re-set if key is held
		self.is_kneeling = False

		# Kneel while DOWN is held and Farah is on the ground
		if keys[pygame.K_DOWN] and self.rect.bottom >= 300:
			self.is_kneeling = True
			self.gravity = 0  # prevent accidental tiny jumps while kneeling

		# Jump only if not kneeling (space or up arrow)
		elif (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 0.95
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			# When kneeling, position Farah lower (closer to ground)
			if self.is_kneeling:
				self.rect.bottom = 320  # Adjust this value to control how low she kneels
			else:
				self.rect.bottom = 300

	def animation_state(self):
		# In the air → jumping sprite
		if self.rect.bottom < 300: 
			self.image = self.farah_jump
		# On ground and kneeling → kneel sprite
		elif self.is_kneeling:
			self.image = self.farah_kneel
		# On ground and not kneeling → walking animation
		else:
			self.farah_index += 0.1
			if self.farah_index >= len(self.farah_walk):self.farah_index = 0
			self.image = self.farah_walk[int(self.farah_index)]

	def update(self):
		self.farah_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 250
		if type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300
		if type == 'libro':
			libro_1=pygame.image.load('graphics/libro/libro.png').convert_alpha()
			libro_2=pygame.image.load('graphics/libro/libro.png').convert_alpha()
			self.frames = [libro_1,libro_2]
			y_pos = 301

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
		
		# Create a smaller collision rectangle (hitbox) - adjust padding to make it smaller
		# This makes collision detection more forgiving without changing visual appearance
		hitbox_padding = 10  # Pixels to shrink from each side
		self.hitbox = self.rect.inflate(-hitbox_padding * 2, -hitbox_padding * 2)

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		if score<150:
			self.rect.x -= 7
		else:
			self.rect.x -= 8
		
		# Update hitbox position to match rect position
		hitbox_padding = 10
		self.hitbox = self.rect.inflate(-hitbox_padding * 2, -hitbox_padding * 2)

		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 100) - start_time
	score_surf = test_font.render(f'Puntaje: {current_time}',False,("White"),("Black"))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 10

			if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
			if obstacle_rect.bottom == 250: screen.blit(fly_surf,obstacle_rect)
			if obstacle_rect.bottom == 301: screen.blit(libro_surf,obstacle_rect)

			

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(farah,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if farah.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	# Use custom collision detection with hitboxes instead of default rects
	farah_rect = farah.sprite.rect
	for obstacle in obstacle_group:
		if farah_rect.colliderect(obstacle.hitbox):
			obstacle_group.empty()
			return False
	return True

def farah_animation():
	global farah_surf, farah_index

	if farah_rect.bottom < 300:
		farah_surf = farah_jump
	else:
		farah_index += 0.1
		if farah_index >= len(farah_walk):farah_index = 0
		farah_surf = farah_walk[int(farah_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Farah Adventures')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/VALEDATION.mp3')
bg_music.play(loops = -1)

#Groups
farah = pygame.sprite.GroupSingle()
farah.add(Farah())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()


# Snail 
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
 
#libro
libro_frame1 = pygame.image.load('graphics/libro/libro.png').convert_alpha()
libro_frame2= pygame.image.load('graphics/libro/libro.png').convert_alpha()
libro_frames = [libro_frame1, libro_frame2]
libro_frame_index = 0
libro_surf = libro_frames[libro_frame_index]

obstacle_rect_list = []


farah_walk_1 = pygame.image.load('graphics/farah/farah_walk_1.png').convert_alpha()
farah_walk_2 = pygame.image.load('graphics/farah/farah_walk_2.png').convert_alpha()
farah_walk = [farah_walk_1,farah_walk_2]
farah_index = 0
farah_jump = pygame.image.load('graphics/farah/jump.png').convert_alpha()

farah_surf = farah_walk[farah_index]
farah_rect = farah_surf.get_rect(midbottom = (80,300))
farah_gravity = 0

# Intro screen
farah_stand = pygame.image.load('graphics/farah/farah_stand.png').convert_alpha()
farah_stand = pygame.transform.rotozoom(farah_stand,0,2)
farah_stand_rect = farah_stand.get_rect(center = (400,200))

game_name = test_font.render('Farah Adventures',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Presiona espacio para iniciar',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

libro_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(libro_animation_timer,100)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if farah_rect.collidepoint(event.pos) and farah_rect.bottom >= 300: 
					farah_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and farah_rect.bottom >= 300:
					farah_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 100)

		if game_active:
			if event.type == obstacle_timer: 
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','libro'])))
			

			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frames[snail_frame_index] 

			if event.type == fly_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frames[fly_frame_index]

			if event.type == libro_animation_timer:
				if libro_frame_index == 0: libro_frame_index = 1
				else: libro_frame_index = 0
				libro_surf = libro_frames[libro_frame_index] 



	if game_active:
		screen.blit(sky_surface,(0,0))

		score = display_score()
		

		farah.draw(screen)
		farah.update()

		obstacle_group.draw(screen)
		obstacle_group.update()



		# collision 
		game_active = collision_sprite()
		
	else:
		screen.fill((255,209,220))
		screen.blit(farah_stand,farah_stand_rect)
		obstacle_rect_list.clear()
		farah_rect.midbottom = (80,300)
		farah_gravity = 0

		score_message = test_font.render(f'GAME OVER  Tu puntaje: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)

import pygame
from sys import exit
from random import randint, choice

class Farah(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		farah_walk_1 = pygame.image.load('graphics/farah/farah_walk_1.png').convert_alpha()
		farah_walk_2 = pygame.image.load('graphics/farah/farah_walk_2.png').convert_alpha()
		self.farah_walk = [farah_walk_1,farah_walk_2]
		self.farah_index = 0
		self.farah_jump = pygame.image.load('graphics/farah/jump.png').convert_alpha()

		# Kneeling image (optional separate sprite). If it doesn't exist yet, fall back to a standing frame.
		try:
			self.farah_kneel = pygame.image.load('graphics/farah/farah_kneel.png').convert_alpha()
		except Exception:
			self.farah_kneel = self.farah_walk[0]

		# State flag for kneeling
		self.is_kneeling = False

		self.image = self.farah_walk[self.farah_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def farah_input(self):
		keys = pygame.key.get_pressed()
		# Reset kneeling every frame, then re-set if key is held
		self.is_kneeling = False

		# Kneel while DOWN is held and Farah is on the ground
		if keys[pygame.K_DOWN] and self.rect.bottom >= 300:
			self.is_kneeling = True
			self.gravity = 0  # prevent accidental tiny jumps while kneeling

		# Jump only if not kneeling (space or up arrow)
		elif (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 0.95
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			# When kneeling, position Farah lower (closer to ground)
			if self.is_kneeling:
				self.rect.bottom = 320  # Adjust this value to control how low she kneels
			else:
				self.rect.bottom = 300

	def animation_state(self):
		# In the air → jumping sprite
		if self.rect.bottom < 300: 
			self.image = self.farah_jump
		# On ground and kneeling → kneel sprite
		elif self.is_kneeling:
			self.image = self.farah_kneel
		# On ground and not kneeling → walking animation
		else:
			self.farah_index += 0.1
			if self.farah_index >= len(self.farah_walk):self.farah_index = 0
			self.image = self.farah_walk[int(self.farah_index)]

	def update(self):
		self.farah_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 250
		if type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300
		if type == 'libro':
			libro_1=pygame.image.load('graphics/libro/libro.png').convert_alpha()
			libro_2=pygame.image.load('graphics/libro/libro.png').convert_alpha()
			self.frames = [libro_1,libro_2]
			y_pos = 301

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
		
		# Create a smaller collision rectangle (hitbox) - adjust padding to make it smaller
		# This makes collision detection more forgiving without changing visual appearance
		hitbox_padding = 10  # Pixels to shrink from each side
		self.hitbox = self.rect.inflate(-hitbox_padding * 2, -hitbox_padding * 2)

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		if score<150:
			self.rect.x -= 7
		else:
			self.rect.x -= 8
		
		# Update hitbox position to match rect position
		hitbox_padding = 10
		self.hitbox = self.rect.inflate(-hitbox_padding * 2, -hitbox_padding * 2)

		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 100) - start_time
	score_surf = test_font.render(f'Puntaje: {current_time}',False,("White"),("Black"))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 10

			if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
			if obstacle_rect.bottom == 250: screen.blit(fly_surf,obstacle_rect)
			if obstacle_rect.bottom == 301: screen.blit(libro_surf,obstacle_rect)

			

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(farah,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if farah.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	# Use custom collision detection with hitboxes instead of default rects
	farah_rect = farah.sprite.rect
	for obstacle in obstacle_group:
		if farah_rect.colliderect(obstacle.hitbox):
			obstacle_group.empty()
			return False
	return True

def farah_animation():
	global farah_surf, farah_index

	if farah_rect.bottom < 300:
		farah_surf = farah_jump
	else:
		farah_index += 0.1
		if farah_index >= len(farah_walk):farah_index = 0
		farah_surf = farah_walk[int(farah_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Farah Adventures')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/VALEDATION.mp3')
bg_music.play(loops = -1)

#Groups
farah = pygame.sprite.GroupSingle()
farah.add(Farah())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()


# Snail 
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
 
#libro
libro_frame1 = pygame.image.load('graphics/libro/libro.png').convert_alpha()
libro_frame2= pygame.image.load('graphics/libro/libro.png').convert_alpha()
libro_frames = [libro_frame1, libro_frame2]
libro_frame_index = 0
libro_surf = libro_frames[libro_frame_index]

obstacle_rect_list = []


farah_walk_1 = pygame.image.load('graphics/farah/farah_walk_1.png').convert_alpha()
farah_walk_2 = pygame.image.load('graphics/farah/farah_walk_2.png').convert_alpha()
farah_walk = [farah_walk_1,farah_walk_2]
farah_index = 0
farah_jump = pygame.image.load('graphics/farah/jump.png').convert_alpha()

farah_surf = farah_walk[farah_index]
farah_rect = farah_surf.get_rect(midbottom = (80,300))
farah_gravity = 0

# Intro screen
farah_stand = pygame.image.load('graphics/farah/farah_stand.png').convert_alpha()
farah_stand = pygame.transform.rotozoom(farah_stand,0,2)
farah_stand_rect = farah_stand.get_rect(center = (400,200))

game_name = test_font.render('Farah Adventures',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Presiona espacio para iniciar',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

libro_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(libro_animation_timer,100)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if farah_rect.collidepoint(event.pos) and farah_rect.bottom >= 300: 
					farah_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and farah_rect.bottom >= 300:
					farah_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 100)

		if game_active:
			if event.type == obstacle_timer: 
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','libro'])))
			

			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frames[snail_frame_index] 

			if event.type == fly_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frames[fly_frame_index]

			if event.type == libro_animation_timer:
				if libro_frame_index == 0: libro_frame_index = 1
				else: libro_frame_index = 0
				libro_surf = libro_frames[libro_frame_index] 



	if game_active:
		screen.blit(sky_surface,(0,0))

		score = display_score()
		

		farah.draw(screen)
		farah.update()

		obstacle_group.draw(screen)
		obstacle_group.update()



		# collision 
		game_active = collision_sprite()
		
	else:
		screen.fill((255,209,220))
		screen.blit(farah_stand,farah_stand_rect)
		obstacle_rect_list.clear()
		farah_rect.midbottom = (80,300)
		farah_gravity = 0

		score_message = test_font.render(f'GAME OVER  Tu puntaje: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
