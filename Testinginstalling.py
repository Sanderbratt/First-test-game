import pygame
from sys import exit
from random import randint, choice

from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/p1_walk/PNG/p1_walk04.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/p1_walk/PNG/p1_walk05.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/p1_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,735))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 735:
            self.gravity = -20 

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 735: self.rect.bottom = 735

    def animation_state(self):
        if self.rect.bottom < 735:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def laser(self):
        if any(pygame.mouse.get_pressed()):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.line(screen,'Red',self.rect.midright,pygame.mouse.get_pos(),10)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.laser()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Enemies/flyFly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Enemies/flyFly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 600
        else:
            snail_1 = pygame.image.load('graphics/Enemies/snailWalk1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/Enemies/snailWalk2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 730

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1500,1700), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        # if type == 'fly':
        #     self.animation_index += 0.1
        #     if self.animation_index >= len(fly_frames): self.animation_index = 0
        #     self.image = self.frames[int(self.animation_index)]
        # else:
        #     self.animation_index += 0.1
        #     if self.animation_index >= len(snail_frames): self.animation_index = 0
        #     self.image = snail_frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()



def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time 
    score_surf = test_font.render(f'{current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (700,100))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6

            if obstacle_rect.bottom == 730: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


def player_animations():
    global player_surf, player_index

    if player_rectangle.bottom < 735:
        player_surf = player_jump
    else: 
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((1400,800))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() 
test_font = pygame.font.Font('font/ThaleahFat.ttf',100)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

ground_surface = pygame.image.load('graphics/Tiles/grassMid.png').convert()
sky_surface = pygame.image.load('graphics/fajrbackground.png').convert()

game_over_bg = pygame.image.load('graphics/noonbackground.png').convert()

# Snail
snail_frame_1 = pygame.image.load('graphics/Enemies/snailWalk1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/Enemies/snailWalk2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/Enemies/flyFly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Enemies/flyFly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[snail_frame_index]

obstacle_rect_list = []


# Player 
player_walk_1 = pygame.image.load('graphics/Player/p1_walk/PNG/p1_walk04.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/p1_walk/PNG/p1_walk05.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/p1_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rectangle = player_walk_1.get_rect(midbottom = (200,735))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/p1_front.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
# player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (700,400))

start_game_screen = test_font.render('Laser Man',False,'Black')
start_game_screen_rect = start_game_screen.get_rect(center = (700,100))

start_instructions = test_font.render('Press Space To Start',False,'Black')
start_instructions_rect = start_instructions.get_rect(center = (700,700))

player_lose = pygame.image.load('graphics/Player/p1_hurt.png').convert_alpha()
player_lose = pygame.transform.scale2x(player_lose)
player_lose_rect = player_lose.get_rect(center = (700,400))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400) 

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

positions_ground = []
x = 0
while x <= 1400:
    positions_ground.append((x,730))
    x += 70

positions_sky = []
x = 0
while x <= 1400:
    positions_sky.append((x,0))
    x += 1000

pos_sky_lose_screen = []
x = 0
while x <= 1400:
    pos_sky_lose_screen.append((x,0))
    x += 1000

player_laser = Player()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
       
        if game_active == True:
            if player_rectangle.bottom >= 735:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rectangle.collidepoint(event.pos): 
                        player_gravity = -20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        else: 
    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint (1500,1700), 730)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(1500,1700), 600)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        for pos in positions_sky:
            screen.blit(sky_surface, pos)


        for pos in positions_ground:
            screen.blit(ground_surface, pos)

        # Title
        score = display_score()

        # Snail
        # snail_rectangle.left -= 6
        # if snail_rectangle.right <= 0: snail_rectangle.left = 1400
        # screen.blit(snail_surface, snail_rectangle)

        # Fly

        # Player      
        # player_gravity += 1
        # player_rectangle.bottom += player_gravity
        # if player_rectangle.bottom >= 735: player_rectangle.bottom = 735
        # player_animations()
        # screen.blit(player_surf, player_rectangle)
        player.draw(screen)
        player.update()

        # Obstacle
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()
        # game_active = collisions(player_rectangle,obstacle_rect_list)

        # if any(pygame.mouse.get_pressed()):
        #     if pygame.mouse.get_pressed()[0]:
        #         pygame.draw.line(screen,'Red',player_laser.rect,pygame.mouse.get_pos(),10)
    else:
        screen.fill('#f5f3cf')
        for pos in pos_sky_lose_screen:
            screen.blit(game_over_bg, pos)

        obstacle_rect_list.clear()
        player_rectangle.midbottom = (200,735)
        player_gravity = 0

        score_message = test_font.render(f'Your Score: {score}',False,'Black')
        score_message_rect = score_message.get_rect(center = (700,700))
        screen.blit(start_game_screen,start_game_screen_rect)

        if score == 0:
            screen.blit(start_instructions,start_instructions_rect)
            screen.blit(player_stand, player_stand_rect)

        else:
            screen.blit(score_message,score_message_rect)    
            screen.blit(player_lose,player_lose_rect)

    pygame.display.update()
    clock.tick(60)


