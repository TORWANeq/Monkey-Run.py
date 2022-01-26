# import bibliotek potrzebnych do działania kodu
import pygame
from sys import exit
from random import randint, choice
from pygame import color

# klasa która dziedziczy po sprite(obrazek)
class Player(pygame.sprite.Sprite):
	# Konstruktor klasy
	def __init__(self):
		# tworzenie obiektu rodzica(czyli sprita)
		super().__init__()
		# Ładowanie odrazków i usuwanie alfy (przezroczystość)
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
		# Tworzenie animacji ustawienie postaci grawitacja (konfiguracja startu postaci gry)
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0
		# Podłączanie dźwieku oraz głośności
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)
	# Odczyt klawiszy jakie użytkownik wybiera
	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -25
			self.jump_sound.play()
	# Grawitacja w momencie skoku
	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300
	# Stan czy skoczył czy nie(Osiągniecie kulminacyjnej wyskości skoku)
	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]
	# Odświeżanie co klatke
	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()
# Przeszkody które dziedziczą po klasie obrazek (spircie)
class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		

		# Ptaki
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 170
		# Tygrysy
		else:
			tiger_1 = pygame.image.load('graphics/Tiger/tiger1.png').convert_alpha()
			tiger_2 = pygame.image.load('graphics/Tiger/tiger2.png').convert_alpha()
			self.frames = [tiger_1,tiger_2]
			y_pos  = 300
		# Wielkość oraz pozycja obrazka(ptak, tygrys)
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
	# Poruszanie przesówanie postaci z prawej do lewej
	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]
	# Odświerzanie pozycji (tygrys ptak) przeszkoda
	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()
	# Niszczy pozycje (usuwa z pamięci) jeżeli przeszło poza ekran
	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()
# Wyświetlanie wyniku miejsca gdzie i renderowanie tekstu
def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(255,255,255))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time
# Sprawdza czy przeszkoda znalazła kolizje z postacią (zwraca true or false)
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

# Konfiguracja całej gry (silnik)
pygame.init()
#wielkość ekranu
screen = pygame.display.set_mode((800,400))
# nazwa gry
pygame.display.set_caption('Monkey Run')
# czas odświeżania
clock = pygame.time.Clock()
# Czcionka menu
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# Flagi czy gra jest aktywna (wartości które można modyfikować w kodzie)
game_active = False
start_time = 0
score = 0
# dzwiek oraz zapętlanie go
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

# tworzenie Grupy (uzytkownaika oraz przeszkody)
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
# Stworzenia tła gry (Ziemia, niebo)
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Ekran startowy
player_stand = pygame.image.load('graphics/background_lose.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Monkey',False,(0,0,0))
game_name_rect = game_name.get_rect(center = (400,200))

game_message = test_font.render('Press space to run',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
# Odświeżanie (czy gra jest aktywna) 
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# Dodajesz przeszkody co kazdy tik
		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','tiger','tiger','fly'])))
		# Odczytywanie klawisza czy jest down czy space (wznawia gre bądź przesówa menu)
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	# renderowanie co klatke (ziemie niebo itp.)
	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score()
		# Wynik
		player.draw(screen)
		player.update()
		# Postacie
		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
	#	Sprawdzasz czy jest kolizja
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)
		# Renderowanie menu jeżeli przegrałeś wraz z wynikiem
		score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)
		# Wynik i wyświetlanie go
		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)
	
	pygame.display.update()
	clock.tick(60)