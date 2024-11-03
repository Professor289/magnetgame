# import pygame
# import sys
# from collections import deque
# from elemant import backgroundcolor, size_cell, SCREEN_HEIGHT, SCREEN_WIDTH, Ball, Magnet, Target

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)
# GREEN = (0, 255, 0)
# PURPLE = (128, 0, 128)

# class MagnetGame:
#     def __init__(self, n, max_steps):
#         pygame.init()
#         self.n = n
#         self.max_steps = max_steps
#         self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#         pygame.display.set_caption("لعبة المغناطيس")
#         self.clock = pygame.time.Clock()
#         self.grid = [[None for _ in range(n)] for _ in range(n)]
#         self.magnets = []
#         self.balls = []
#         self.targets = []
#         self.blocks = [] 
#         self.steps = 0
#         self.font = pygame.font.SysFont(None, 40)
#         self.won = False
#         self.lost = False
#         self.solution_steps = []
#         self.selected_magnet = None
#         self.is_player_mode = True 

#     def draw_grid(self):
#         for x in range(0, SCREEN_WIDTH, size_cell):
#             for y in range(0, SCREEN_HEIGHT, size_cell):
#                 rect = pygame.Rect(x, y, size_cell, size_cell)
#                 color = WHITE if (x // size_cell < self.n and y // size_cell < self.n) else PURPLE
#                 pygame.draw.rect(self.screen, color, rect, 1)

#     def draw_elemant(self):
#         for block in self.blocks:  
#             block_rect = pygame.Rect(block[0] * size_cell, block[1] * size_cell, size_cell, size_cell)
#             pygame.draw.rect(self.screen, PURPLE, block_rect)

#         for magnet in self.magnets:
#             pygame.draw.circle(self.screen, RED if magnet.type == "+" else BLUE, magnet.position, size_cell // 2)
        
#         for ball in self.balls:
#             pygame.draw.circle(self.screen, BLACK, ball.position, size_cell // 4)
        
#         for target in self.targets:
#             pygame.draw.circle(self.screen, GREEN, target.position, size_cell // 4)

#     def add_magnet(self, x, y, type):
#         self.magnets.append(Magnet(x, y, type))

#     def add_ball(self, x, y):
#         self.balls.append(Ball(x, y))

#     def add_target(self, x, y):
#         self.targets.append(Target(x, y))

#     def add_block(self, x, y):  
#         self.blocks.append((x, y))

#     def is_block(self, x, y): 
#         return (x, y) in self.blocks

#     def move_magnet_to(self, magnet, x, y):
#         if 0 <= x < self.n and 0 <= y < self.n and not self.is_block(x, y):  
#             magnet.move(x, y)
#             if self.is_player_mode:  
#                 self.steps += 1
#             self.apply_magnet_effect(magnet)


#     def apply_magnet_effect(self, magnet):
#         for ball in self.balls:
#             if not ball.is_on_target:
#                 if magnet.type == "+":
#                     ball.move_towards(magnet.x, magnet.y, self.magnets, self.n)
#                 elif magnet.type == "-":
#                     ball.move_away_from(magnet.x, magnet.y, self.magnets, self.n)
#         for ball in self.balls:
#             ball.check_target(self.targets)

#     def check_win(self):
#         if self.is_player_mode and self.steps > self.max_steps:
#             self.lost = True
#             return False

#         all_balls_on_target = all(ball.is_on_target for ball in self.balls)
#         all_magnets_on_target = all(
#             any((target.x, target.y) == (magnet.x, magnet.y) for target in self.targets)
#             for magnet in self.magnets
#         )
#         if all_balls_on_target and all_magnets_on_target:
#             self.won = True
#         return self.won

#     def message_win(self):
#         win_text = self.font.render(f"You won the game in {self.steps} steps!", True, BLACK)
#         self.screen.blit(win_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

#     def message_lost(self):
#         loss_text = self.font.render("You lost! Exceeded maximum steps.", True, (255, 0, 0))
#         self.screen.blit(loss_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

#     def handle_mouse_click(self, pos):
#         x, y = pos[0] // size_cell, pos[1] // size_cell
#         if self.selected_magnet:
#             self.move_magnet_to(self.selected_magnet, x, y)
#             self.selected_magnet = None
#         else:
#             for magnet in self.magnets:
#                 if (magnet.x, magnet.y) == (x, y):
#                     self.selected_magnet = magnet
#                     break

#     def dfs_solve(self):
#         self.is_player_mode = False  
#         target_x, target_y = self.balls[0].x, self.balls[0].y 
#         start_x, start_y = self.magnets[0].x, self.magnets[0].y
#         stack = [(start_x, start_y, [])]
#         visited = set()

#         while stack:
#             x, y, path = stack.pop()
#             if (x, y) in visited:
#                 continue
#             visited.add((x, y))

            
#             self.move_magnet_to(self.magnets[0], x, y)
#             path.append((x, y))

            
#             if self.check_win():
#                 self.solution_steps = path
#                 print(f"DFS solution path: {self.solution_steps}")
#                 return True

           
#             directions = []
#             if target_x > x:
#                 directions.append((1, 0)) 
#             elif target_x < x:
#                 directions.append((-1, 0))  
#             if target_y > y:
#                 directions.append((0, 1)) 
#             elif target_y < y:
#                 directions.append((0, -1))  
            
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 if (dx, dy) not in directions:
#                     directions.append((dx, dy))

#             for dx, dy in directions:
#                 new_x, new_y = x + dx, y + dy
#                 if 0 <= new_x < self.n and 0 <= new_y < self.n and not self.is_block(new_x, new_y):
#                     stack.append((new_x, new_y, path.copy()))

#         print("DFS: No solution.")
#         return False


#     def bfs_solve(self):
#         self.is_player_mode = False 
#         queue = deque([(self.magnets[0].x, self.magnets[0].y, [])])
#         visited = set()

#         while queue:
#             x, y, path = queue.popleft()
#             if (x, y) in visited:
#                 continue
#             visited.add((x, y))

#             self.move_magnet_to(self.magnets[0], x, y)
#             path.append((x, y))

#             print(f"BFS current path: {path}")

#             if self.check_win():
#                 self.solution_steps = path
#                 print(f"BFS solution path: {self.solution_steps}")
#                 return True

#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 new_x, new_y = x + dx, y + dy
#                 if 0 <= new_x < self.n and 0 <= new_y < self.n and not self.is_block(new_x, new_y):  # استخدام is_block
#                     queue.append((new_x, new_y, path.copy()))

#         print("BFS: No solution.")
#         return False

#     def game_loop(self):
#         while True:
#             self.screen.fill(backgroundcolor)
#             self.draw_grid()
#             self.draw_elemant()

#             if self.won:
#                 self.message_win()
#             elif self.lost:
#                 self.message_lost()
#             else:
#                 if self.check_win():
#                     self.won = True
#                 elif self.lost:
#                     self.message_lost()

#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         sys.exit()
#                     elif event.type == pygame.MOUSEBUTTONDOWN:
#                         self.is_player_mode = True  
#                         self.handle_mouse_click(pygame.mouse.get_pos())
#                     elif event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_g:  
#                             print("Starting DFS...")
#                             if self.dfs_solve():
#                                 print("DFS: Solution found!")
#                             else:
#                                 print("DFS: No solution.")
#                         elif event.key == pygame.K_b: 
#                             print("Starting BFS...")
#                             if self.bfs_solve():
#                                 print("BFS: Solution found!")
#                             else:
#                                 print("BFS: No solution.")
            
#             pygame.display.flip()
#             self.clock.tick(60)
import pygame
import sys
from elemant import backgroundcolor, size_cell, HEIGHT, WIDTH, Ball, Magnet, Target

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
purple = (128, 0, 128)

class LogicMagnet:
    def __init__(self, n, full_steps):
        pygame.init()
        self.n = n
        self.full_steps = full_steps
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("لعبة المغناطيس")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 40)
        self.grid = [[None for _ in range(n)] for _ in range(n)]
        self.magnets = []
        self.balls = []
        self.targets = []
        self.blocks = [] 
        self.steps = 0
        self.font = pygame.font.SysFont(None, 40)
        self.win = False
        self.lost = False
        self.selected_magnet = None
        self.is_player_mode = True 

    def draw_grid(self):
        for x in range(0, WIDTH, size_cell):
            for y in range(0, HEIGHT, size_cell):
                rect = pygame.Rect(x, y, size_cell, size_cell)
                color = WHITE if (y // size_cell < self.n and x // size_cell < self.n) else purple
                pygame.draw.rect(self.screen, color, rect, 1)

    def draw_elemant(self):
        for block in self.blocks:  
            block_rect = pygame.Rect(block[0] * size_cell, block[1] * size_cell, size_cell, size_cell)
            pygame.draw.rect(self.screen, purple, block_rect)

        for magnet in self.magnets:
            pygame.draw.circle(self.screen, RED if magnet.type == "+" else BLUE, magnet.position, size_cell // 2)
        
        for ball in self.balls:
            pygame.draw.circle(self.screen, BLACK, ball.position, size_cell // 4)
        
        for target in self.targets:
            pygame.draw.circle(self.screen, GREEN, target.position, size_cell // 4)

    def add_target(self,x, y):
        self.targets.append(Target(x, y))
        
    def add_ball(self,x, y):
        self.balls.append(Ball(x, y))
    
    def add_magnet(self, x,y, type):
        self.magnets.append(Magnet(x, y, type))    

    def add_block(self, x,  y):  
        self.blocks.append((x, y))

    def is_block(self ,x, y): 
        return (x, y) in self.blocks

    def move_magnet_to(self, magnet, x, y):
        if 0 <= x < self.n and 0 <= y < self.n and not self.is_block(x, y):  
            magnet.move(x, y)
            if self.is_player_mode:  
                self.steps += 1
            self.apply_magnet_impact(magnet)

    def apply_magnet_impact(self, magnet):
        for ball in self.balls:
            if not ball.is_on_target:
                if magnet.type == "-":
                     ball.move_away_from(magnet.x, magnet.y, self.magnets, self.n)
                     
                elif magnet.type == "+":
                     ball.move_towards(magnet.x, magnet.y, self.magnets, self.n)
        for ball in self.balls:
            ball.check_target(self.targets)

    def check_win(self):
        if self.is_player_mode and self.full_steps < self.steps:
            self.lost = True
            return False

        balls_on_target = all(ball.is_on_target for ball in self.balls)#هنا تحقق جميع الكرات الحديدية في الاهداف
        
        magnets_on_target = all(any((target.x, target.y) == (magnet.x, magnet.y) for target in self.targets)
            for magnet in self.magnets)
        
        if balls_on_target and magnets_on_target:
            self.win = True
        return self.win

    def message_win(self):
        win_text = self.font.render(f"you win in game in {self.steps}steps!", True, BLACK)
        self.screen.blit(win_text, (WIDTH // 6, HEIGHT // 2))

    def message_lost(self):
        loss_text = self.font.render("You lost! Exceeded maximum steps.", True, (255, 0, 0))
        self.screen.blit(loss_text, (WIDTH // 6,HEIGHT // 2))

    def handle_mouse_click(self, pos):
        x, y = pos[0] // size_cell, pos[1] // size_cell
        if self.selected_magnet:
            self.move_magnet_to(self.selected_magnet, x, y)
            self.selected_magnet = None
        else:
            for magnet in self.magnets:
                if (magnet.x, magnet.y) == (x, y):
                    self.selected_magnet = magnet
                    break

    def game_loop(self):
        while True:
            self.screen.fill(backgroundcolor)
            self.draw_grid()
            self.draw_elemant()

            if self.win:
                self.message_win()
            elif self.lost:
                self.message_lost()
            else:
                if self.check_win():
                    self.win = True
                elif self.lost:
                    self.message_lost()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.is_player_mode = True  
                        self.handle_mouse_click(pygame.mouse.get_pos())
            
            pygame.display.flip()
            self.clock.tick(60)
