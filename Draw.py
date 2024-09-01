import pygame as pg
import os

font_name = os.path.join("jf.ttf")
# 繪製遊戲中的文字模板
def draw_text(surf, text, size, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)
        
# 繪製通關畫面的文字模板
def draw_clear(surf, text, size, x_pos, y_pos):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x_pos, y_pos)
    surf.blit(text_surface, text_rect)
        
# 製作血條(畫在甚麼平面,剩餘血量,x座標,y座標)
def draw_health(surf, hp, x, y):
    if hp < 0:
       hp = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 15
    #將生命條填滿多少(生命百分比)
    fill = (hp/100)*BAR_LENGTH
    #製作生命條外框，pygame的矩形(x座標,y座標,長,高)
    outline = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    #填滿框
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    pg.draw.rect(surf,(0,255,0),fill_rect)
    pg.draw.rect(surf, (255,255,255), outline,2)
# 製作生命  
def draw_lifes(surf, lifes, img, x, y):
    for i in range(lifes):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i #共3條命，間隔30像素
        img_rect.y = y
        surf.blit(img,img_rect)

# 設計首頁畫面
def draw_init(screen):
    width = screen.get_width()
    height = screen.get_height()
    title_img = pg.image.load(os.path.join("img", "background_title.jpg"))
    title_img = pg.transform.scale(title_img, (width, height))
    screen.blit(title_img,(0,0))

    # 讀取按鈕圖案
    start_img = pg.image.load(os.path.join("img", "start.png"))
    start1_img = pg.image.load(os.path.join("img", "start1.png"))
    inf_img = pg.image.load(os.path.join("img", "inf.png"))
    inf1_img = pg.image.load(os.path.join("img", "inf1.png"))
    exit_img = pg.image.load(os.path.join("img", "exit.png"))
    exit1_img = pg.image.load(os.path.join("img", "exit1.png"))
    # 設置按鈕位置
    start_x = (width -start_img.get_width()) // 2 - 250
    start_y = (height - start_img.get_height())
    start1_x = (width -start1_img.get_width()) // 2 - 250
    start1_y = (height - start1_img.get_height())
    inf_x = (width -inf_img.get_width()) // 2
    inf_y = (height - start_img.get_height())
    inf1_x = (width -inf1_img.get_width()) // 2
    inf1_y = (height - start_img.get_height())
    exit_x = (width -start_img.get_width()) // 2 + 250
    exit_y = (height - start_img.get_height())
    exit1_x = (width -start_img.get_width()) // 2 + 250
    exit1_y = (height - start_img.get_height())
    # 獲取按鈕矩形區域
    start_rect = start_img.get_rect(topleft=(start_x, start_y))
    start1_rect = start1_img.get_rect(topleft=(start1_x, start1_y))
    inf_rect = inf_img.get_rect(topleft=(inf_x, inf_y))
    inf1_rect = inf1_img.get_rect(topleft=(inf1_x, inf1_y))
    exit_rect = exit_img.get_rect(topleft=(exit_x, exit_y))
    exit1_rect = exit1_img.get_rect(topleft=(exit1_x, exit1_y))
    
    # 回傳圖片與按鈕
    return (title_img, start_img, start1_img, start_rect, start1_rect,
            inf_img, inf1_img, inf_rect, inf1_rect,
            exit_img, exit1_img, exit_rect, exit1_rect)

# 暫停功能
def paused(screen):
    width = screen.get_width()
    height = screen.get_height()
    draw_text(screen,"遊戲暫停",74,width/2,height/2) #利用draw_text()繪製
    draw_text(screen,"請按P繼續遊戲，或Esc關閉遊戲",36,width/2,height/2+200)
    pg.display.update() #需要於呼叫時更新畫面
    
# 操作說明頁面
def draw_rule(screen):
    width = screen.get_width()
    height = screen.get_height()
    rule_img = pg.image.load(os.path.join("img", "rule.png"))
    rule_img = pg.transform.scale(rule_img, (width, height))
    #返回按鈕
    back = pg.image.load(os.path.join("img", "back.png"))
    back = pg.transform.scale(back, (100, 100))
    back_x = (width - back.get_width())
    back_y = (height - back.get_height())
    back_rect = back.get_rect(topleft=(back_x, back_y))
    
    back1 = pg.image.load(os.path.join("img", "back1.png"))
    back1 = pg.transform.scale(back1, (100, 100))
    back1_x = (width - back1.get_width())
    back1_y = (height - back1.get_height())
    back1_rect = back1.get_rect(topleft=(back1_x, back1_y))
    #回傳圖片與按鈕
    return back, back_rect, back1, back1_rect,rule_img

#插入結束頁面
def draw_end(screen):
    width = screen.get_width()
    height = screen.get_height()
    end_img = pg.image.load(os.path.join("img", "end.jpg"))
    end_img = pg.transform.scale(end_img, (width, height))
    screen.blit(end_img,(0,0))

    

    