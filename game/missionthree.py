# -*- coding: utf-8 -*-
from direct.stdpy import threading
from direct.stdpy.threading import currentThread
from pandac.PandaModules import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import sys, os, math
from math import pi, sin, cos, atan, acos
from direct.actor.Actor import Actor
from resourcemanager.GoodsManager import GoodsManager
from bag import Goods
from direct.gui.DirectFrame import DirectFrame
from password import Password
from password import Boxpassword
from password import Epassword
from chessboard import ChessboardDemo
from role.enemy import Enemylevel3


class MissionThree(object):
    def __init__(self, p, m):
        """

        :type p: Player
        """
        self.menu = m
        self.player = p
        self.memoryNum = 0
        self.password = None
        self.passwordExit = None
        self.boxPassword = None
        self.boxWrongTimes = 0
        self.hallPassword = None
        self.bookIndex = 0
        # self.manager = GoodsManager()
        self.manager = self.player.goodmanager
        self.tutorialText = range(10)
        self.plotText = [[0] * 10] * 10
        self.memoryText = [[] for i in range(10)]
        self.kuraText = range(10)
        self.initTutorial()
        self.initPlot()
        self.initMemory()
        self.initKuraMessage()
        self.manager.GoodsIta['labdoor_box'].state = 'unlockedClose'
        # self.manager.GoodsIta['labdoor_box'].state = 'unlockedClose'
        # self.manager.GoodsIta['chessdoor_box'].state = 'unlockedClose'
        self.hiddenState = False
        self.chessBoard = ChessboardDemo(self)
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])

    def initTutorial(self):
        self.tutorialText[0] = ""
        self.tutorialText[1] = "被Erosion感染的人存在侵蚀度这个概念。侵蚀度越高你的身体机能也就越强，\n" \
                               "但是一定不要为了力量而盲目提升侵蚀度，因为你的侵蚀度达到100%之后意识" \
                               "就会立刻消亡，成为Erosion病毒的傀儡。"
        self.tutorialText[2] = "如果真的需要力量的话，可以发动技能入魔，通过提升侵蚀度的代价短暂提升\n" \
                               "自身的速度，同时随着侵蚀度上升可以做一些平时力量达不到的事情。但是一\n" \
                               "定给我不要滥用啊，不然的话就去死吧，笨蛋。系统提示：按下Space发动入魔。"
        self.tutorialText[3] = "你终于想起来一些事情了呢~这个房间中有好多能让你找回记忆的东西。找到\n" \
                               "那些东西，也是拯救我们的办法呢。系统提示：在侵蚀度高于50%时你会有破坏\n" \
                               "东西的冲动和焦虑感，可能会影响剧情的发展。"
        self.tutorialText[4] = "我们这种被Erosion寄生的人呢，在危险的时候会有一种直觉，这种直觉会让\n" \
                               "你在遭遇危险时听到自己的心跳声。说来，为什么我的心跳这么剧烈呢…"
        self.tutorialText[5] = "在遇到无法通过的障碍时，使用侵蚀之门可以在空间中制造通道从而进行穿梭。\n" \
                               "我先在这里制造一扇给你示范一下，看好了哦。系统提示：按下鼠标右键可以\n" \
                               "向前方发射侵蚀之门，如果场景中存在两个侵蚀之门即可互相穿梭。"
        self.menu.nextButton['command'] = self.hideTutorial
        self.menu.nextButton['extraArgs'] = []

    def initPlot(self):
        self.plotText[0][0] = "终于醒了啊。估计你也想不起来过去的事情了，那我就重新介绍一下自己吧"
        self.plotText[0][1] = "我叫Kura。当时有一群人冲向我们，你给自己注射了Erosion，\n然后杀掉了那些人呢。"
        self.plotText[0][2] = "那些…人？Kura？不行，我还是想不起来……。"
        self.plotText[0][3] = "只有你知道治疗Erosion的办法，所以能从病毒中拯救我们的…也就只有你了。\n" \
                              "因为我被感染的时间比较长，所以只能保持清醒状态很短时间…务必要从这里逃\n" \
                              "出去然后找到解药，不然我们恐怕都要迷失在这里了…我会在这里等你的。"
        self.plotText[1] = "刚一踏出房间，房间的门就被重重的锁上了。无论我怎么叫喊，里面都没有回应。" \
                           "我尽可能不去想最糟糕的情况，大概kura不会有什么问题的吧。"

    def initMemory(self):
        pass
        '''
        编号1 钥匙
        '''
        self.memoryText[1].append("原来——属于我记忆的钥匙，在这里。")
        self.memoryText[1].append("我的生活，我的女儿，我的研究。")
        self.memoryText[1].append("这就是我的实验室啊……这个五芒星堂，正是我一切灵感的起始。")
        self.memoryText[1].append("那个棋局…原来我执的根本不是黑子。")
        self.memoryText[1].append("我是那个被步步紧逼的，愚蠢的白王……\n"
                                  "看着Erosion从萌芽，成长，直到最后被其吞噬……")
        self.memoryText[1].append("Kura啊，你就是我的女儿吧。\n"
                                  "不知被Erosion控制的你，还能不能记得你的父亲……")
        self.memoryText[1].append("Erosion……作为你最大的对手，我承认你很强。\n"
                                  "知己知彼，我对你的了解，还是太少了啊……")
        self.memoryText[1].append("但是，我还不能承认…我已经输了，我要从这个早已不属于我的实验室——")
        self.memoryText[1].append("逃！出！去！")

        '''
        编号2 记忆的回影
        '''
        self.memoryText[2].append("相册上这些实验体…似曾相识的感觉呢……")
        self.memoryText[2].append("这份研究结论我也见过……为什么呢……")
        self.memoryText[2].append("实验体被Erosion所侵蚀之后意识会逐渐被吞噬……\n"
                                  "Erosion结附在实验体上，夺去实验体的意识。")
        self.memoryText[2].append("而这些失去意识的实验体脸上挂着笑容，大概是本我还活在海市蜃楼中吧。")

        '''
        编号3 食人书
        '''
        self.memoryText[3].append("食人书么…这本书为什么我如此眼熟呢…")
        self.memoryText[3].append("对了，这是我给女儿小时候买的画集…我原来也在这个实验室工作过么……")
        self.memoryText[3].append("当时实验失败之后的食人书居然没有被完全销毁…\n"
                                  "是谁把这本书放回书架上了呢…")
        self.memoryText[3].append("算了，不去想了，还有很多东西等着我去探索……")

        '''
        编号4 熟识的地点
        '''
        self.memoryText[4].append("什么？！这个地点…我曾经来过。")
        self.memoryText[4].append("这两个几乎完全相同的实验室…正是我曾经每天待着的地方……")
        self.memoryText[4].append("为什么我会……有这么强的即视感呢？")
        self.memoryText[4].append("那些大大的培养槽中的人，都还活着！他们本我的意识\n"
                                "已经在幻境中沉沉睡去，大概是已经变成Erosion控制的傀儡……")
        self.memoryText[4].append("这个实验的实验者是谁？为什么要研究这些傀儡呢？")

        '''
        编号5 过去的残影
        '''
        self.memoryText[5].append("这个合影……我依稀记得这是我和女儿一起照的……感觉……记忆在涌上来")
        self.memoryText[5].append("她应该也在这个实验室中……在不久之前她被一些实验体咬伤了\n……不行，"
                                "我一定要活着出去，并且找到她……")
        self.memoryText[5].append("说起来kura，你长的真的很像我的女儿呢。可是你为什么会在这里呢？\n")
        self.memoryText[5].append("是吗？那你就把我当成你的女儿呗，爸爸。")
        self.memoryText[5].append("……")
        self.memoryText[5].append("当然是开玩笑的啦，嘻嘻。我也不知道我为什么在这里，我只知道我也\n"
                                "被Erosion感染了。不管这些，你一定要逃出去哦，无论是为了为了你\n"
                                "的女儿亦或是你自己，或者说……为了我？")
        self.memoryText[5].append("嗯，一定。")

        '''
        编号6 持有其他四个记忆碎片触发
        '''
        self.memoryText[6].append("原来——属于我记忆的钥匙，在这里。")
        self.memoryText[6].append("我的生活，我的女儿，我的研究。")
        self.memoryText[6].append("这就是我的实验室啊……这个五芒星堂，正是我一切灵感的起始。")
        self.memoryText[6].append("然而，已经没有时间给我犹豫了，因为对Erosion的研究，还没有中止。")
        self.memoryText[6].append("我记得我之前研究过解除病毒的配方……只是材料还不够而已")
        self.memoryText[6].append("神啊，拜托了，再给我更多的时间吧…让我从这里出去的话…还能救…")

        '''
        编号7 持有其他两个记忆碎片触发
        '''
        self.memoryText[7].append("这个心形的钥匙…是什么呢？")
        self.memoryText[7].append("我似乎有点印象，这是我家里的钥匙吧……")
        self.memoryText[7].append("为什么它会在这里呢…不管了，先带上再说吧。")

        '''
        编号7 持有其他两个记忆碎片触发
        '''
        self.memoryText[8].append("虽然地上是有个钥匙，不过看起来很旧，也没有什么用了呢。")

    def initKuraMessage(self):
        self.kuraText[0] = "呜……真是的…干嘛突然用\n手电筒照我呀，好刺眼的……"
        self.kuraText[1] = "……呜…又来…恶作剧也要有\n个限度呀………人家也是会生气的哦…"
        self.kuraText[2] = "…不是说过了么…恶作剧什么的，要有个…限度呢。\n...\n去死吧你这可恶的人类！"
        self.kuraText[3] = "我记得那边有个八音盒哦。\n这个发条应该和那个八音盒有关"

    def interactiveWith(self, goods):
        self.player.walksound.stop()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.goods = goods
        if goods.Name == "elebutton_box":
            self.menu.selectDialog.show()
            if goods.state == "":
                self.menu.textLabel['text'] = "随着一声轻响，电梯缓缓地打开了。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ['随着一声轻响，电梯缓缓地打开了。', goods, 'opened', ['openElevator']]
                self.menu.aButton['text'] = "走出电梯"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "没必要再回去了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "notebook1_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这个世界上存在着*大罪，分别是嫉妒，暴食，\n傲慢，色欲，贪婪，怠惰，还有暴怒。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "notebook2_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "用数字指代方向是一直以来人们常用的方法。\n比如说用8代表上，6代表右，2代表下。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "notebook3_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "你听说过食人书的故事嘛？屋子里有一本食人书，食人书在书架上的时候,\n" \
                                          "因为被其他的书本顶住，所以不会咬人。但当你将其抽出的时候——应对食人书的方法，\n" \
                                          "就是将其书架两边的书抽出来，然后迅速往上泼水。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "book_studyroom_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "墙上的标语只有一个是真的。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "biaoyu1_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "名字为C++开头的是食人书。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "biaoyu2_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "书架上根本没有食人书。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "biaoyu3_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《死印》不是食人书。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "book_chessroom_box":
            self.menu.selectDialog.show()
            if self.player.EROSION < 80:
                self.menu.textLabel['text'] = "魔术师和魔女们联手讨伐残暴无道的国王。\n" \
                                              "愚王之城堡陷落于无尽的五芒之中。\n" \
                                              "在布满灰尘的西洋棋中——宣告将军。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            elif self.goods.state == "":
                self.menu.textLabel['text'] = "书中似乎有一张残页。"
                self.menu.aButton['command'] = self.showPiece
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "labdoor_box":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "实验室门上现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭实验室门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "实验室门上现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开实验室门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "这扇现在打不开。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "studydoor_box":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "书房门上现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭书房门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "书房门上现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开书房门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "这扇门现在打不开。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "chessdoor_box":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "象棋房门现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭象棋房门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "象棋房门上现在没有上锁。"
                self.menu.aButton['command'] = self.openDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开象棋房门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "这扇门现在打不开。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "exit_box":
            if self.goods.state == "":
                self.menu.selectDialog.show()
                self.menu.textLabel['text'] = "这扇门现在打不开。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.end('trueEnd')
        elif goods.Name == "midpillar_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "起点：E2"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "key_box":
            self.menu.selectDialog.show()
            if self.goods.state == "":
                if self.hiddenState:
                    self.menu.textLabel['text'] = "地上似乎有一把钥匙?"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["获得记忆碎片Ⅰ", goods, "searched", ['roomKey'], 1]
                    self.menu.aButton['text'] = "捡起钥匙"
                    self.menu.bButton.hide()
                if self.memoryNum == 0:
                    self.menu.textLabel['text'] = "虽然地上是有个钥匙，不过看起来很旧，也没有什么用了呢。"
                    self.menu.aButton['command'] = self.doNothing
                    self.menu.aButton['extraArgs'] = []
                    self.menu.aButton['text'] = "离开"
                    self.menu.bButton.hide()
                elif self.memoryNum < 4:
                    self.menu.textLabel['text'] = "这个心形的钥匙…是什么呢？\n" \
                                                  "我似乎有点印象，这是我家里的钥匙吧……\n" \
                                                  "为什么它会在这里呢…不管了，先带上再说吧。"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["获得钥匙", goods, "searched", ['roomKey']]
                    self.menu.aButton['text'] = "离开"
                    self.menu.bButton.hide()
                else:
                    self.menu.textLabel['text'] = "地上似乎有一把钥匙?"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["获得记忆碎片Ⅰ", goods, "searched", ['roomKey'], 6]
                    self.menu.aButton['text'] = "捡起钥匙"
                    self.menu.bButton.hide()
            elif self.goods.state == "searched":
                self.menu.textLabel['text'] = "这里没什么东西。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "这里似乎什么都没发现。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "chessdesk_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "死亡的国际象棋。你执黑子。移动棋子时请慎重，错误的移动会招致死亡。"
            self.menu.aButton['command'] = self.showChessBoard
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "确定"
            self.menu.bButton.hide()
        elif goods.Name == "pool_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "实验室的水池，里面满是很脏的水。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "emptybottle_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "桌子上有个小瓶子。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得空瓶子*1", goods, "picked", ["bottle_empty"]]
            self.menu.aButton['text'] = "拿走瓶子"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "biaoyu_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这个实验室已经被废弃了。正确的一手——即将主教向*的方向移动一步。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "zitiao_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "在国际象棋中，纵向的格子一般用ABCDEFGH来表示，横向的格子则\n" \
                                          "用12345678表示。每一个格都用直线的字母和横线的数字结合起来\n" \
                                          "表示，字母在前，数字在后。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "paints_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "画上写着 五芒星：BD EB HD BH HH"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "bookshelf_box":
            self.menu.selectDialog.show()
            if self.goods.state == '':
                self.menu.textLabel['text'] = "你想要抽出哪一本书呢？"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["GameOver", goods, "", None, "endG"]
                self.menu.aButton['text'] = "《如何把马画成骆驼》"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["《C++从入门到放弃》被抽出", goods, "stage1"]
                self.menu.bButton['text'] = "《C++从入门到放弃》"
                self.menu.cButton['command'] = self.showInfo
                self.menu.cButton['extraArgs'] = ["《死印》被抽出", goods, "stage2"]
                self.menu.cButton['text'] = "《死印》"
                self.menu.cButton.show()
            elif self.goods.state == 'stage1':
                self.menu.textLabel['text'] = "你想要抽出哪一本书呢？"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["GameOver", goods, "", None, "endG"]
                self.menu.aButton['text'] = "《如何把马画成骆驼》"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["《死印》被抽出", goods, "stage3", ['countDown5']]
                self.menu.bButton['text'] = "《死印》"
            elif self.goods.state == 'stage2':
                self.menu.textLabel['text'] = "你想要抽出哪一本书呢？"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["GameOver", goods, "", None, "endG"]
                self.menu.aButton['text'] = "《如何把马画成骆驼》"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["《C++从入门到放弃》被抽出", goods, "stage3", ['countDown5']]
                self.menu.bButton['text'] = "《C++从入门到放弃》"
            else:
                self.menu.textLabel['text'] = "书架里只是一些没用的书。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "vaccine1_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "地上有支抑制剂。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得抑制剂*1", goods, "picked", ["injection"]]
            self.menu.aButton['text'] = "拿走抑制剂"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "vaccine2_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "地上有支抑制剂。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得抑制剂*1", goods, "picked", ["injection"]]
            self.menu.aButton['text'] = "拿走抑制剂"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "vaccine_studyroom_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "地上有支抑制剂。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得抑制剂*1", goods, "picked", ["injection"]]
            self.menu.aButton['text'] = "拿走抑制剂"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        else:
            self.resume()

    def showPiece(self):
        self.menu.endBackground.setImage('res/end/piece.png')
        self.menu.endPictureFrame.show()
        self.menu.endBackground.setTransparency(TransparencyAttrib.MAlpha)
        self.menu.selectDialog.hide()
        base.accept('mouse1', self.removePiece)
        base.accept('b', self.menu.nothing)
        base.accept('escape', self.removePiece)

    def removePiece(self):
        self.menu.endPictureFrame.hide()
        self.menu.endBackground.setTransparency(TransparencyAttrib.MNone)
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
        base.accept('b', self.player.game.openBag)
        base.accept('escape', self.player.game.pauseGame)
        self.showEnemy()

    def showEnemy(self):
        self.menu.game.enemy = Enemylevel3(self.player)
        self.resume()
        self.player.initTask()
        self.hiddenState = True
        self.manager.GoodsIta['chessdoor_box'].state = ''
        self.manager.GoodsIta['chessdoor_box'].CloseDoor()

    def showChessBoard(self):
        base.accept("mouse1", self.chessBoard.grabPiece)  # left-click grabs a piece
        base.accept("mouse1-up", self.chessBoard.releasePiece)  # releasing places
        self.menu.selectDialog.hide()
        self.chessBoard.show()

    def openDoor(self):
        self.goods.Interactive = False
        if self.goods.state == 'unlockedOpen':
            self.goods.state = 'unlockedClose'
            self.goods.CloseDoor()
        else:
            self.goods.state = 'unlockedOpen'
            self.goods.OpenDoor()
        self.resume()
        self.player.initTask()

    def openElevatorTask(self, task):
        # if task.time < 1.3:
        # print self.manager.GoodsIta['leftdianti_box'].Node.getY()
        if self.manager.staticGoods['leftdianti_box'].Node.getY() > -65:
            self.manager.staticGoods['leftdianti_box'].Node.setY(self.manager.staticGoods['leftdianti_box'].Node.getY() - 1.2)
            self.manager.staticGoods['rightdianti_box'].Node.setY(self.manager.staticGoods['rightdianti_box'].Node.getY() + 1.2)
            # print self.manager.staticGoods['leftdianti_box'].Node.getY()
            return task.cont
        return task.done

    def openElevator(self):
        taskMgr.add(self.openElevatorTask, 'openElevatorTask')

    def countDown5(self, task):
        if task.time >= 5:
            if self.manager.GoodsIta['bookshelf_box'].state == 'stage3':
                self.showInfo('你被《如何把马画成骆驼》咬了一口，侵蚀度+25。\n'
                              '书中一页纸条掉了下来，上面写着：\n'
                              '将我移动至C3，礼拜堂即可打开。', self.player.goodmanager.GoodsIta['bookshelf_box'],
                              'timeout', None, None, 25)
                self.menu.infoDialog.hide()
                self.menu.tipDialog.show()
                self.menu.tipLabel['text'] = '你被《如何把马画成骆驼》咬了一口，侵蚀度+25。\n' \
                                             '书中一页纸条掉了下来，上面写着：\n' \
                                             '将我移动至C3，礼拜堂即可打开。'
                taskMgr.add(self.fadeTipsTask, 'fadeTipsTask')
            return task.done
        return task.cont

    def doNothing(self):
        self.resume()
        self.player.initTask()

    def showTutorial(self, tutorialIndex):
        self.menu.selectDialog.hide()
        self.menu.tutorialDialog.show()
        self.menu.nextButton['text'] = self.tutorialText[tutorialIndex]

    def hideTutorial(self):
        self.menu.bButton.show()
        self.menu.selectDialog.hide()
        self.menu.tutorialDialog.hide()
        self.skip()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        self.player.initTask()

    def hideOcanio(self):
        self.menu.tutorialDialog.hide()
        self.menu.ocanioDialog.hide()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        self.player.initTask()

    def showInfo(self, info, goods, state, items=None, index=None, addErosion=None):
        taskMgr.remove("fadeTask")
        self.menu.infoDialog.show()
        goods.state = state
        self.menu.infoLabel['text'] = info
        if items is not None:
            for item in items:
                if item == "openElevator":
                    self.openElevator()
                elif item == "countDown5":
                    taskMgr.add(self.countDown5, 'countDown5')
                elif item == "injection":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.injection, "抑制剂"))
                    self.player.goodmanager.GoodsIta[self.goods.Name].Node.hide()
                    self.player.goodmanager.UnLoad(self.goods.Name)
                elif item == "bottle":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.bottle, "一个装满水的瓶子"))
                    self.player.bag.removeItem('bottle_empty')
                elif item == "bottle_empty":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.emptyBottle, "一个空瓶子"))
                    self.player.goodmanager.GoodsIta[self.goods.Name].Node.hide()
                    self.player.goodmanager.UnLoad(self.goods.Name)
                elif item == "roomKey":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.goldenKey, "一把钥匙"))
                else:
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.panda, "这是啥？"))
        if index is not None:
            if index == 3:
                self.memoryNum += 1
                self.beginMemory(0, 3)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 4:
                self.memoryNum += 1
                self.beginMemory(0, 4)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 1:
                self.memoryNum += 1
                self.beginMemory(0, 1)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 2:
                self.memoryNum += 1
                self.beginMemory(0, 2)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 5:
                self.memoryNum += 1
                self.beginMemory(0)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == "endC" or index == "endD" or str(index).startswith('end'):
                self.end(index)
            else:
                self.showTutorial(index)
                self.skip()
        else:
            self.resume()
            self.player.initTask()
        if addErosion is not None:
            if self.player.EROSION + addErosion < 0:
                self.player.EROSION = 0
            elif self.player.EROSION + addErosion > 100:
                self.player.EROSION = 100
            else:
                self.player.EROSION += addErosion

    def beginMemory(self, index, memIndex = None):
        print 'index, memIndex', index, memIndex
        if memIndex is not None:
            if memIndex == 2 or memIndex == 3:
                if index < 3:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.beginMemory
                    self.menu.ocanioButton['extraArgs'] = [index + 1, memIndex]
                else:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.hideOcanio
                    self.menu.ocanioButton['extraArgs'] = []
            elif memIndex == 4:
                if index < 4:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.beginMemory
                    self.menu.ocanioButton['extraArgs'] = [index + 1, memIndex]
                else:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.hideOcanio
                    self.menu.ocanioButton['extraArgs'] = []
            elif memIndex == 1:
                if index < 8:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.beginMemory
                    self.menu.ocanioButton['extraArgs'] = [index + 1, memIndex]
                else:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    self.menu.ocanioButton['text'] = self.memoryText[memIndex][index]
                    self.menu.ocanioButton['command'] = self.hideOcanio
                    self.menu.ocanioButton['extraArgs'] = []
        else:
            if index < 3 or index == 4:
                self.menu.tutorialDialog.hide()
                self.menu.ocanioDialog.show()
                self.menu.ocanioButton['text'] = self.memoryText[5][index]
                self.menu.ocanioButton['command'] = self.beginMemory
                self.menu.ocanioButton['extraArgs'] = [index + 1]
            elif index == 3 or index == 5:
                self.menu.tutorialDialog.show()
                self.menu.ocanioDialog.hide()
                self.menu.nextButton['text'] = self.memoryText[5][index]
                self.menu.nextButton['command'] = self.beginMemory
                self.menu.nextButton['extraArgs'] = [index + 1]
            elif index == 6:
                self.menu.tutorialDialog.hide()
                self.menu.ocanioDialog.show()
                self.menu.ocanioButton['text'] = self.memoryText[5][index]
                self.menu.ocanioButton['command'] = self.hideOcanio
                self.menu.ocanioButton['extraArgs'] = []

    def aCommand(self):
        self.resume()
        self.player.initTask()

    def bCommand(self):
        self.menu.infoDialog.show()
        self.menu.infoLabel['text'] = "get something!"
        self.resume()
        self.player.initTask()

    def skip(self):
        taskMgr.add(self.fadeTask, "fadeTask")

    def fadeTask(self, task):
        if task.time < 3.0:
            return task.cont
        self.menu.infoDialog.hide()
        return task.done

    def fadeTipsTask(self, task):
        if task.time < 5.0:
            return task.cont
        self.menu.tipDialog.hide()
        return task.done

    def resume(self):
        self.menu.bButton.show()
        self.menu.cButton.hide()
        self.menu.selectDialog.hide()
        # self.menu.tutorialDialog.hide()
        self.skip()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)

    def end(self, fun="endB"):
        self.endFun = fun
        self.menu.tutorialDialog.hide()
        self.menu.selectDialog.hide()
        taskMgr.add(self.fadeEnd, "fadeEnd")

    def fadeEnd(self, task):
        if task.time < 1.0:
            self.menu.passFrame['frameColor'] = (0, 0, 0, task.time)
            return task.cont
        self.menu.passFrame.hide()
        self.menu.infoDialog.hide()
        if self.endFun == "endA":
            self.endA()
            self.showEndPicture('deadend_text.png')
        elif self.endFun == "end1":
            self.end1()
            self.showEndPicture('deadend_text.png')
        elif self.endFun == "endB":
            self.endB()
            self.showEndPicture('end_text.png')
        elif self.endFun == "endC":
            self.endC()
            self.showEndPicture('deadend+_text.png')
        elif self.endFun == "endD":
            self.endD()
        elif self.endFun == "endE":
            self.endE()
        elif self.endFun == "endF":
            self.endF()
        elif self.endFun == "endG":
            self.endG()
            self.showEndPicture('deadend3_text.png')
        elif self.endFun == "hiddenEnd":
            self.hiddenEnd()
            self.showEndPicture('hiddenend_text.png')
        elif self.endFun == "trueEnd":
            self.trueEnd()
            return task.done
        else:
            return task.done
        # self.menu.endPictureFrame.doMethodLater(10, self.removeEndPicture, 'removeEndPicture')
        self.menu.mainFrame.hide()
        base.accept('mouse1-up', self.removeEndPicture)
        return task.done

    def removeEndPicture(self):
        self.menu.endPictureFrame.hide()
        self.menu.mainFrame.show()

    def endA(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.infoLabel['text'] = "Erosion max!"
        self.menu.infoDialog.hide()
        self.skip()

    def endB(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = "Kura被你吓死了！"
        self.menu.infoDialog.hide()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.tutorialDialog.hide()
        self.skip()

    def endC(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = '谁动了我的蛋糕?'
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.tutorialDialog.hide()
        self.skip()

    def endD(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = '活该'
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.tutorialDialog.hide()
        self.skip()

    def endE(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = '活该'
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.tutorialDialog.hide()
        self.skip()

    def endF(self):
        self.resume()
        self.player.initTask()

    def endG(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = '书不能乱读'
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.tutorialDialog.hide()
        self.skip()

    def end1(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = "Erosion max!"
        self.menu.infoDialog.hide()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.skip()

    def hiddenEnd(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.menu.mainFrame.show()
        self.menu.infoLabel['text'] = "既然已经知道棋局的真相，为何还要\n" \
                                      "进行无谓的挣扎——你还没意识到那被\n" \
                                      "将死的白王——是谁么。"
        self.menu.infoDialog.show()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.skip()

    def trueEnd(self):
        self.player.mouseIconNormal.show()
        self.player.mouseIconWatch.hide()
        self.player.isInteractive = False
        self.playPostVideo()

    def playPostVideo(self):
        media_file = "res/videos/postVideo.avi"
        self.tex = MovieTexture("postVideo")
        success = self.tex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("postVideo Card")
        # cm.setFrameFullscreenQuad()
        cm.setFrame(-1.3, 1.3, -1, 1)

        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.tex)
        self.card = NodePath(cm.generate())
        self.card.reparentTo(base.render2d)
        self.card.setTexture(self.tex)
        self.videoSound = loader.loadSfx(media_file)
        self.tex.synchronizeTo(self.videoSound)
        self.videoSound.play()

        taskMgr.add(self.playPostGameVideo, 'playPostGameVideo')

    def playPostGameVideo(self, task):
        if self.videoSound.status() != AudioSound.PLAYING:
            self.videoSound.stop()
            self.card.hide()
            # self.menu.soundMgr.playMusic('bgm1.mp3')
            self.menu.passFrame.hide()
            self.player.erosionFrame.hide()
            self.player.currentItemFrame.hide()
            # self.menu.mainFrame.show()
            if self.memoryNum >= 5:
                self.showEndPicture('trueend_text.png')
            else:
                self.showEndPicture('end_text.png')
            return task.done
        return task.cont

    def showEndPicture(self, pic):
        self.menu.endBackground.setImage('res/end/' +  pic)
        self.menu.endPictureFrame.show()
        base.accept('mouse1-up', self.removeEndPicture)
        # self.menu.endPictureFrame.doMethodLater(10, self.removeEndPicture, 'removeEndPicture')

    def playEnd(self):
        self.removeGame()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.player.shoot.TwoBullet[0].Disappera()
        self.player.shoot.TwoBullet[1].Disappera()
        self.menu.selectedSave = 3
        self.menu.tempPlayer = self.player
        self.menu.loadSave()

    def removeGame(self):
        '''
        释放内存
        '''
        names = ['elebutton_box', 'notebook1_box', 'notebook2_box', 'notebook3_box', 'book_studyroom_box', 'biaoyu1_box', 'biaoyu2_box',
                 'biaoyu3_box', 'book_chessroom_box', 'labdoor_box', 'studydoor_box', 'chessdoor_box', 'exit_box', 'midpillar_box',
                 'chessdesk_box', 'pool_box', 'emptybottle_box', 'biaoyu_box', 'zitiao_box', 'paints_box', 'bookshelf_box',
                 'vaccine1_box', 'vaccine2_box', 'vaccine_studyroom_box', 'light_box', 'wall', 'floor', 'diantikuang_box', 'zhuozi_box',
                 'king_box', 'rook1_box', 'rook2_box', 'knight_box', 'bishop_box', 'leftdianti_box', 'rightdianti_box', 'desk_box']
        for name in names:
            self.player.goodmanager.UnLoad(name)

    def fadeMove(self, task):
        if task.time < 1.0:
            self.menu.passFrame['frameColor'] = (0, 0, 0, task.time)
            return task.cont
        else:
            self.menu.passFrame.hide()
            self.playEnd()
            return task.done