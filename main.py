from src import FlappyBird
import pygame
from src.FlappyBird import *



if __name__ == "__main__":
            
    # pygame setup
    pygame.init()
    fbg:FlappyBirdGame = FlappyBirdGame()
    
    pipe_speed = 2



    

    clock = pygame.time.Clock()
    running = True
    dt = 0
    frame_numbers = 0
    start_time = time.time()
    
    
    fbg.resetGame()
    numerator = 200
    showing_pipe_list:list[PipesPair] = []
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # fill the screen with a color to wipe away anything from last frame
        fbg.screen.fill("black")
        # bird = pygame.draw.circle(screen, "red", bird_pos, 40)
        ground = pygame.draw.rect(fbg.screen, "white", fbg.ground_surface)
        bird_rect = pygame.draw.circle(fbg.screen, "red", fbg.bird_pos.center, fbg.bird_size.width/2)
        
        fbg.showImageOn(fbg.background_img, fbg.screen, pygame.Vector2(0,0))    
        if len(fbg.showing_pipe_list) > 0:
            pipe:PipesPair = fbg.showing_pipe_list[0]
            if fbg.bird_pos.x >= pipe.pos_up.x+pipe.img_up.get_width() and not fbg.isScoreSoundPlayed:
                fbg.game_score += 1
                # if not fbg.score_sound:
                fbg.isScoreSoundPlayed = True
                pygame.mixer.Sound.play(fbg.score_sound)
                
        pipe_speed = 2 + (fbg.game_score / 10)    
        numerator = 120 - (fbg.game_score)

        if pipe_speed > 5:
            pipe_speed = 5                                         
        if numerator < 100:
            numerator = 100

        if fbg.frame_numbers % numerator == 0 and not fbg.game_over:
            if fbg.before_start and len(fbg.showing_pipe_list) < 2:
                pipe_pair = PipesPair(fbg.screen, fbg.pipe_up_img, fbg.pipe_down_img, fbg.window_rect)
                fbg.showing_pipe_list.append(pipe_pair)
                if len(fbg.showing_pipe_list) > 0:
                    pipe_pair.recoordinate(fbg.showing_pipe_list[0].pos_up)
                
            elif fbg.before_start and len(fbg.showing_pipe_list) == 2:
                for pipe in fbg.showing_pipe_list:
                    pipe.allow_move = False
                
            elif not fbg.before_start:
                for pipe in fbg.showing_pipe_list:
                    pipe.allow_move = True
                pipe_pair = PipesPair(fbg.screen, fbg.pipe_up_img, fbg.pipe_down_img, fbg.window_rect)
                fbg.showing_pipe_list.append(pipe_pair)
             
        if len(fbg.showing_pipe_list) > 0 and fbg.showing_pipe_list[0].pos_up.x + fbg.showing_pipe_list[0].img_up.get_width() < 0:
            fbg.showing_pipe_list.pop(0)
            fbg.isScoreSoundPlayed = False
                
                
        
        
        for pipe in fbg.showing_pipe_list:
            if fbg.game_over:        
                pipe.allow_move = False
            pipe.show(pipe_speed, fbg)
        
        # showImageOn(pipe_up_img, screen, pygame.Vector2(850-frame_numbers, -270))
        # showImageOn(pipe_down_img, screen, pygame.Vector2(850-frame_numbers, window_rect.height-ground_height - 50))
        fbg.showImageOn(fbg.ground_img, fbg.screen, fbg.ground_surface)    
        fbg.showImageOn(fbg.bird_img, fbg.screen, fbg.bird_pos)   
        
        fbg.updateGravity()
        fbg.groundColission()
        fbg.checkGameState()
        fbg.animateFlying()
        
        
        
        # print(f'\r{allow_fly=}, {gravity_velocity=}', end='')
        # print(f'\r{bird_pos=}, {bird_rect=}, {gravity_velocity=} {before_start=} ', end='')
        # print(f'\r{frame_numbers=}', end='')
        if fbg.before_start:
            fbg.moveToPos(fbg.screen.get_width() / 10)
        elif fbg.game_over:
            fbg.moveToPos(fbg.screen.get_width() / 2.5)
            
        if fbg.game_over:
            pygame.draw.rect(fbg.background_img, pygame.Color(0,0,0, 120), 
                             pygame.Rect(fbg.window_rect.width/2-200, 
                                         fbg.window_rect.height/2-60, 
                                         400, 150))
            
            if frame_numbers  % 60 < 30 :
                fbg.showText("Press Enter/Return to Play Again.", 
                        pygame.Vector2(fbg.window_rect.width/2-1, fbg.window_rect.height/2+48),
                        "black", display_surface=fbg.screen, fontSize=20)
                fbg.showText("Press Enter/Return to Play Again.", 
                        pygame.Vector2(fbg.window_rect.width/2, fbg.window_rect.height/2+50),
                        "white", display_surface=fbg.screen, fontSize=20)
            fbg.showImageOn(fbg.gameOver_img, fbg.screen, pygame.Vector2(fbg.screen.get_width()/2-fbg.gameOver_img.get_width()/2,
                                                            fbg.screen.get_height()/2-fbg.gameOver_img.get_height()/2))
            
        # if time.time() - start_time > 5:
        keys = pygame.key.get_pressed()
    
        if fbg.before_start:
            if fbg.frame_numbers  % 60 < 30 :
                fbg.showText("Press SPACE to Start.", 
                        pygame.Vector2(fbg.window_rect.width/2-1, fbg.window_rect.height/2),
                        "black", display_surface=fbg.screen, fontSize=35)
                fbg.showText("Press SPACE to Start.", 
                        pygame.Vector2(fbg.window_rect.width/2, fbg.window_rect.height/2),
                        "white", display_surface=fbg.screen, fontSize=35)
                
            if keys[pygame.K_SPACE] and fbg.frame_numbers > 180:
                fbg.before_start = False
                fbg.frame_numbers = 151
                
                # print(True)
                for pipe in fbg.showing_pipe_list:
                    if fbg.game_over:        
                        pipe.allow_move = False
                    else:
                        pipe.allow_move = True
                        
                    pipe.show(pipe_speed, fbg)
        
        fbg.frame_numbers += 1
        
        fbg.spaceKeyReleased = not keys[pygame.K_SPACE]
        
        if keys[pygame.K_SPACE] and fbg.frame_numbers > 180:
            fbg.fly()
            spaceKeyReleased = False
        if (keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]):
            if fbg.game_over:
                fbg.resetGame()
        fbg.pipesColission()
        
        fbg.showGameScore()
        
        
        # fbg.showImageOn()
        # pygame.Rect(0, window_rect.height - ground_height ,window_rect.width , 100)
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
    pass