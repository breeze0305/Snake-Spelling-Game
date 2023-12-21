# 遊戲簡介
此遊戲是一款基於Pygame框架開發的互動式學習遊戲-貪食蛇拼字。它結合了顏色豐富的圖形界面和教育性質的遊戲玩法，旨在提供一個有趣且具啟發性的學習環境，並促進學生主動學習的動力。

<img src="/document/picture.png" alt="蛇" width="200" height="150">


# 安裝指南
1. 確保您的電腦上安裝了Python。
2. 安裝Pygame庫：在終端或命令提示符中運行 `pip install pygame`，Pygame主要負責渲染並展示遊戲畫面。
3. 安裝gTTs庫：在終端或命令提示符中運行 `pip install gTTS`，gTTs主要負責將文字轉為語音，念出遊戲單字。
4. 下載遊戲代碼文件。
```
main.py
introduction_ui.py
select_question_ui.py
review_wrong_ui.py
```
5. 將上述文件放在同一目錄下，並且建立一個名稱為 `questions`的資料夾來放置客制化的題目，請將題目圖片以單字拼音(小寫)作為檔名，放入資料夾內即可。
```
可接受的檔名範例：
.png
.jpg
.jepg
```
6. 在遊戲代碼所在的目錄下打開終端或命令提示符，執行 `python main.py` 啟動遊戲。

# 文件結構展示
```
snake_spelling_game/  
├─ main.py  
├─ introduction_ui.py  
├─ select_question_ui.py  
├─ review_wrong_ui.py  
├─ questions/  
    ├─ apple.png  
    ├─ banana.jpg  
    ├─ carrot.jpeg  
    ├─ ...
```

# 如何玩
- 在啟動遊戲後，首先會出現遊戲規則和速度設置介面。
- 根據屏幕上的指示進行操作，學習遊戲規則並設置您喜歡的速度。
- 透過按下【上】【下】【左】【右】方向鍵進行操作，題目會以半透明的方式顯示在遊戲的背景。
- 遊戲過程中，您可以透過按下【Enter】鍵來聆聽單字的發音，按下【Backspace】鍵則可直接中斷遊戲。


# 內容說明
- `main.py` 遊戲主程式，負責主要遊戲迴圈與呼叫其他介面。
- `introduction_ui.py` 遊戲規則介面，展示操作說明和選擇遊戲困難度，負責回傳 __遊戲速度__ 和 __wifi連接狀態__。
- `select_question_ui.py` 選擇題目介面，讀取`questions`資料夾內的檔案，並展示題目選項，可多選並返還list。
- `review_wrong_ui.py` 回顧錯題介面，傳入錯題的list並顯示，點擊圖片即可收聽發音。
