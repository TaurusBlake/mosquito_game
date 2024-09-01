import pygame as pg
import os
import random

def mos_sound():
    pg.mixer.music.load(os.path.join("sound", "mosquito_voice1.mp3"))
    pg.mixer.music.set_volume(1.2)
    pg.mixer.music.play(-1)
    
def back_sound():
    pg.mixer.music.load(os.path.join("sound", "clear.mp3"))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1)
    
def died():
    die0 = pg.mixer.Sound(os.path.join("sound", "die0.mp3"))
    die0.set_volume(0.4)
    die2 = pg.mixer.Sound(os.path.join("sound", "die2.mp3"))
    die2.set_volume(0.4)
    died_sounds = [die0,die2]
    random.choice(died_sounds).play()

def p_die():
    p_die = pg.mixer.Sound(os.path.join("sound", "die1.mp3"))
    p_die.set_volume(0.5)
    p_die.play()
    
def click():
    click = pg.mixer.Sound(os.path.join("sound","click.mp3"))
    click.set_volume(1.5)
    click.play()
    
def shoot_sound():
    shoot_sound = pg.mixer.Sound(os.path.join("sound","shoot.mp3"))
    shoot_sound.set_volume(0.1)
    shoot_sound.play()