import pygame
pygame.init()


class Game:
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    WIDTH, HEIGHT = 700, 500
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    #font for drawing scores
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    BLACK = (0,0,0)
        #draw func to draw on the window
    
    def __init__(self):
        self.left_hits = 0
        self.right_hits = 0

    def draw(self, win, paddles, ball, left_score, right_score,draw_hits=False):
        win.fill(self.BLACK)
        #drawing score:
        left_score_text = self.SCORE_FONT.render(f"{left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(f"{right_score}", 1, self.WHITE)
        win.blit(left_score_text,(self.WIDTH//4 - left_score_text.get_width()//2, 20))
        win.blit(right_score_text,(self.WIDTH * (3/4) - right_score_text.get_width()//2, 20))
        if draw_hits:
            total_hits_draw = self.SCORE_FONT.render(f"{self.left_hits + self.right_hits}", 1, self.WHITE)
            win.blit(total_hits_draw,(self.WIDTH//2 - total_hits_draw.get_width()//2, 10))

        #draw paddles and ball in the window
        for paddle in paddles:
            paddle.draw(win)
        #drawing dashed line in the middle of the window
        for i in range(10, self.HEIGHT, self.HEIGHT//20):
            #skip odd number i 
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, self.WHITE, (self.WIDTH//2 - 5, i, 10, self.HEIGHT//20))

        ball.draw(win)
        # .update is gonna preform all the operations we ahve done with drawing and display them on the win
        pygame.display.update()

    #handling collision
    def handle_collision(self, ball, left_paddle, right_paddle):
        
        #celling collision
        if ball.y + ball.RADIUS >= self.HEIGHT:
            #hittin up --> reverse velocity
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            #hittin down --> reverse velocity again
            ball.y_vel *= -1

        #left paddle collision
        if ball.x_vel < 0:
            #locaiting the paddle and calculating x_vel
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.PADDLE_HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + left_paddle.PADDLE_WIDTH:
                    ball.x_vel *= -1

                    #calculating y_vel
                    middle_y = left_paddle.y + left_paddle.PADDLE_HEIGHT / 2
                    difference_in_y = middle_y -ball.y
                    reduction_factor = (left_paddle.PADDLE_HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel 
                    self.left_hits += 1     

        else:
            #right paddle collision
            #locaiting the paddle and calculating x_vel
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.PADDLE_HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1
                    
                    #calculating y_vel
                    middle_y = right_paddle.y + right_paddle.PADDLE_HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.PADDLE_HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1 

            
    def game_info_hits(self):
        return [self.left_hits, self.right_hits]
    
    

    def hits_reset(self):
        self.left_hits = 0
        self.right_hits = 0

    #handling movement func
    def handle_paddle_movement(self, keys, left_paddle, right_paddle, ai_key=''):
        #keys[pygame.K_w] returns true if we press W
        #left paddle movement
        if (keys[pygame.K_w] or ai_key == 'w' )and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if (keys[pygame.K_s] or ai_key == 's' )and left_paddle.y + left_paddle.VEL + self.PADDLE_HEIGHT < self.HEIGHT:
            left_paddle.move(up=False)
        
        #right paddle movement
        if (keys[pygame.K_UP] or ai_key == 'UP') and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if (keys[pygame.K_DOWN] or ai_key == 'DOWN') and right_paddle.y + right_paddle.VEL +self.PADDLE_HEIGHT < self.HEIGHT:
            right_paddle.move(up=False)
    