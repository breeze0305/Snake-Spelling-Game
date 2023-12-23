import pygame
import time
import random
import string
import os
from gtts import gTTS

from select_question_ui import lauch_preprocessing
from introduction_ui import show_rules_and_set_speed
from review_wrong_ui import show_wrong_words

class snake_game():
    def __init__(self,word,speed):
        # color
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        
        # window
        self.dis_width = 600
        self.dis_height = 400
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        
        # snake
        self.snake_block = 20
        self.clock = pygame.time.Clock()
        self.snake_list = []
        self.word_list = ['']
        self.length_of_snake = 1
        self.current_index = 0
        self.spawn_x = self.dis_width / 2
        self.spawn_y = self.dis_height / 2
        
        # font
        self.font_style = pygame.font.SysFont(None, 50)
        self.letter_font = pygame.font.SysFont(None, 25)
        
        # word
        self.target_word = word
        
        # audio
        self.audio_file_exit = False
        self.audio_file_name = "temp.mp3"
        
        # time
        self.tick = 50
        self.snake_speed = speed # 1->fastest

    def set_caption(self):
        pygame.display.set_caption("Snake Spelling Game")

    def load_background(self):
        extensions = ['.png', '.jpg', '.jpeg']
        for ext in extensions:
            file_path = os.path.join("questions", self.target_word + ext)
            if os.path.exists(file_path):
                # 加載圖片
                image = pygame.image.load(file_path).convert_alpha()
                
                # 獲取原始圖片尺寸
                orig_width, orig_height = image.get_size()
                aspect_ratio = orig_width / orig_height

                # 計算新尺寸
                new_width, new_height = self.dis_width, int(self.dis_width / aspect_ratio)
                if new_height > self.dis_height:
                    new_height = self.dis_height
                    new_width = int(self.dis_height * aspect_ratio)

                # 等比例縮放圖片
                image = pygame.transform.scale(image, (new_width, new_height))

                # 創建一個半透明的 Surface
                transparent_surface = pygame.Surface((self.dis_width, self.dis_height), pygame.SRCALPHA)
                transparent_surface.fill((255, 255, 255, 0))  # 填充透明背景

                # 將圖片繪製到這個半透明 Surface 上
                image_rect = image.get_rect(center = (self.dis_width // 2, self.dis_height // 2))
                transparent_surface.blit(image, image_rect)

                # 設置透明度
                transparent_surface.set_alpha(80)  # 設置半透明，50 為透明度值

                return transparent_surface
        return None


    def generate_food_position(self):
        word = self.target_word
        positions = []
        used_positions = set()
        extra_number = len(word) if len(word) > 5 else len(word) + 3
        letters = list(word) + random.sample(string.ascii_lowercase, extra_number)
        random.shuffle(letters)

        for letter in letters:
            x = random.randrange(0, self.dis_width // self.snake_block) * self.snake_block
            y = random.randrange(0, self.dis_height // self.snake_block) * self.snake_block

            while (x, y) in used_positions or (x == self.spawn_x and y == self.spawn_y):
                x = random.randrange(0, self.dis_width // self.snake_block) * self.snake_block
                y = random.randrange(0, self.dis_height // self.snake_block) * self.snake_block

            positions.append((x, y, letter))
            used_positions.add((x, y))

        return positions

    
    def draw_food(self,food_positions):
        for food in food_positions:
            pygame.draw.rect(self.dis, self.blue, [food[0], food[1], self.snake_block, self.snake_block])
            text = self.letter_font.render(food[2], True, self.white)
            self.dis.blit(text, [food[0] + 5, food[1] + 2])
    
    def our_snake(self):
        for i, pos in enumerate(reversed(self.snake_list)): 
            color = self.blue if i > 0 else self.black  # 蛇頭是黑色，蛇身是藍色
            pygame.draw.rect(self.dis, color, [pos[0], pos[1], self.snake_block, self.snake_block])

            if i > 0 and i < len(self.word_list):
                letter = self.word_list[i]
                text = self.letter_font.render(letter, True, self.white)
                self.dis.blit(text, [pos[0] + 5, pos[1] + 2])

    def init_window(self):
        # 繪製白底
        self.dis.fill(self.white)

        # 繪製網格
        for x in range(0, self.dis_width, self.snake_block):  
            pygame.draw.line(self.dis, self.black, (x, 0), (x, self.dis_height))
        for y in range(0, self.dis_height, self.snake_block): 
            pygame.draw.line(self.dis, self.black, (0, y), (self.dis_width, y))

        # 繪製半透明背景圖片
        background = self.load_background()
        if background:
            self.dis.blit(background, (0, 0))
            
    def show_victory_screen(self):
        self.dis.fill(self.white)
        victory_text = self.font_style.render('You Win!', True, self.green)
        text_rect = victory_text.get_rect(center=(self.dis_width / 2, self.dis_height / 2))
        self.dis.blit(victory_text, text_rect)
        pygame.display.update()
    
    def show_game_over_screen(self):
        self.dis.fill(self.white)
        game_over_text = self.font_style.render('Game Over', True, self.red)
        text_rect = game_over_text.get_rect(center=(self.dis_width / 2, self.dis_height / 2))
        self.dis.blit(game_over_text, text_rect)
        pygame.display.update()
    
    def speak_word(self):
        if not self.audio_file_exit:
            tts = gTTS(text=self.target_word, lang='en')
            self.audio_file_name = 'temp.mp3'
            tts.save(self.audio_file_name)
            self.audio_file_exit = True

        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file_name)
        pygame.mixer.music.play()
        
    def cleanup(self):
        if self.audio_file_exit and os.path.exists(self.audio_file_name):
            pygame.mixer.init()
            pygame.mixer.music.unload()
            os.remove(self.audio_file_name)
        
# Main game loop
def gameLoop(word,speed,wifi):
    pygame.init()
    snake=snake_game(word,speed)
    game_over = False
    game_win = False
    x1 = snake.spawn_x
    y1 = snake.spawn_y

    x1_change = 0
    y1_change = 0
    tick = snake.snake_speed
    
    snake.set_caption()
    snake.speak_word() if wifi else None
    food_positions = snake.generate_food_position()
    
    while not game_over and not game_win:
        
        snake.init_window()
        snake.draw_food(food_positions)
        
        # user control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake.snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake.snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake.snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake.snake_block
                    x1_change = 0
                elif event.key == pygame.K_RETURN and wifi:
                    snake.speak_word()
                elif event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    snake.cleanup()
                    quit()
                     
                    
        # speed control
        if tick == snake.snake_speed:
            tick = 0
            x1 += x1_change
            y1 += y1_change

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake.snake_list.append(snake_head)
            if len(snake.snake_list) > snake.length_of_snake:
                del snake.snake_list[0]
        else:
            tick+=1
        
        # 1.Check if snake eats a letter
        for food in food_positions:
            if x1 == food[0] and y1 == food[1]:
                if food[2] == snake.target_word[snake.current_index]:
                    snake.word_list.append(food[2])
                    snake.current_index += 1
                    food_positions.remove(food)
                    snake.length_of_snake += 1
                    if snake.current_index == len(snake.target_word):
                        game_win = True
                else:
                    game_over = True
        
        # 2.Check if snake run out
        if x1 >= snake.dis_width or x1 < 0 or y1 >= snake.dis_height or y1 < 0:
            game_over = True

        snake.our_snake()  # 繪製貪食蛇
        
        # 3.Check if snake hit itself 
        for x in snake.snake_list[:-1]:
            if x == snake_head:
                game_over = True

        pygame.display.update()
        snake.clock.tick(snake.tick)

    if game_win:
        snake.show_victory_screen()
    elif game_over:
        snake.show_game_over_screen()
    snake.cleanup()
    time.sleep(2) 
    pygame.quit()
    return snake.target_word if game_over else None


def main():
    wrong_vocs = []
    question_folder_path = "questions"
    speed , wifi = show_rules_and_set_speed()
    vocs = lauch_preprocessing(question_folder_path)
    for vocabulary in vocs:
        word = gameLoop(vocabulary,speed,wifi)
        wrong_vocs.append(word) if word else None
        
    show_wrong_words(wrong_vocs,wifi)


if __name__=="__main__":
    main()