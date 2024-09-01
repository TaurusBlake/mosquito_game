import pygame as pg
import os

B_anim = {}
B_anim['b'] = []

def load_boom():
    for i in range(9):
        B_img = pg.image.load(os.path.join("img",f"B{i}.png"))
        B_anim['b'].append(pg.transform.scale(B_img, (75,75)))

#利用sprite來將image屬性設為爆炸圖片，每次更新切換一張，播完刪除
class Boom(pg.sprite.Sprite):
    B_anim = B_anim
    #要傳入爆炸中心點以及大小
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = B_anim[self.size][0]
        self.rect = self.image.get_rect()
        #圖片進入的中心點
        self.rect.center = center
        #更新到第幾張圖，初始為0
        self.frame = 0
        #紀錄最後一次更新時間，此函式會回傳初始化到現在經過的毫秒數
        self.last_update = pg.time.get_ticks()
        #至少經過幾毫秒才更新下一張圖，因為若照遊戲設計的fps更新速度會太快，所以需要控制更新速度
        #代表50毫秒才更新
        self.frame_rate = 50
        

    def update(self):
        #取得現在時間
        now = pg.time.get_ticks()
        #如果經過時間>更新時間，就更新圖片
        if now - self.last_update > self.frame_rate:
            #將最後時間更新為現在
            self.last_update = now
            #更新圖片
            self.frame +=1
            #判定是否已更新到最後一張
            if self.frame == len(B_anim[self.size]):
                #若更新到最後一張就刪除圖片
                self.kill()
            #否則繼續更新
            else:
                #將圖片更新
                self.image = B_anim[self.size][self.frame]
                #記錄當前中心點
                center = self.rect.center
                #重新取得定位
                self.rect = self.image.get_rect()
                #更新中心點
                self.rect.center = center