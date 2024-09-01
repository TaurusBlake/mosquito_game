import pygame as pg
import os
from Bottle import Bottle
import sound_a

# image用來顯示圖片rect用來定位
class Player(pg.sprite.Sprite):
    
    def __init__(self, width, height, all_sprites):
        super().__init__()
        player_img = pg.image.load(os.path.join("img", "bottle.png"))
        self.image = player_img
        self.image = pg.transform.scale(player_img, (60,60))
        # 插入圖片前製作的測試方塊
        # self.image = pg.Surface((50,40))
        # self.image.fill((255,0,0))
        self.rect = self.image.get_rect() #取得矩形區域
        self.radius =  20 #取得半徑
        # 檢測圓型區域
        # pg.draw.circle(self.image, (0,0,255), self.rect.center, self.radius)
        self.rect.centery = height / 2
        self.rect.left = width *0.05
        self.speed = 7 #移動速度
        # 儲存視窗尺寸，讓其他函式使用
        self.height = height
        self.width = width
        
        # 建立all_sprites物件
        self.all_sprites = all_sprites
        # 創建子彈群組
        self.bottles = pg.sprite.Group()
        self.health = 100   # 設定血量初值
        self.lifes = 3      # 設定生命初值
        self.hidden = False #物件是否隱藏，預設False
        self.hide_time = 0  #設定隱藏時間，初值為0
        # 记录初始位置
        self.initial_position = (self.rect.left, self.rect.centery)
        
    def update(self):
        now = pg.time.get_ticks() #取得現在時間
        # 隱藏時間超過1秒，重新顯示
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centery = self.height / 2
            self.rect.left = self.width *0.05
            
        #隱藏時不調用鍵盤方法
        if self.hidden:
          return
        
         #控制player移動
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_RIGHT]:
             self.rect.x += self.speed
        if key_pressed[pg.K_LEFT]:
             self.rect.x -= self.speed
        if key_pressed[pg.K_UP]:
             self.rect.y -= self.speed
        if key_pressed[pg.K_DOWN]:
             self.rect.y += self.speed

            
        #判斷是否超出畫面
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
    
    # 射擊函式
    def shoot(self):
        #不是隱藏狀態才可執行
        if not (self.hidden):
            sound_a.shoot_sound() #呼叫函式添加音效
            #添加子彈並加入sprite群組
            bottle = Bottle(self.rect.right, self.rect.top)
            self.all_sprites.add(bottle)
            self.bottles.add(bottle)
        
    # 隱藏player函式
    def hide(self,width,height):
        self.hidden = True
        #將隱藏的時間記下來
        self.hide_time = pg.time.get_ticks()
        #將player定位到畫面之外，當作隱藏
        self.rect.center = (-500,height/2)