import pygame as pg
import os
import Player
import Mosquito
import Draw
import Boom
import time
import sound_a

# 設定遊戲的FPS與畫面(用大寫代表定值不做修改)
FPS = 60
WIDTH = 900
HEIGHT = 600

# 初始化pygame與音效mixer
pg.init()
pg.mixer.init()

# 建立名叫screen的視窗
screen = pg.display.set_mode((WIDTH, HEIGHT))

# 建立視窗標題
pg.display.set_caption("滅蚊大進擊")

# 創建管理時間的物件
clock = pg.time.Clock()

# 讀取並設置左上角icon
icon = pg.image.load(os.path.join("img","mosquito1.png"))
pg.display.set_icon(icon)

# 讀取背景圖，並將背景圖設置為screen長寬
bg_img = pg.image.load(os.path.join("img", "background.jpg"))
background_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))

# 創建生命圖片(遊戲右上角噴霧罐)
lifes_img = pg.image.load(os.path.join("img", "bottle.png"))
lifes_img = pg.transform.scale(lifes_img, (30, 30))

# 加載爆炸圖片(蚊子跟噴霧罐)
Boom.load_boom()

# 載入初始音樂
sound_a.back_sound()


# 設置初始背景位置
# x1放置於主畫面的位置，x2放置於主畫面以外的右側，如圖示 → 口口
bg_x1 = 0
bg_x2 = WIDTH
scroll_speed = 1  # 背景滾動速度

# 突然加速蚊子的變數
speed_increased = 1
boss = 1

# 跟踪遊戲的暫停狀態
paused = False

# 通關畫面的獎勵文字座標(通關後的操作提示在程式區塊修改)
clear_borad_text_size=50
textx=60
texty=240


# 取得Draw檔案中，draw_init()的回傳值，用來繪製首頁
(title_img,
 start_img, start1_img, start_rect, start1_rect,
 inf_img,   inf1_img,   inf_rect,   inf1_rect,
 exit_img,  exit1_img,  exit_rect,  exit1_rect  ) = Draw.draw_init(screen)
# 取得Draw檔案中，draw_rule()的回傳值，用來繪製操作頁面
back, back_rect, back1, back1_rect,rule_img = Draw.draw_rule(screen)


#初始畫面顯示狀態，遊戲運行狀態
show_init = True
running = True

#遊戲迴圈
#初始介面回圈
while running:
    
    if show_init:
        
        screen.blit(title_img, (0, 0))  # 绘制背景图像    
        
        # 检查游標位置，繪製按鈕
        mouse_pos = pg.mouse.get_pos()    
        if start1_rect.collidepoint(mouse_pos):
            screen.blit(start1_img, start1_rect.topleft)    # 繪製開始按鈕
        else:
            screen.blit(start_img, start_rect.topleft)      
        
        if inf1_rect.collidepoint(mouse_pos):               
            screen.blit(inf1_img, inf1_rect.topleft)        # 繪製說明按鈕
        else:
            screen.blit(inf_img, inf_rect.topleft)
            
        if exit1_rect.collidepoint(mouse_pos):
            screen.blit(exit1_img, exit1_rect.topleft)      # 繪製離開按鈕
        else:
            screen.blit(exit_img, exit_rect.topleft)
        
        pg.display.update()  # 更新畫面(將物件更新到screen)
                
        #pg.event.get()取得事件
        #判斷點擊按鈕或右上角直接關閉遊戲
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):  #初始畫面False往下進入遊戲
                    show_init = False
                    sound_a.click() #點擊音效撥放
                    break
                elif exit_rect.collidepoint(mouse_pos): #運行False外圈while直接跳出
                    running = False
                    sound_a.click()
                    time.sleep(0.3) #0.3秒後才beeak(目的讓點擊音效播完)
                    break
                elif inf_rect.collidepoint(mouse_pos): #進入操作介紹
                    screen.blit(rule_img, (0, 0)) #繪製操作圖片
                    sound_a.click()                  
                    show_rule = True #進入操作介紹初值
                    while show_rule:
                        mouse_pos = pg.mouse.get_pos()
                        if back_rect.collidepoint(mouse_pos):
                            screen.blit(back1, back1_rect.topleft)  # 繪製返回按鈕
                        else:
                            screen.blit(back, back_rect.topleft)
                        pg.display.update() #在操作介紹頁面回圈中更新畫面
                        
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                running = False
                                show_rule = False
                                break
                            elif event.type == pg.MOUSEBUTTONDOWN:
                                if back_rect.collidepoint(mouse_pos):
                                    sound_a.click()
                                    # 點擊back按鈕時，rule設為False，離開rule回圈
                                    show_rule = False
                                    break
        continue #循環show_init(遊戲首頁)，直到點開始遊戲show_init=False進入下段循環區塊
    
    #初始化積分
    score = 0
    
    #建立Sprite群組(Group)(簡介參閱inf.py)
    all_sprites = pg.sprite.Group()
    
    #建立player物件，將其加入sprite群組
    player = Player.Player(WIDTH, HEIGHT, all_sprites)
    all_sprites.add(player)
    
    #建立蚊子群組
    mosquitos = pg.sprite.Group()
    #利用迴圈呼叫Mosquito.py中的函式添加新的物件
    for i in range(25):
        Mosquito.newMosquito(WIDTH, HEIGHT, all_sprites, mosquitos)
                
    #遊戲開始，停止初始音樂，並載入遊戲音樂(蚊子聲)
    pg.mixer.music.stop()
    sound_a.mos_sound()
    
    #遊玩回圈
    while not show_init:
        #1秒內最多執行x次裡面的數字也稱作(FPS)
        #若不限制fps蚊子會集體爆衝，不要輕易嘗試
        clock.tick(FPS)
        
        #取得輸入(右上關閉、esc關閉、p暫停)
        for event in pg.event.get():
            if event.type == pg.QUIT :
                running = False
                break
            elif event.type ==pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    break
                elif event.key == pg.K_SPACE and not paused:
                     player.shoot()
                elif event.key == pg.K_p:  
                     paused = not paused  # 切換暫停狀態
                     
        #右上關閉或ESC會將running設為False，並結束遊戲回圈            
        if not running:
            break
        # 只有在未暫停的情況下才更新遊戲狀態
        if paused:
            Draw.paused(screen) #繪製暫停資訊
            continue

        #更新sprite物件
        all_sprites.update()
            
        # 背景滾動邏輯(圖片往左移動，當移出畫面時，將畫面重設到右側)
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
        
        if bg_x1 <= -WIDTH:
            bg_x1 = WIDTH
        if bg_x2 <= -WIDTH:
            bg_x2 = WIDTH
                
        #用sprite中的函式groupcollide()來判斷子彈與蚊子有無碰撞
        #判斷兩個群組中的物件碰撞後是否消失，True or False
        #此函式會回傳一個字典，{mosquito:bottle, ..., ...}
        #預設是使用矩形碰撞判斷，若改為圓形，雖然判斷較精準，但需要較多計算故較慢
        #在最後加上pg.sprite.collide_circle改為圓形判定，然後需要給player與mosquitos一個半徑的屬性參數
        hits = pg.sprite.groupcollide(mosquitos,player.bottles,True,True)
        #由於碰撞後會消失，所以必須再添加新的物件進去
        for hit in hits:
            score += hit.radius
            B = Boom.Boom(hit.rect.center,'b')
            all_sprites.add(B)
            Mosquito.newMosquito(WIDTH, HEIGHT, all_sprites, mosquitos)
            sound_a.died()
        #分數達200的倍數，蚊子會瞬間加速
        if score == 200 * speed_increased:
            for mosquito in mosquitos:
                mosquito.add_speed(boss) 
            speed_increased+=1
            boss+=3
            
        #判斷完加與蚊子的碰撞
        hits = pg.sprite.spritecollide(player, mosquitos, True, pg.sprite.collide_circle)
        for hit in hits:
            Mosquito.newMosquito(WIDTH, HEIGHT, all_sprites, mosquitos)
            player.health -= 35
            if player.health <=0:
                B = Boom.Boom(hit.rect.center,'b')
                all_sprites.add(B)
                sound_a.p_die()
                player.lifes -= 1
                player.health = 100
                #player中的函式將死亡時暫時隱藏在畫面外
                player.hide(WIDTH, HEIGHT)
        
        #生命歸0，將end設為True，進入結束畫面循環
        if player.lifes == 0 :
            end = True
            pg.mixer.music.stop() #停止蚊子聲
            sound_a.back_sound()  #重新載入背景音樂

            while end:
                Draw.draw_end(screen)
                Draw.draw_clear(screen, "總分為:%d分" %(score), clear_borad_text_size, textx,100)
                Draw.draw_clear(screen, "共消滅:%d隻蚊子" %(int(score/20)), 50, textx,170)
                if score < 800:
                    Draw.draw_clear(screen, "下次會更好", clear_borad_text_size, textx,texty)
                elif score >= 800 and score <= 1600:
                    Draw.draw_clear(screen, "感謝你對睡眠的貢獻", 50, clear_borad_text_size,texty)
                elif score > 1600 and score < 2400:
                    Draw.draw_clear(screen, "你真是太棒了!", 50, clear_borad_text_size,texty)
                elif score >= 2400 and score < 3000:
                    Draw.draw_clear(screen, "你簡直是滅蚊專家!!!", 50, clear_borad_text_size,texty)
                elif score >= 3000 and score < 4000:
                    Draw.draw_clear(screen, "蚊子看到你就嚇死了!!!", 50, clear_borad_text_size,texty)
                else:
                    Draw.draw_clear(screen, "你真的很討厭蚊子...", 50, clear_borad_text_size,texty)
                Draw.draw_clear(screen, "Enter回主畫面，Esc離開遊戲", 35, 70,320)
                pg.display.update()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT :
                        running = False
                        end = False
                        break
                    elif event.type ==pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            running = False
                            end = False
                            break
                        elif event.key == pg.K_RETURN: #Enter鍵
                            end = False
                             
                if not running:
                    break                     
            
            #重設end,show_init，回到初始回圈
            end = True
            show_init = True
        # 顯示背景畫面
        screen.blit(background_img, (bg_x1, 0))
        screen.blit(background_img, (bg_x2, 0))
        # 將sprites物件畫到screen上
        all_sprites.draw(screen)
        # 畫出分數
        Draw.draw_text(screen, "SCORE:"+str(score), 25, WIDTH/2, 20)
        # 畫出血量表
        Draw.draw_health(screen, player.health, 20, 30)
        # 畫出生命
        Draw.draw_lifes(screen, player.lifes, lifes_img, 650, 20)
        # 更新畫面
        pg.display.update() 
pg.quit()
