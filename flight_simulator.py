import pygame
import sys
import math

# 初始化Pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("飞行模拟器")

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Aircraft:
    def __init__(self, name, speed, max_altitude):
        self.name = name
        self.speed = speed
        self.max_altitude = max_altitude
        self.x = WINDOW_WIDTH // 4
        self.y = WINDOW_HEIGHT - 100
        self.altitude = 0
        self.angle = 0
        
    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        
        # 确保飞机不会飞出屏幕
        self.x = max(0, min(self.x, WINDOW_WIDTH))
        self.y = max(0, min(self.y, WINDOW_HEIGHT))

class Game:
    def __init__(self):
        self.aircrafts = [
            Aircraft("小型飞机", 3, 5000),
            Aircraft("中型客机", 5, 8000),
            Aircraft("军用战斗机", 7, 12000)
        ]
        self.selected_aircraft = None
        self.game_state = "selection"  # selection, flying, landed
        self.altitude = 0
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "selection":
                    self.handle_aircraft_selection(event.pos)
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.game_state == "flying":
                        self.game_state = "landed"
                        print("紧急着陆完成！游戏结束。")
                        pygame.quit()
                        sys.exit()
            
            if self.game_state == "flying":
                self.handle_flight_controls()
            
            self.draw()
            clock.tick(60)
    
    def handle_aircraft_selection(self, pos):
        # 处理飞机选择逻辑
        mouse_x, mouse_y = pos
        selection_y = 200
        for i, aircraft in enumerate(self.aircrafts):
            if 100 <= mouse_x <= 300 and selection_y <= mouse_y <= selection_y + 50:
                self.selected_aircraft = aircraft
                self.game_state = "flying"
            selection_y += 100
    
    def handle_flight_controls(self):
        keys = pygame.key.get_pressed()
        
        # 控制飞行高度
        if keys[pygame.K_UP] and self.selected_aircraft.altitude < self.selected_aircraft.max_altitude:
            self.selected_aircraft.altitude += 50
        if keys[pygame.K_DOWN] and self.selected_aircraft.altitude > 0:
            self.selected_aircraft.altitude -= 50
            
        # 控制方向
        if keys[pygame.K_LEFT]:
            self.selected_aircraft.angle = (self.selected_aircraft.angle + 2) % 360
        if keys[pygame.K_RIGHT]:
            self.selected_aircraft.angle = (self.selected_aircraft.angle - 2) % 360
            
        self.selected_aircraft.move()
    
    def draw(self):
        screen.fill(WHITE)
        
        if self.game_state == "selection":
            self.draw_selection_screen()
        elif self.game_state == "flying":
            self.draw_flight_screen()
            
        pygame.display.flip()
    
    def draw_selection_screen(self):
        font = pygame.font.Font(None, 36)
        text = font.render("请选择飞机：", True, BLUE)
        screen.blit(text, (100, 100))
        
        selection_y = 200
        for aircraft in self.aircrafts:
            pygame.draw.rect(screen, GREEN, (100, selection_y, 200, 50))
            text = font.render(aircraft.name, True, BLUE)
            screen.blit(text, (120, selection_y + 15))
            selection_y += 100
    
    def draw_flight_screen(self):
        # 绘制天空和地面
        pygame.draw.rect(screen, BLUE, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - 100))
        pygame.draw.rect(screen, GREEN, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
        
        # 绘制飞机
        pygame.draw.circle(screen, RED, (int(self.selected_aircraft.x), int(self.selected_aircraft.y)), 10)
        
        # 显示高度信息
        font = pygame.font.Font(None, 36)
        altitude_text = font.render(f"高度: {self.selected_aircraft.altitude}米", True, WHITE)
        screen.blit(altitude_text, (20, 20))

if __name__ == "__main__":
    game = Game()
    game.run() 