import pygame
import os
import sys
import threading
from gtts import gTTS

from select_question_ui import scale_image_to_max_size

def speak_word(word):
    audio_file = word + ".mp3"
    audio_file = os.path.join("voice", audio_file)
    # 確保混音器已初始化
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def download_word_audio(words):
    # 將錯誤的單字「全部」進行下載
    if not os.path.exists("voice"):
        os.makedirs("voice")
    for word in words:
        audio_file = word + ".mp3"
        audio_file = os.path.join("voice", audio_file)
        if not os.path.exists(audio_file):
            tts = gTTS(text=word, lang='en')
            tts.save(audio_file)

def download_audio_in_background(words):
    # 創建並啟動一個新線程來處理音頻下載
    download_thread = threading.Thread(target=download_word_audio, args=(words,))
    download_thread.start()
    
def show_wrong_words(wrong_words, wifi, folder_path="questions", max_size=80): 
    # 如果沒有錯字，則返回 
    if len(wrong_words) == 0:
        return 0 
    # 使用多線程在背景下載音檔
    download_audio_in_background(wrong_words) if wifi else None
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Review Wrong Words")

    font = pygame.font.SysFont(None, 24)
    gap = 10
    start_x, start_y = 20, 50
    box_height = 150
    box_width = 100
    max_row_count = 7

    # 加載錯誤單詞的圖片
    images = {}
    for word in wrong_words:
        for ext in ['.png', '.jpg', '.jpeg']:
            file_path = os.path.join(folder_path, word + ext)
            if os.path.exists(file_path):
                image = pygame.image.load(file_path)
                image = scale_image_to_max_size(image, max_size)
                images[word] = image
                break
    
    # 主畫面渲染
    while True:
        screen.fill((255, 255, 255))
        rects = []

        for i, (word, img) in enumerate(images.items()):
            row = i // max_row_count
            column = i % max_row_count
            x = start_x + column * (box_width + gap)
            y = start_y + row * (box_height * 1.2)

            rect = pygame.Rect(x, y, box_width, box_height)
            pygame.draw.rect(screen, (200, 200, 200), rect, border_radius=15)
            rects.append((rect, word))  

            img_rect = img.get_rect(center=(rect.centerx, rect.centery - 15))
            screen.blit(img, img_rect)

            text = font.render(word, True, (0, 0, 0))
            text_rect = text.get_rect(center=(rect.centerx, rect.centery + 55))
            screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, word in rects:
                    if rect.collidepoint(event.pos):
                        speak_word(word) if wifi else None

        pygame.display.flip()


if __name__ == "__main__":
    words= ['eraser', 'cloud', 'pencil', 'phone', 'apple', 'glasses', 'cup', 'light', 'book', 'lemon', 'candy']
    show_wrong_words(words)