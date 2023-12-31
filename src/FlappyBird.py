# Example file showing a circle moving on screen
import random
import time
import pygame


class PipesPair:
    def __init__(self, surface: pygame.Surface, pipe_up_img:pygame.Surface, pipe_down_img:pygame.Surface, window_rect: pygame.Rect) -> None:
        self.img_up:pygame.Surface = pipe_up_img.copy()
        self.img_down:pygame.Surface = pipe_down_img.copy()
        self.window_rect = window_rect
        self.pos_up:pygame.Vector2 = pygame.Vector2(self.window_rect.width, random.randint(-270, -30))
        self.pos_down:pygame.Vector2 = pygame.Vector2(self.window_rect.width, self.pos_up.y + 100 + self.img_up.get_height())
        self.surface:pygame.Surface = surface
        self.allow_move:bool = True
    
    def recoordinate(self, lastPos:pygame.Vector2):
        y = lastPos.y
        # if self.pos_up.y < lastPos.y  :
        if y - 20 < -270:
            y = -250
        elif y + 20 < -30:
            y = -50
        self.pos_up:pygame.Vector2 = pygame.Vector2(self.window_rect.width, random.randint(y-20, y + 20))         
        self.pos_down:pygame.Vector2 = pygame.Vector2(self.window_rect.width, self.pos_up.y + 100 + self.img_up.get_height())
        
    def show(self, pipe_speed:int, fbg):
        if self.allow_move:
            self.pos_up.x -= pipe_speed
            self.pos_down.x -= pipe_speed
        fbg.showImageOn(self.img_up, self.surface, self.pos_up)
        fbg.showImageOn(self.img_down, self.surface, self.pos_down)
        
class FlappyBirdGame:
    frame_numbers = 0
    gravity_acceleration = 5 
    gravity_velocity = 0
    ground_collision = -15
    frame_rate = 60
    window_rect = pygame.Rect(0,0,1440,512)
    before_start = True
    ground_height = 75
    allow_fly = True
    game_over = False
    game_score = 0
    game_time = 0
    spaceKeyReleased = True
    start_time = time.time()
    screen:pygame.Surface = None
    bird:pygame.Surface = None
    bird_pos = None
    bird_rect:pygame.Rect = None
    showing_pipe_list:list[PipesPair] = []
    
    ground_threashold = -25
    bird_img:pygame.Surface = pygame.image.load('.\\assets\\image\\bluebird-upflap.png')
    ground_img:pygame.Surface = pygame.image.load('.\\assets\\image\\base.png')
    gameOver_img:pygame.Surface = pygame.image.load('.\\assets\\image\\gameover.png')
    background_img:pygame.Surface = pygame.image.load('.\\assets\\image\\background-night.png')
    pipe_up_img:pygame.Surface = pygame.image.load('.\\assets\\image\\pipe-green.png')
    pipe_down_img:pygame.Surface = pygame.image.load('.\\assets\\image\\pipe-green.png')
    bird_size = bird_img.get_size()
    bird_size = pygame.Rect(0,0,min(bird_size),min(bird_size))
    bird = pygame.Surface((bird_size.width, bird_size.height), masks="white")
    bird_pos = bird.get_rect()
    
    screen = pygame.display.set_mode((window_rect.width, window_rect.height))
    ground_surface = pygame.Rect(0, window_rect.height - ground_height ,window_rect.width , 100)
    bird_pos.center:tuple = ( -60 ,  screen.get_height() / 2 )

    bird_pos.center:tuple =  ( -60 ,  screen.get_height() / 2 )
    bird_rect = pygame.draw.circle(screen, "red", bird_pos.center, bird_size.width/2)

    bird_color:str = 'blue'
    bird_images:dict[str, dict[str, str]] = {
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
    
    img_digit_0:pygame.Surface = pygame.image.load('.\\assets\\image\\0.png')
    img_digit_1:pygame.Surface = pygame.image.load('.\\assets\\image\\1.png')
    img_digit_2:pygame.Surface = pygame.image.load('.\\assets\\image\\2.png')
    img_digit_3:pygame.Surface = pygame.image.load('.\\assets\\image\\3.png')
    img_digit_4:pygame.Surface = pygame.image.load('.\\assets\\image\\4.png')
    img_digit_5:pygame.Surface = pygame.image.load('.\\assets\\image\\5.png')
    img_digit_6:pygame.Surface = pygame.image.load('.\\assets\\image\\6.png')
    img_digit_7:pygame.Surface = pygame.image.load('.\\assets\\image\\7.png')
    img_digit_8:pygame.Surface = pygame.image.load('.\\assets\\image\\8.png')
    img_digit_9:pygame.Surface = pygame.image.load('.\\assets\\image\\9.png')
    
    img_digits_list = [img_digit_0, img_digit_1, img_digit_2, img_digit_3,
                       img_digit_4, img_digit_5, img_digit_6, img_digit_7, 
                       img_digit_8, img_digit_9]
    fly_sound = None
    game_over_sound = None
    crach_sound = None
    score_sound = None
    swoosh_sound = None
    
    isFlyingSoundPlayed = False
    isScoreSoundPlayed = False
    isCrashSoundPlayed = False
    isGameOverSoundPlayed = False
    isHitSoundPlayed = False
    gv = 0
    swoosh_sound_counter = 0
    
    
    def __init__(self) -> None:
        
        self.pipe_up_img.convert()
        self.pipe_up_img = pygame.transform.rotate(self.pipe_up_img, 180)
        self.pipe_down_img.convert()

        self.bird_img.convert()
        self.ground_img.convert()
        self.gameOver_img.convert()
        self.background_img.convert()

        self.fly_sound:pygame.mixer.Sound = pygame.mixer.Sound(".\\assets\\audio\\wing.wav")
        
        self.game_over_sound:pygame.mixer.Sound = pygame.mixer.Sound(".\\assets\\audio\\die.wav")
        self.hit_sound:pygame.mixer.Sound = pygame.mixer.Sound(".\\assets\\audio\\hit.wav")
        self.score_sound:pygame.mixer.Sound = pygame.mixer.Sound(".\\assets\\audio\\point.wav") 
        self.swoosh_sound:pygame.mixer.Sound = pygame.mixer.Sound(".\\assets\\audio\\swoosh.wav") 
        self.bird_rect = pygame.draw.circle(self.screen, "red", self.bird_pos.center, self.bird_size.width/2)
    
        self.resetGame()
    
    def showGameScore(self):
        digits:list[pygame.Surface] = []
        score = self.game_score 
        
        while score // 10 > 0:
            digits.insert(0, self.img_digits_list[score % 10])
            score = score // 10
            
        digits.insert(0, self.img_digits_list[score % 10])
        
        for idx, digit in enumerate(digits):
            self.showImageOn(digit, self.screen, pygame.Vector2(idx * 25 + 20, 20))
        
    def resetGame(self):
        self.isGameOverSoundPlayed = False
        self.isFlyingSoundPlayed = False
        self.isScoreSoundPlayed = False
        self.isCrashSoundPlayed = False
        self.isHitSoundPlayed = False
        self.swoosh_sound_counter = 0
        
        self.background_img:pygame.Surface = pygame.image.load('.\\assets\\image\\background-night.png')
        
        self.frame_numbers = 0
        self.gravity_acceleration = 5 
        self.gravity_velocity = 0
        self.ground_collision = -15
        self.frame_rate = 60
        self.window_rect = pygame.Rect(0,0,1440,512)
        self.before_start = True
        self.ground_height = 75
        self.allow_fly = True
        self.game_over = False
        self.game_score = 0
        self.game_time = 0
        self.spaceKeyReleased = True
        self.start_time = time.time()
        self.bird_pos = self.bird.get_rect()
        self.bird_pos.center = ( -60 ,  self.screen.get_height() / 2 )
        self.bird_rect.y =  self.screen.get_height() / 2
        self.showing_pipe_list = []
    def animateFlying(self):
        if not self.before_start:
            if self.allow_fly and not self.game_over :
                diff = self.gv - self.gravity_velocity
                if diff > 0.05:    
                    self.bird_img = pygame.image.load(self.bird_images[self.bird_color]['down'])
                    self.isFlyingSoundPlayed = False
                elif 0.05 >= diff >= -0.05:
                    self.bird_img = pygame.image.load(self.bird_images[self.bird_color]['mid'])
                    self.isFlyingSoundPlayed = False
                        
                elif diff < -0.05:
                    self.bird_img = pygame.image.load(self.bird_images[self.bird_color]['up'])
                    if not self.isFlyingSoundPlayed:
                        self.isFlyingSoundPlayed = True
                        pygame.mixer.Sound.play(self.fly_sound)
        else:
            wings = ['up', 'mid', 'down', 'mid']
            self.bird_img = pygame.image.load(self.bird_images[self.bird_color][wings[self.frame_numbers//10%4]])
            if wings[self.frame_numbers//10%4] == 'down':
                
                if not self.isFlyingSoundPlayed:
                    self.isFlyingSoundPlayed = True
                    pygame.mixer.Sound.play(self.fly_sound)
            else:
                self.isFlyingSoundPlayed = False
        self.gv = self.gravity_velocity      
        self.bird_img.convert()

    def showImageOn(self, img:pygame.Surface, surface:pygame.Surface, pos:pygame.Rect):
        
        surface.blit(img, (pos.x ,pos.y ))
        
    def showText(self, text:str, pos: pygame.Vector2, color:str,
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

    def checkGameState(self):
 
        if self.bird_pos.y >= self.window_rect.height - self.bird_rect.height - self.ground_height + self.ground_threashold:
            self.game_over = True
    
        if self.game_over and not self.isGameOverSoundPlayed:
            self.isGameOverSoundPlayed = True
            pygame.mixer.Sound.play(self.game_over_sound)
        # print('checkGameState')
    def fly(self):
 
        if self.gravity_velocity < -3:
            self.allow_fly = False
            self.isFlyingSoundPlayed = False
            
        if self.gravity_velocity > 0.5 and self.bird_pos.y > 80:
            self.allow_fly = True
        
        if self.allow_fly and not self.game_over and self.bird_pos.y > 80:
            self.gravity_velocity -= 0.2
            
        # print('fly')

    def moveToPos(self, x:int):
 
        if self.bird_pos.x < x:
            self.bird_pos.x += 2
            
        if  self.before_start:
            self.gravity_velocity = 0
    def groundColission(self):
        
        if self.bird_pos.y + self.bird_rect.height / 2 == self.window_rect.height - self.ground_height + self.ground_threashold:
            self.gravity_velocity *= self.ground_collision / self.frame_rate
            self.bird_pos.y += self.gravity_velocity
            if self.swoosh_sound_counter < 3:
                pygame.mixer.Sound.play(self.swoosh_sound)
                self.swoosh_sound_counter += 1
        # print('groundColission')
        
    def pipesColission(self):
 
        if len(self.showing_pipe_list) == 0: return
        pipe:PipesPair = self.showing_pipe_list[0]
        if (pipe.pos_up.x <= self.bird_pos.x+self.bird_pos.width <= pipe.pos_up.x + pipe.img_up.get_width() and
           self.bird_pos.y <= pipe.pos_up.y + pipe.img_up.get_height()) or\
            (pipe.pos_down.x <= self.bird_pos.x <= pipe.pos_down.x + pipe.img_down.get_width() and
            pipe.pos_down.y <= self.bird_pos.y  + self.bird_pos.height ) :
                
            self.gravity_velocity *= self.ground_collision / self.frame_rate
            self.bird_pos.y += self.gravity_velocity
            self.game_over = True
            # print('gameOver')
        # print('groundColission')
        if self.game_over and not self.isHitSoundPlayed:
            self.isHitSoundPlayed = True
            pygame.mixer.Sound.play(self.hit_sound)
            
    def updateGravity(self):
 
        self.gravity_velocity += self.gravity_acceleration / self.frame_rate
        if self.bird_pos.y + self.bird_rect.height/2 < self.window_rect.height - self.ground_height + self.ground_threashold:
            if self.bird_pos.y + self.bird_rect.height/2 + self.gravity_velocity < self.window_rect.height - self.ground_height + self.ground_threashold:
                self.bird_pos.y += self.gravity_velocity
            else:
                self.bird_pos.y = self.window_rect.height-self.bird_rect.height / 2 - self.ground_height + self.ground_threashold
                
        # print('updateGravity')

    