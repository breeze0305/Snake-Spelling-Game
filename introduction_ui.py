import pygame
import urllib.request

def check_internet_connection():
    try:
        # 嘗試訪問Google主頁來測試網絡連接
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False

def show_rules_and_set_speed():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Rules and Speed Setting")
    font = pygame.font.SysFont(None, 40)

    # 檢查網絡連接
    internet_connection = check_internet_connection()
    wifi_status_text = "WiFi Connected" if internet_connection else "No WiFi Connection"
    
    speed = 1  # 默認速度
    running = True

    while running:
        screen.fill((255, 255, 255))  # 白色背景
        font_path = "jf-openhuninn-1.1.ttf"  # 替換為您的中文字體文件路徑
        font = pygame.font.Font(font_path, 30)  # 使用中文字體
        
        # 顯示規則文字
        rules_text = [
            "Game Rules:",
            "1. 請按上下左右來控制蛇",
            "2. 按下【enter】後會唸出單字的發音(需要啟動朗讀功能)",
            "3. 按下【backspace】後遊戲會直接結束",
            "4. 回頭、撞到牆壁、吃到錯誤的拼字，都會直接結束遊戲",
            "請使用【上】、【下】來調整蛇的速度(最慢1~最快5).",
            "按下【enter】後請選擇單字(可多選)並再次按下【enter】",
            "開始遊戲"
        ]
        y = 10
        for line in rules_text:
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (20, y))
            y += 60

        # 顯示速度
        speed_text = font.render(f"Speed: {speed}", True, (244, 0, 0))
        screen.blit(speed_text, (650, 500))

        # 顯示WiFi狀態
        if internet_connection:
            wifi_status_text = "WiFi Connected：已啟用朗讀功能"
            wifi_status_color = (0, 128, 0)  # 綠色表示有連接
        else:
            wifi_status_text = "No WiFi Connection：無朗讀功能"
            wifi_status_color = (255, 0, 0)  # 紅色表示無連接

        wifi_status_surface = font.render(wifi_status_text, True, wifi_status_color)
        screen.blit(wifi_status_surface, (20, 500))  # 調整位置以適應您的界面


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    speed = min( speed + 1, 5 )  # 最大5
                elif event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)  # 最小1
                elif event.key == pygame.K_RETURN:
                    speed = 15 - speed
                    return speed, internet_connection  # 確認速度並返回

        pygame.display.flip()

    pygame.quit()
    return speed, internet_connection  # 返回速度和WiFi狀態

if __name__ == "__main__":
    selected_speed, wifi_connected = show_rules_and_set_speed()
    print("Selected Speed:", selected_speed)
    print("WiFi Connected:", wifi_connected)
