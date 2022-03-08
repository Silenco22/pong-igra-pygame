import pygame
from paddle import Paddle
from ball import Ball
from game import Game
#always initialize pygame first
pygame.init()

#1st draw windov with width, height
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# displays window with the name Pong
pygame.display.set_caption("Pong")

FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

WHITE = (255,255,255)
BLACK = (0,0,0)

#font for drawing scores
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

#winning
WINNING_SCORE = 4

game = Game()

def main():
    run = True
    clock = pygame.time.Clock() #sets fps for every pc its gonna run the same speed on every pc
    
    #setting where the left  and right paddle gonna be draw
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball(WIDTH//2, HEIGHT//2)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS) #wont run faster than 60 fps on every pc
        #passing every elemet to the drawing function
        game.draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        #loopin through all the events taht occur like hiting keyboard etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exiting the game
                run =False
                break
        
        #getting pressed keys
        keys = pygame.key.get_pressed()
        #handling movemnet with aonther func to avoid clustering our mani func
        game.handle_paddle_movement(keys, left_paddle, right_paddle)
        #moving the ball
        ball.move()
        #handle collision
        game.handle_collision(ball, left_paddle, right_paddle)

        #calculating the score
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
        #winnig the game
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            #dispaying some text wfter winning
            win_text = "Left won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right won!"

        if won:
            winning_text = SCORE_FONT.render(win_text, 1, WHITE)
            #bliting in the middle of the screen with math calcus :)
            WIN.blit(winning_text,(WIDTH // 2 - winning_text.get_width()//2, HEIGHT // 2 - winning_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0


     #exiting the game  
    pygame.quit()


#runs the game only if its directly called from this window
if __name__ == '__main__':
    main()