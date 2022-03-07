import pygame
#always initialize pygame first
pygame.init()

#1st draw windov with width, height

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# displays window with the name Pong
pygame.display.set_caption("Pong")

FPS = 60

#drawing on the window with func draw:
WHITE = (255,255,255)
BLACK = (0,0,0)

#values for width and height or the paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

#ball radius
RADIUS = 7

#font for drawing scores
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

#winning
WINNING_SCORE = 3

#creating paddles
class Paddle:
    COLOR = WHITE
    #velocity of how much will paddles move once we hit up or down key 
    VEL = 4

    #intialize x,y cordinates where to draw and witdt and height of rectangle how big to draw
    def __init__(self, x, y, width, height):
        self.x = self.orginial_x = x
        self.y = self.orginial_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        #drawing rectangle (we need window, color(cprdinate x and y, width, height))
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height) )

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self):
        self.x = self.orginial_x
        self.y = self.orginial_y

class Ball:
    COLOR = WHITE
    
    #velocity of how FAST will ball move once we start
    MAX_VEL = 5
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        #drawing rectangle (we need window, color(cordinate x and y), radius)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius )
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0

#draw func to draw on the window
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    #drawing score:
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text,(WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    #draw paddles and ball in the window
    for paddle in paddles:
        paddle.draw(win)
    #drawing dashed line in the middle of the window
    for i in range(10, HEIGHT, HEIGHT//20):
        #skip odd number i 
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    # .update is gonna preform all the operations we ahve done with drawing and display them on the win
    pygame.display.update()

#handling collision
def handle_collision(ball, left_paddle, right_paddle):
    #celling collision
    if ball.y + ball.radius >= HEIGHT:
        #hittin up --> reverse velocity
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        #hittin down --> reverse velocity again
        ball.y_vel *= -1

    #left paddle collision
    if ball.x_vel < 0:
        #locaiting the paddle and calculating x_vel
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                #calculating y_vel
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y -ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel      

    else:
        #right paddle collision
        #locaiting the paddle and calculating x_vel
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                
                #calculating y_vel
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

        


#handling movement func
def handle_paddle_movement(keys, left_paddle, right_paddle):
    #keys[pygame.K_w] returns true if we press W
    #left paddle movement
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + PADDLE_HEIGHT < HEIGHT:
        left_paddle.move(up=False)
    
    #right paddle movement
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + PADDLE_HEIGHT < HEIGHT:
        right_paddle.move(up=False)
    

def main():
    run = True
    clock = pygame.time.Clock() #sets fps for every pc its gonna run the same speed on every pc
    
    #setting where the left  and right paddle gonna be draw
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS) #wont run faster than 60 fps on every pc
        #passing every elemet to the drawing function
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        #loopin through all the events taht occur like hiting keyboard etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exiting the game
                run =False
                break
        
        #getting pressed keys
        keys = pygame.key.get_pressed()
        #handling movemnet with aonther func to avoid clustering our mani func
        handle_paddle_movement(keys, left_paddle, right_paddle)
        #moving the ball
        ball.move()
        #handle collision
        handle_collision(ball, left_paddle, right_paddle)

        #calculating the core
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
            pygame.time.delay(5000)
            
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