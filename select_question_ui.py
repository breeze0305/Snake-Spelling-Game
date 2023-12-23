import pygame
import sys
import os
import random
def load_images(folder_path, max_size=80):
    images = {}
    supported_formats = {".png", ".jpg", ".jpeg"}
    files = os.listdir(folder_path)
    random.shuffle(files)
    files = sorted(files[:21])
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext.lower() in supported_formats:
            image_path = os.path.join(folder_path, filename)
            image = pygame.image.load(image_path)
            image = scale_image_to_max_size(image, max_size)
            images[name] = image   
    return images

def scale_image_to_max_size(image, max_size):
    width, height = image.get_size()
    scale = min(max_size / width, max_size / height)
    new_size = (int(width * scale), int(height * scale))
    return pygame.transform.scale(image, new_size)

def select_word_ui(images):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Words")

    font = pygame.font.SysFont(None, 24)
    gap = 10
    start_x, start_y = 20, 50
    box_height = 150
    box_width = 100
    max_row_count = 7

    # 跟蹤每個單詞是否被選中
    selected_words = {word: False for word in images}

    while True:
        screen.fill((255, 255, 255))
        rects = []

        for i, (word, img) in enumerate(images.items()):
            row = i // max_row_count
            column = i % max_row_count
            x = start_x + column * (box_width + gap)
            y = start_y + row * (box_height * 1.2)

            rect = pygame.Rect(x, y, box_width, box_height)
            color = (173, 214, 255) if selected_words[word] else (200, 200, 200) 
            pygame.draw.rect(screen, color, rect, border_radius=15)
            rects.append(rect)

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
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        word = list(images.keys())[i]
                        selected_words[word] = not selected_words[word]  # 切換選中狀態
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 按下 Enter 鍵
                    return [word for word, selected in selected_words.items() if selected]  # 返回選中的單詞列表

        pygame.display.flip()

def lauch_preprocessing(path="questions"):
    images = load_images(path)
    selected_words = select_word_ui(images)
    return selected_words


