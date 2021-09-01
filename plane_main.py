# _*_coding:utf-8_*_
# Author:薄凉
# Time:2021/8/11 13:19
import pygame
from plane_sprites import *
class PlaneGame(object):
    '''飞机大战主游戏'''
    def __init__(self):
        print('游戏初始化')
        #创建游戏主窗口
        self.screen=pygame.display.set_mode(SCREEN_RECT.size)
        #创建游戏时钟
        self.clock=pygame.time.Clock()
        #创建私有方法，用于精灵精灵组
        self.__create_sprites()
        #创建敌机设置敌机定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        #创建英雄子弹定时器事件
        pygame.time.set_timer(HERO_FIRE_EVENT,500)
    def __create_sprites(self):
        #创建背景精灵和精灵组
        bg1=BackGround()
        bg2 = BackGround(True)
        bg2.rect.y=-bg2.rect.height
        self.back_group=pygame.sprite.Group(bg1,bg2)

        #创建敌机精灵组
        self.enemy_group=pygame.sprite.Group()
        #创建英雄精灵和精灵组
        self.hero=Hero()
        self.hero_group=pygame.sprite.Group(self.hero)


    def start_game(self):
        print('游戏开始')
        while True:
            #设置刷新频率
            self.clock.tick(FRAME_CLOCK)
            #事件监听
            self.__event_handle()
            #碰撞检测
            self.__check_collide()
            #更新精灵、精灵组
            self.__update_sprites()
            #更新显示
            pygame.display.update()
    def __event_handle(self):
        event_list=pygame.event.get()
        for event in event_list:
            if event.type==pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type==CREATE_ENEMY_EVENT:
                # print('敌机出场')
                #创建敌机精灵
                enemy=Enemy()
                #将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type==HERO_FIRE_EVENT:
                self.hero.Fire()
            # elif event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
            #     print('向右移动...')
        #使用键盘提供的方法获取按键  元组
        key_press=pygame.key.get_pressed()
        #判断元组中按键索引是不是 1
        if key_press[pygame.K_RIGHT]:
            self.hero.speed=2
        elif key_press[pygame.K_LEFT]:
            self.hero.speed=-2
        else:
            self.hero.speed=0
        # elif key_press[pygame.K_UP]:
        #     self.hero.speed = -2
        # elif key_press[pygame.K_DOWN]:
        #     self.hero.speed = 2
    def __check_collide(self):
        #子弹击毁敌机
        pygame.sprite.groupcollide(self.enemy_group,self.hero.bullets_group,True,True)
        #敌机撞毁英雄
        enemies=pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemies)>0:
            self.hero.kill()
            print('英雄光荣了')
            PlaneGame.__game_over()
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets_group.update()
        self.hero.bullets_group.draw(self.screen)
    @staticmethod
    def __game_over():
        print('游戏结束')
        pygame.quit()
        exit()
if __name__ == '__main__':
    #创建游戏对象
    game=PlaneGame()
    #启动游戏
    game.start_game()