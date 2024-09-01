import pygame as pg
import os
import random

# 建立蚊子類別並繼承sprite類別，__init__說明見inf.py
class Mosquito(pg.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        mosquito_img1 = pg.image.load(os.path.join("img", "mosquito1.png"))
        mosquito_img2 = pg.image.load(os.path.join("img", "mosquito2.png"))
        
        # 調整圖片大小
        self.images = [
            pg.transform.scale(mosquito_img1, (60, 60)),
            pg.transform.scale(mosquito_img2, (60, 60))
            ]
        
        # 設置初始圖片和動畫幀計數器
        self.image = self.images[0] # 設置初始圖片
        self.current_frame = 0 # 追蹤當前的動畫幀
        self.frame_delay = 4  # 延遲更新次數(更新4次後換下一幀)
        self.frame_counter = 0 # 已更新的幀數
        
        # 插入圖片前先製作方塊測試功能
        # self.image = pg.Surface((30,40))
        # self.image.fill((0,255,0)) 
        self.rect = self.image.get_rect() #取得矩形區域
        self.radius = 20    #取得半徑
        #檢測圓型區域
        # pg.draw.circle(self.images[0], (0,0,255), self.rect.center, self.radius)
        self.rect.x = random.randrange(width+40,width+100) #隨機產生x與y座標值
        self.rect.y = random.randrange(-100, height +100)
        
        # 設定垂直與水平移動(亂數生成讓每個物件隨機速度)
        self.speedx = random.randrange(2,8)
        self.speedy = random.randrange(-2,2)
        
        # 儲存視窗尺寸，讓其他函式使用
        self.width = width
        self.height = height
        
    def update(self):
        # 遊戲是讓蚊子往左移動，x座標用減法
        # 垂直方向本身有負值，y座標直接使用加法
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        
        # 切換圖片以實現動畫效果
        self.frame_counter += 1 # 每次循環+1
        if self.frame_counter >= self.frame_delay: # 滿足更新次數
            self.frame_counter = 0  #將值重設為0
            self.current_frame = 1 - self.current_frame #只有兩個畫面，在0-1間切換
            # self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        # 當蚊子跑出畫面時，重新生成蚊子
        if self.rect.top > self.height or self.rect.bottom < 0 or self.rect.right < 0:
            self.rect.x = random.randrange(self.width+40, self.width+100)
            self.rect.y = random.randrange(0, self.height - self.rect.height)
            self.speedx = random.randrange(2,8)
            self.speedy = random.randrange(-2,2)
    # 徒然增加速度
    def add_speed(self, amount):
        self.speedx += amount        
        
# 建立添加蚊子函式
def newMosquito(width, height, all_sprites,mosquitos):
    mosquito = Mosquito(width, height)
    all_sprites.add(mosquito)
    mosquitos.add(mosquito)