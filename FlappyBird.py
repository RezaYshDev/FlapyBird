# Example file showing a circle moving on screen
import random
import time
import pygame

gravity_acceleration = 5 
gravity_velocity = 0
ground_collision = -15
frame_rate = 60
window_rect = pygame.Rect(0,0,1440,512)
before_start = True
ground_height = 75
ground_threashold = 25
allow_fly = True
game_over = False
game_score = 0
game_time = 0
spaceKeyReleased = True
bird_color = 'blue'
bird_images = {
    'blue':{
        'down':'.\\assets\\image\\bluebird-downflap.png',
        'mid':'.\\assets\\image\\bluebird-midflap.png',
        'up':'.\\assets\\image\\bluebird-upflap.png'
        },
    'red':{
        'down':'.\\assets\\image\\redbird-downflap.png',
        'mid':'.\\assets\\image\\redbird-midflap.png',
        'up':'.\\assets\\image\\redbird-upflap.png'
        },
    'yellow':{
        'down':'.\\assets\\image\\yellowbird-downflap.png',
        'mid':'.\\assets\\image\\yellowbird-midflap.png',
        'up':'.\\assets\\image\\yellowbird-upflap.png'
        }
    }

pipe_speed = 2


class PipesPair:
    def __init__(self, surface: pygame.Surface) -> None:
        self.img_up = pipe_up_img.copy()
        self.img_down = pipe_down_img.copy()
        self.pos_up = pygame.Vector2(window_rect.width, random.randint(-270, -30))
        self.pos_down = pygame.Vector2(window_rect.width, self.pos_up.y + 100 + self.img_up.get_height())
        self.surface = surface
        self.allow_move = True
        
    def show(self):
        if self.allow_move:
            self.pos_up.x -= pipe_speed
            self.pos_down.x -= pipe_speed
        showImageOn(self.img_up, self.surface, self.pos_up)
        showImageOn(self.img_down, self.surface, self.pos_down)
        
def resetGame():
    global gravity_acceleration
    global gravity_velocity
    global ground_collision
    global frame_rate
    global window_rect
    global before_start
    global ground_height
    global allow_fly
    global game_over
    global game_score
    global game_time
    global spaceKeyReleased
    global bird_pos
    global bird_rect
    global frame_numbers
    global start_time
    global showing_pipe_list
    
    frame_numbers = 0
    gravity_acceleration = 5 
    gravity_velocity = 0
    ground_collision = -15
    frame_rate = 30
    window_rect = pygame.Rect(0,0,1440,512)
    before_start = True
    ground_height = 75
    allow_fly = True
    game_over = False
    game_score = 0
    game_time = 0
    spaceKeyReleased = True
    start_time = time.time()
    
    bird_pos = bird.get_rect()
    bird_pos.center = ( -60 ,  screen.get_height() / 2 )
    bird_rect.y =  screen.get_height() / 2
    showing_pipe_list = []
def animateFlying():
    global gravity_velocity
    global allow_fly
    global bird_img
    global before_start
    global frame_numbers
    global bird_color
    
    if not before_start:
        if allow_fly :
            bird_img = pygame.image.load(bird_images[bird_color]['down'])
        elif 2 >= gravity_velocity >= -2:
            bird_img = pygame.image.load(bird_images[bird_color]['mid'])
        elif gravity_velocity > 2:
            bird_img = pygame.image.load(bird_images[bird_color]['up'])
    else:
        wings = ['up', 'mid', 'down', 'mid']
        bird_img = pygame.image.load(bird_images[bird_color][wings[frame_numbers//10%4]])
    bird_img.convert()

def showImageOn(img:pygame.image, surface:pygame.Surface, pos:pygame.Rect):
    
    surface.blit(img, (pos.x ,pos.y ))
    
def showText(text:str, pos: pygame.Vector2, color:str,
             display_surface:pygame.surface.Surface,
             fontSize:int=10, font:str=None, center=True):
    if font is None:
        font = '.\\assets\\font\\arial.ttf'
    fnt = pygame.font.Font(font, fontSize)
    txt = fnt.render(f'{text}', True, color)
    txtRect = txt.get_rect()
    
    txtRect.x = pos.x - txtRect.width/2 if center else 0
    txtRect.y = pos.y - txtRect.height/2 if center else 0
    
    display_surface.blit(txt, txtRect)


def checkGameState(pos: pygame.Vector2):
    global game_over
    global bird_rect
    global window_rect
    global ground_height
    global ground_threashold
    if pos.y >= window_rect.height - bird_rect.height - ground_height + ground_threashold:
        game_over = True
    # print('checkGameState')
    
def fly(pos: pygame.Vector2):
    global gravity_velocity
    global allow_fly
    global game_over
    global spaceKeyReleased
    if gravity_velocity < -3:
        allow_fly = False
        
    if gravity_velocity > 1 and pos.y > bird_rect.height*2:
        allow_fly = True
    
    if allow_fly and not game_over:
        gravity_velocity -= 1
        
    # print('fly')

def moveToPos(pos:pygame.Vector2, x:int):
    global gravity_velocity
    global before_start
    # print('moveToPos')
    if pos.x < x:
        pos.x += 2
        
    if  before_start:
        gravity_velocity = 0
def groundColission(obj:pygame.Rect, pos:pygame.Vector2):
    global gravity_acceleration
    global gravity_velocity
    global ground_collision
    global frame_rate
    global window_rect
    global ground_threashold
    if pos.y + obj.height / 2 == window_rect.height - ground_height + ground_threashold:
        gravity_velocity *= ground_collision / frame_rate
        pos.y += gravity_velocity
    # print('groundColission')
def pipesColission(obj:pygame.Rect, pos:pygame.Vector2):
    global gravity_acceleration
    global gravity_velocity
    global ground_collision
    global frame_rate
    global window_rect
    global ground_threashold
    global showing_pipe_list
    global game_over
    if len(showing_pipe_list) == 0: return
    pipe = showing_pipe_list[0]
   
    if (pipe.pos_up.x <= pos.x <= pipe.pos_up.x + pipe.img_up.get_width() and
        pipe.pos_up.y <= pos.y <= pipe.pos_up.y + pipe.img_up.get_height()) or\
        (pipe.pos_down.x <= pos.x <= pipe.pos_down.x + pipe.img_up.get_width() and
        pipe.pos_down.y <= pos.y <= pipe.pos_down.y + pipe.img_up.get_height()) :
            
        gravity_velocity *= ground_collision / frame_rate
        pos.y += gravity_velocity
        game_over = True
        # print('gameOver')
    # print('groundColission')
        
def updateGravity(obj:pygame.Rect, pos:pygame.Vector2):
    global gravity_velocity
    global gravity_acceleration
    global frame_rate
    global window_rect
    global ground_height
    global ground_threashold
    gravity_velocity += gravity_acceleration / frame_rate
    if pos.y + obj.height/2 < window_rect.height - ground_height + ground_threashold:
        if pos.y + obj.height/2 + gravity_velocity < window_rect.height - ground_height + ground_threashold:
            pos.y += gravity_velocity
        else:
            pos.y = window_rect.height-obj.height / 2 - ground_height + ground_threashold
            
    # print('updateGravity')
     
# pygame setup
pygame.init()
screen = pygame.display.set_mode((window_rect.width, window_rect.height))
ground_surface = pygame.Rect(0, window_rect.height - ground_height ,window_rect.width , 100)


clock = pygame.time.Clock()
running = True
dt = 0
frame_numbers = 0
start_time = time.time()
bird_img = pygame.image.load('.\\assets\\image\\bluebird-upflap.png')
ground_img = pygame.image.load('.\\assets\\image\\base.png')
gameOver_img = pygame.image.load('.\\assets\\image\\gameover.png')
background_img = pygame.image.load('.\\assets\\image\\background-night.png')
pipe_up_img = pygame.image.load('.\\assets\\image\\pipe-green.png')
pipe_down_img = pygame.image.load('.\\assets\\image\\pipe-green.png')

pipe_up_img.convert()
pipe_up_img = pygame.transform.rotate(pipe_up_img, 180)
pipe_down_img.convert()

bird_img.convert()
ground_img.convert()
gameOver_img.convert()
background_img.convert()
bird_size = bird_img.get_size()
bird_size = pygame.Rect(0,0,min(bird_size),min(bird_size))
bird = pygame.Surface((bird_size.width, bird_size.height), masks="white")
bird_pos = bird.get_rect()
bird_pos.center = ( -60 ,  screen.get_height() / 2 )
bird_rect = pygame.draw.circle(screen, "red", bird_pos.center, bird_size.width/2)
resetGame()

showing_pipe_list:list[PipesPair] = []
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # bird = pygame.draw.circle(screen, "red", bird_pos, 40)
    ground = pygame.draw.rect(screen, "white", ground_surface)
    bird_rect = pygame.draw.circle(screen, "red", bird_pos.center, bird_size.width/2)
    
    showImageOn(background_img, screen, pygame.Vector2(0,0))    
 
    if frame_numbers % 180 == 0 and not game_over:
        if before_start and len(showing_pipe_list) < 2:
            pipe_pair = PipesPair(screen)
            showing_pipe_list.append(pipe_pair)
            
        elif before_start and len(showing_pipe_list) == 2:
           for pipe in showing_pipe_list:
               pipe.allow_move = False
               
        elif not before_start:
            for pipe in showing_pipe_list:
                pipe.allow_move = True
            pipe_pair = PipesPair(screen)
            showing_pipe_list.append(pipe_pair)
        if len(showing_pipe_list) > 4:
            showing_pipe_list.pop(0)
            
    for pipe in showing_pipe_list:
        if game_over:        
            pipe.allow_move = False
        pipe.show()
    
    # showImageOn(pipe_up_img, screen, pygame.Vector2(850-frame_numbers, -270))
    # showImageOn(pipe_down_img, screen, pygame.Vector2(850-frame_numbers, window_rect.height-ground_height - 50))
    showImageOn(ground_img, screen, ground_surface)    
    showImageOn(bird_img, screen, bird_pos)   
    
    updateGravity(bird_rect, bird_pos)
    groundColission(bird_rect, bird_pos)
    checkGameState(bird_pos)
    animateFlying()
    
    
    
    # print(f'\r{allow_fly=}, {gravity_velocity=}', end='')
    # print(f'\r{bird_pos=}, {bird_rect=}, {gravity_velocity=} {before_start=} ', end='')
    # print(f'\r{frame_numbers=}', end='')
    if before_start:
        moveToPos(bird_pos, screen.get_width() / 10)
    elif game_over:
        moveToPos(bird_pos, screen.get_width() / 2.5)
        
    if game_over:
        if frame_numbers  % 60 < 30 :
            showText("Press Enter/Return to Play Again.", 
                    pygame.Vector2(window_rect.width/2-1, window_rect.height/2+48),
                    "black", display_surface=screen, fontSize=20)
            showText("Press Enter/Return to Play Again.", 
                    pygame.Vector2(window_rect.width/2, window_rect.height/2+50),
                    "white", display_surface=screen, fontSize=20)
        showImageOn(gameOver_img, screen, pygame.Vector2(screen.get_width()/2-gameOver_img.get_width()/2,
                                                         screen.get_height()/2-gameOver_img.get_height()/2))
        
    # if time.time() - start_time > 5:
    keys = pygame.key.get_pressed()
   
    if before_start:
        if frame_numbers  % 60 < 30 :
            showText("Press SPACE to Start.", 
                    pygame.Vector2(window_rect.width/2-1, window_rect.height/2),
                    "black", display_surface=screen, fontSize=35)
            showText("Press SPACE to Start.", 
                    pygame.Vector2(window_rect.width/2, window_rect.height/2),
                    "white", display_surface=screen, fontSize=35)
            
        if keys[pygame.K_SPACE] and frame_numbers > 180:
            before_start = False
            # print(True)
            for pipe in showing_pipe_list:
                if game_over:        
                    pipe.allow_move = False
                else:
                    pipe.allow_move = True
                    
                pipe.show()
    
    # if before_start and frame_numbers % 60 == 0:
    #     fly(bird_pos)
        # fly(bird_pos)
        # fly(bird_pos)
        # fly(bird_pos)
    frame_numbers += 1
    
    spaceKeyReleased = not keys[pygame.K_SPACE]
    
    if keys[pygame.K_SPACE] and frame_numbers > 150:
        fly(bird_pos)
        spaceKeyReleased = False
    if (keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]):
        if game_over:
            resetGame()
    pipesColission(bird_rect, bird_pos)
    
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()