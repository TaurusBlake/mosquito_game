import pygame as pg
import os

class Bottle(pg.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        # 讀取圖片
        bullet_img = pg.image.load(os.path.join("img","bullet.png"))
        self.image = bullet_img
        # 修改大小
        self.image = pg.transform.scale(bullet_img, (40,30))
        # 插入圖片前做的測試方塊
        # self.image = pg.Surface((20,10))
        # self.image.fill((0,0,255))
        #取得矩形範圍
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
        self.speed = 10
        
        
    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 1000:
            self.kill()