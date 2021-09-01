# _*_coding:utf-8_*_
# Author:薄凉
# Time:2021/8/11 2:38
import random
import pygame
#设置屏幕大小
SCREEN_RECT=pygame.Rect(0,0,480,700)
#刷新帧率
FRAME_CLOCK=60
#创建敌机定时器常量
CREATE_ENEMY_EVENT=pygame.USEREVENT
#创建英雄发射子弹定时器常量
HERO_FIRE_EVENT=pygame.USEREVENT+1
class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''
    def __init__(self,img_name,speed=1):
        #调用父类的初始化方法
        super().__init__()
        #定义对象属性
        self.image=pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        self.speed=speed
    def update(self, *args, **kwargs):
        #让战机在垂直方向移动
        self.rect.y+=self.speed

class BackGround(GameSprite):
    '''游戏背景精灵'''
    def __init__(self,is_alt=False):
        super().__init__('./images/background.png')
        #判断图像是否交替
        if is_alt:
            self.rect.y=-self.rect.height
    def update(self, *args, **kwargs):
        #调用父类方法实现
        super().update()
        # 判断是否超出屏幕，如果超出就把图像移到屏幕上方
        if self.rect.y>SCREEN_RECT.height:
            self.rect.y=-self.rect.height

class Enemy(GameSprite):
    '''敌机精灵'''
    def __init__(self):
        # 调用父类方法，创建敌机精灵，指定敌机图片
        super().__init__('./images/enemy1.png')
        #随机指定敌机速度
        self.speed=random.randint(1,3)
        #随机指定敌机初始位置
        self.rect.bottom=0
        random_x=SCREEN_RECT.width-self.rect.width
        self.rect.x=random.randint(0,random_x)
    def update(self, *args, **kwargs):
        #调用父类方法，让敌机垂直运动
        super().update()
        #判断敌机是否飞出屏幕，如果飞出则从精灵组删除敌机
        if self.rect.y>=SCREEN_RECT.height:
            # print('敌机飞出屏幕')
            #kill()当敌机飞出屏幕是调用，将敌机从精灵组中删除并销毁
            self.kill()
    def __del__(self):
        # print('敌机销毁的坐标 %s'%self.rect)
        pass

class Hero(GameSprite):
    def __init__(self):
        #调用父类方法，改写英雄img/speed
        super().__init__('./images/me1.png',0)
        #设置英雄的初始位置
        self.rect.centerx=SCREEN_RECT.centerx
        self.rect.centery=SCREEN_RECT.bottom-120

        #创建子弹的精灵组
        self.bullets_group=pygame.sprite.Group()
    def update(self, *args, **kwargs):
        #设置英雄在水平位置移动
        self.rect.x+=self.speed
        #控制英雄不能离开屏幕
        if self.rect.x<0:
            self.rect.x=0
        #right=y+width
        elif self.rect.right>SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
    def Fire(self):
        # print('发射子弹')
        for i in range(3):
            #创建子弹精灵组
            bullet=Bullet()
            #设置子弹精灵位置
            bullet.rect.bottom=self.rect.y-i*20
            bullet.rect.centerx=self.rect.centerx
            #将子弹精灵添加到精灵组
            self.bullets_group.add(bullet)

class Bullet(GameSprite):
    '''子弹精灵'''
    def __init__(self):
        #调用父类方法 设置子弹 img/speed
        super().__init__('./images/bullet1.png',-2)
    def update(self):
        #设置子弹垂直运动
        super().update()
        #判断子弹是否离开屏幕,离开就销毁
        if self.rect.bottom<0:
            self.kill()
    def __del__(self):
        # print('子弹被销毁')
        pass