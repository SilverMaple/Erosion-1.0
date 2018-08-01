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


class MissionTwo(object):
    def __init__(self, p, m):
        """

        :type p: Player
        """
        self.menu = m
        self.player = p
        self.memoryNum = 0
        self.copperState = True
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
        self.inFlowerNum = 1
        self.outFlowerNum = 6
        self.checkState = False
        taskMgr.add(self.checkFlowerNum, "checkFlowerNum")
        # self.manager.GoodsIta['outdoor_box'].OpenDoor()
        # self.manager.GoodsIta['Backdoor'].OpenDoor()
        # self.manager.GoodsIta['Frontdoor'].state = 'closed'
        # self.manager.GoodsIta['Backdoor'].state = 'closed'

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
        编号2 记忆的回影
        '''
        # self.memoryText[2][0] = "相册上这些实验体…似曾相识的感觉呢……"
        # self.memoryText[2][1] = "这份研究结论我也见过……为什么呢……"
        # self.memoryText[2][2] = "实验体被Erosion所侵蚀之后意识会逐渐被吞噬……\n" \
        #                         "Erosion结附在实验体上，夺去实验体的意识。"
        # self.memoryText[2][3] = "而这些失去意识的实验体脸上挂着笑容，大概是本我还活在海市蜃楼中吧。"
        self.memoryText[2].append("日记上记述的这些实验体…似曾相识的感觉呢……")
        self.memoryText[2].append("这份研究结论我也见过……为什么呢……")
        self.memoryText[2].append("实验体被Erosion所侵蚀之后意识会逐渐被吞噬……\n"
                                  "Erosion结附在实验体上，夺去实验体的意识。")
        self.memoryText[2].append("而这些失去意识的实验体脸上挂着笑容，大概是本我还活在海市蜃楼中吧。")

        '''
        编号4 熟识的地点
        '''
        # self.memoryText[4][0] = "什么？！这个地点…我曾经来过。"
        # self.memoryText[4][1] = "这两个几乎完全相同的实验室…正是我曾经每天待着的地方……"
        # self.memoryText[4][2] = "为什么我会……有这么强的即视感呢？"
        # self.memoryText[4][3] = "那些大大的培养槽中的人，都还活着！他们本我的意识\n" \
        #                         "已经在幻境中沉沉睡去，大概是已经变成Erosion控制的傀儡……"
        # self.memoryText[4][4] = "这个实验的实验者是谁？为什么要研究这些傀儡呢？"
        self.memoryText[4].append("什么？！这个地点…我曾经来过。")
        self.memoryText[4].append("这两个几乎完全相同的实验室…正是我曾经每天待着的地方……")
        self.memoryText[4].append("为什么我会……有这么强的即视感呢？")
        self.memoryText[4].append("那些大大的培养槽中的人，都还活着！他们本我的意识\n"
                                "已经在幻境中沉沉睡去，大概是已经变成Erosion控制的傀儡……")
        self.memoryText[4].append("这个实验的实验者是谁？为什么要研究这些傀儡呢？")

        '''
        编号5 过去的残影
        '''
        # self.memoryText[5][0] = "这个合影……我依稀记得这是我和女儿一起照的……感觉……记忆在涌上来"
        # self.memoryText[5][1] = "她应该也在这个实验室中……在不久之前她被一些实验体咬伤了\n……不行，" \
        #                         "我一定要活着出去，并且找到她……"
        # self.memoryText[5][2] = "说起来kura，你长的真的很像我的女儿呢。可是你为什么会在这里呢？\n"
        # self.memoryText[5][3] = "是吗？那你就把我当成你的女儿呗，爸爸。"
        # self.memoryText[5][4] = "……"
        # self.memoryText[5][5] = "当然是开玩笑的啦，嘻嘻。我也不知道我为什么在这里，我只知道我也\n" \
        #                         "被Erosion感染了。不管这些，你一定要逃出去哦，无论是为了为了你\n" \
        #                         "的女儿亦或是你自己，或者说……为了我？"
        # self.memoryText[5][6] = "嗯，一定。"
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
        if goods.Name == "dianti_box":
            self.menu.selectDialog.show()
            if goods.state == "ready":
                self.menu.textLabel['text'] = "随着一声轻响，电梯缓缓地打开了。"
                self.menu.aButton['command'] = self.enterElevator
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "走进电梯"
                self.menu.bButton.hide()
            # elif self.player.bag.haveItem("res/models/items/" + "hammer" + ".png") \
            #         and goods.state == "cracked":
            #     self.menu.textLabel['text'] = "无论怎么按动按钮，电梯都没有反应。\n" \
            #                                   "电梯门已经残破不堪了，似乎可以强行打开的样子。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你愤怒的抄起锤子砸向有一点裂缝的电梯门。\n"
            #                                       "电梯间的门被砸开了。然而里面却没有电梯，\n"
            #                                       "等待着你的是……", goods, "smashed", None, 'endC', None]
            #     self.menu.aButton['text'] = "用锤子砸"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "暂时离开"
            # elif self.player.bag.haveItem("res/models/items/" + "hammer" + ".png")\
            #         and goods.state == "":
            #     self.menu.textLabel['text'] = "无论怎么按动按钮，电梯都没有反应。\n" \
            #                                   "电梯门已经残破不堪了，似乎可以强行打开的样子。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你愤怒的抄起锤子砸向电梯门。\n门似乎被砸出了一点缝隙。", goods, "smashed", ["torch", "groupPhoto"], 3, -15]
            #     self.menu.aButton['text'] = "用锤子砸"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "暂时离开"
            else:
                self.menu.textLabel['text'] = "无论怎么按动按钮，电梯都没有反应。\n" \
                                              "电梯门已经残破不堪了，似乎可以强行打开的样子。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "暂时离开"
                self.menu.bButton.hide()
        elif goods.Name == "broken_dianti_box":
            self.menu.selectDialog.show()
            if goods.state == "ready":
                self.menu.textLabel['text'] = "随着一声轻响，电梯缓缓地打开了。"
                self.menu.aButton['command'] = self.enterElevator
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "走进电梯"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "无论怎么按动按钮，电梯都没有反应。\n" \
                                              "电梯门已经残破不堪了，似乎可以强行打开的样子。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "暂时离开"
                self.menu.bButton.hide()
        elif goods.Name == "ElectricBox":
            self.menu.selectDialog.show()
            if goods.state == "opened":
                self.menu.textLabel['text'] = "这个配电盒已经被打开了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            elif goods.state == "smashed":
                self.menu.textLabel['text'] = "这个配电盒已经被砸开了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            # elif self.player.bag.haveItem("res/models/items/" + "goldenKey" + ".png") and \
            #         self.player.bag.haveItem("res/models/items/" + "hammer" + ".png"):
            #     self.menu.textLabel['text'] = "配电盒被紧紧锁着，没有钥匙的话似乎打不开。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["配电盒的锁被打开了。你拉下了电闸，\n"
            #                                       "看到电梯的按钮亮了起来。", goods, "opened"]
            #     self.menu.aButton['text'] = "用钥匙打开"
            #     self.menu.bButton['command'] = self.showInfo
            #     self.menu.bButton['extraArgs'] = ["你砸开了配电盒，此时从配电盒里\n"
            #                                       "传来巨大电流，你被电成了焦炭。", goods, "", None, "endD", None]
            #     self.menu.bButton['text'] = "用锤子砸"
            # elif self.player.bag.haveItem("res/models/items/" + "hammer" + ".png"):
            #     self.menu.textLabel['text'] = "配电盒被紧紧锁着，没有钥匙的话似乎打不开。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你砸开了配电盒，此时从配电盒里\n"
            #                                       "传来巨大电流，你被电成了焦炭。", goods, "", None, "endD", None]
            #     self.menu.aButton['text'] = "用锤子砸"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "暂时离开"
            # elif self.player.bag.haveItem("res/models/items/" + "goldenKey" + ".png"):
            #     self.menu.textLabel['text'] = "配电盒被紧紧锁着，没有钥匙的话似乎打不开。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["配电盒的锁被打开了。你拉下了电闸，\n"
            #                                       "看到电梯的按钮亮了起来。", goods, "opened", None, "endD", None]
            #     self.menu.aButton['text'] = "用钥匙打开"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "暂时离开"
            else:
                self.menu.textLabel['text'] = "配电盒被紧紧锁着，没有钥匙的话似乎打不开。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "暂时离开"
                self.menu.bButton.hide()
        elif goods.Name == "clock_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这个钟显示的时间……有点奇怪呢。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "entrance_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这扇门已经被从里面反锁了。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "暂时离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_1":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《不要动我的蛋糕》\n" \
                                          "似乎还有一行小字\n" \
                                          "这些画是穿插在这一层中的解谜关键。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_2":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《死兔》"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_3":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《破碎的镜》"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_4":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《沾血的房间》\n画的旁边还有一行小字：获取一个颜色寓意的最简单方法，就是将其连线的两边相加。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_5":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《数学题》\n画上内容：x=???? ????=ti:me"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_6":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《正与反的恒常》"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_7":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《夕阳》\n说来在房间里的时候，kura告诉我现在是中午，不知道还有多久太阳会下山呢。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_8":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《花》"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "painting_9":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "《希望》\n" \
                                          "似乎还有一行小字\n" \
                                          "“password=hua*hua+X hua≠hua。”"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "diary_box":
            self.menu.selectDialog.show()
            if self.player.EROSION <= 50 and self.goods.state == "":
                self.menu.textLabel['text'] = "这是一本日记。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得记忆碎片Ⅱ", goods, "searched", None, 2]
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            elif self.goods.state == "searched":
                self.menu.textLabel['text'] = "这本日记已经查看过了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "因为意识混乱，日记上的字迹模糊不清，难以调查。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "Frontdoor":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "大厅门上现在没有上锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭大厅门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "大厅门上现在没有上锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开大厅门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "门上存在一个电子锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "输入密码"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["这个密码到底是什么呢……", goods, ""]
                self.menu.bButton['text'] = "暂时离开"
        elif goods.Name == "Backdoor":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "大厅门上现在没有上锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭大厅门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "大厅门上现在没有上锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开大厅门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "门上存在一个电子锁。"
                self.menu.aButton['command'] = self.openHallDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "输入密码"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["这个密码到底是什么呢……", goods, ""]
                self.menu.bButton['text'] = "暂时离开"
        elif goods.Name == "outdoor_box":
            self.menu.selectDialog.show()
            if goods.state == "" or goods.state == "rabbit":
                self.menu.textLabel['text'] = "这个门似乎可以推开，但总感觉里面阴森森的，有种不祥的气息。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["里面有窸窸窣窣的声音，不知道是什么\n"
                                                  "东西在里面，但是好像很可怕。", goods, ""]
                self.menu.aButton['text'] = "趴在门上听"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["你面前出现了...", goods, "", None, "endD", None]
                self.menu.bButton['text'] = "推开门"
            elif goods.state == "unlockedCloseFirst":
                self.menu.textLabel['text'] = "这个门似乎可以推开。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["里面有窸窸窣窣的声音，但是声音距离你很远。", goods, "unlockedCloseFirst"]
                self.menu.aButton['text'] = "趴在门上听"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["门被打开了。", goods, "unlockedClose", ["openLabDoor"]]
                self.menu.bButton['text'] = "推开门"
            elif goods.state == 'unlockedClose':
                self.menu.textLabel['text'] = "实验门内外现在好像没什么危险。"
                self.menu.aButton['command'] = self.openLabDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开实验室门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "实验门内外现在好像没什么危险。"
                self.menu.aButton['command'] = self.openLabDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭实验室门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            # elif self.player.bag.haveItem("res/models/items/" + "deadRabbit" + ".png"):
            #     self.menu.textLabel['text'] = "这个门似乎可以推开，但总感觉里面阴森森的，有种不祥的气息。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你将死兔放在门口，之后躲在大厅门旁暗中观察。\n"
            #                                       "这时，一只血红色的手抓住了兔子，将其拉入了门内。\n"
            #                                       "不久，门内传来哀嚎声。", goods, "deadRabbit"]
            #     self.menu.aButton['text'] = "投放死兔"
            #     self.menu.bButton['command'] = self.showInfo
            #     self.menu.bButton['extraArgs'] = ["你面前出现了...", goods, "", None, "endE", None]
            #     self.menu.bButton['text'] = "推开门"
            #     self.menu.bButton.hide()
            # elif self.player.bag.haveItem("res/models/items/" + "rabbit" + ".png"):
            #     self.menu.textLabel['text'] = "这个门似乎可以推开，但总感觉里面阴森森的，有种不祥的气息。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你将实验兔放在门口，之后躲在大厅门旁暗中观察。\n"
            #                                       "这时，一只血红色的手抓住了兔子，将其拉入了门内。\n"
            #                                       "你似乎听到门内传来“我……还……要”", goods, "rabbit"]
            #     self.menu.aButton['text'] = "投放实验兔"
            #     self.menu.bButton['command'] = self.showInfo
            #     self.menu.bButton['extraArgs'] = ["你面前出现了...", goods, "", None, "endE", None]
            #     self.menu.bButton['text'] = "推开门"
            #     self.menu.bButton.hide()
            # elif self.player.bag.haveItem("res/models/items/" + "hammer" + ".png"):
            #     self.menu.textLabel['text'] = "这个门似乎可以推开，但总感觉里面阴森森的，有种不祥的气息。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你把门敲开了，看到了一群满身血迹的怪物。\n"
            #                                       "这时谁都救不了你了。", goods, "", None, "endE", None]
            #     self.menu.aButton['text'] = "用锤子砸"
            #     self.menu.bButton['command'] = self.showInfo
            #     self.menu.bButton['extraArgs'] = ["你面前出现了...", goods, "", None, "endE", None]
            #     self.menu.bButton['text'] = "推开门"
            #     self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "这个门似乎可以推开，但总感觉里面阴森森的，有种不祥的气息。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "暂时离开"
                self.menu.bButton.hide()
        elif goods.Name == "fridge_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "冰箱中东西不多，仅有几根胡萝卜和一个大蛋糕。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得胡萝卜*1", goods, "searched", ["carrot"]]
            self.menu.aButton['text'] = "拿走胡萝卜"
            self.menu.bButton['command'] = self.showInfo
            self.menu.bButton['extraArgs'] = ["获得大蛋糕*1", goods, "searched", ["cake"]]
            self.menu.bButton['text'] = "拿走大蛋糕"
            if self.player.bag.haveItem('res/models/items/carrot.png'):
                self.menu.aButton['extraArgs'] = ["背包已有胡萝卜", goods, "searched", ["carrot"]]
            if self.player.bag.haveItem('res/models/items/cake.png'):
                self.menu.bButton['extraArgs'] = ["背包已有蛋糕", goods, "searched", ["cake"]]
        elif goods.Name == "food_box":
            self.menu.selectDialog.show()
            # if self.player.bag.haveItem("res/models/items/" + "rabbit_alive" + ".png"):
            #     self.menu.textLabel['text'] = "食物放了太久 早就发霉了。看起来像是煮好的胡萝卜。\n“还是不要去尝了吧，不然会死人的”"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["实验兔吃下了发霉的食物，蹬了一下腿就一动不动了。\n"
            #                                       "获得死兔", goods, "eaten", ["rabbit_dead"]]
            #     self.menu.aButton['text'] = "使用实验兔"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "离开"
            # else:
            self.menu.textLabel['text'] = "食物放了太久 早就发霉了。看起来像是煮好的胡萝卜。\n“还是不要去尝了吧，不然会死人的”"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "暂时离开"
            self.menu.bButton.hide()
        elif goods.Name == "safe_box":
            self.menu.selectDialog.show()
            if self.goods.state == "unlocked":
                self.menu.textLabel['text'] = "保险柜里面什么都没有。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "保险柜上面似乎有一个密码锁。"
                self.menu.aButton['command'] = self.openSafe
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "输入密码"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["这个密码到底是什么呢……", goods, ""]
                self.menu.bButton['text'] = "暂时离开"
        elif goods.Name == "rabbit_cage":
            self.menu.selectDialog.show()
            # if self.player.bag.haveItem("res/models/items/" + "carrot" + ".png"):
            #     self.menu.textLabel['text'] = "实验室的实验兔笼。里面的兔子似乎因为没有食物而显得很躁动。\n" \
            #                                   "伸了伸手，发现似乎够不着兔子。"
            #     self.menu.aButton['command'] = self.showInfo
            #     self.menu.aButton['extraArgs'] = ["你使用胡萝卜引诱兔子出来，抓出了一只兔子。\n"
            #                                       "获得兔子*1", goods, "", ["rabbit_alive"]]
            #     self.menu.aButton['text'] = "使用胡萝卜"
            #     self.menu.bButton['command'] = self.doNothing
            #     self.menu.bButton['extraArgs'] = []
            #     self.menu.bButton['text'] = "离开"
            # else:
            self.menu.textLabel['text'] = "实验室的实验兔笼。里面的兔子似乎因为没有食物而显得很躁动。\n" \
                                        "伸了伸手，发现似乎够不着兔子。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "暂时离开"
            self.menu.bButton.hide()
        elif goods.Name == "window_box":
            self.menu.selectDialog.show()
            if goods.state == "smashed":
                self.menu.textLabel['text'] = "这个窗户已经被砸开了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "这个窗户似乎通向实验室。透过窗户看了看实验室里面，\n" \
                                              "只看到一片阴影在蠕动。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "window_broken_box":
            self.menu.selectDialog.show()
            if goods.state == "smashed":
                self.menu.textLabel['text'] = "这个窗户已经被砸开了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "这个窗户似乎通向实验室。透过窗户看了看实验室里面，\n" \
                                              "只看到一片阴影在蠕动。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "vaccine_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这里有支抑制剂。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得抑制剂*1", goods, "picked", ["injection"]]
            self.menu.aButton['text'] = "拿起抑制剂"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "hallvaccine_box":
            if goods.state is not "used":
                print 'hallvaccine_box'
                self.menu.selectDialog.show()
                self.menu.textLabel['text'] = "这里有支抑制剂。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得抑制剂*1", goods, "picked", ["injection"]]
                self.menu.aButton['text'] = "拿起抑制剂"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
        elif goods.Name == "knife_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这里有把裁纸刀。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得裁纸刀*1", goods, "picked", ["knife"]]
            self.menu.aButton['text'] = "拿起裁纸刀"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "inknife_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "这里有把裁纸刀。"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得裁纸刀*1", goods, "picked", ["inknife"]]
            self.menu.aButton['text'] = "拿起裁纸刀"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        elif goods.Name == "lavabo_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "硫酸槽中盛满了稀硫酸。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "inlavabo_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "硫酸槽中盛满了稀硫酸。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "biaoyu_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "我们是正与反的恒常，镜子的表与里。\n" \
                                          "将正与反恢复一致，谜题即可解开。\n" \
                                          "当你迷茫如何前进时，不如去走廊摘朵花儿来。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "furnace_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "熊熊燃烧的火炉。你看到周围的灰烬中残留的纸屑写着文字“悲”"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
            # self.menu.aButton['command'] = self.showInfo
            # self.menu.aButton['extraArgs'] = ["你把莎士比亚喜剧集烧掉，火焰变的更旺了", goods, "burned", None, "burnBook", None]
            # self.menu.aButton['text'] = "烧掉喜剧集"
            # self.menu.aButton['command'] = self.showInfo
            # self.menu.aButton['extraArgs'] = ["这时火焰突然跃起。", goods, "burned", None, "burnFunBook", 15]
            # self.menu.aButton['text'] = "烧掉其他书"
        elif goods.Name == "infurnace_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "熊熊燃烧的火炉。你看到周围的灰烬中残留的纸屑写着文字“喜”"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
            # self.menu.aButton['command'] = self.showInfo
            # self.menu.aButton['extraArgs'] = ["你把莎士比亚悲剧集烧掉，火焰变的更旺了", goods, "", None, "burnBook", None]
            # self.menu.aButton['text'] = "烧掉悲剧集"
            # self.menu.aButton['command'] = self.showInfo
            # self.menu.aButton['extraArgs'] = ["这时火焰突然跃起。", goods, "", None, "burnSadBook", 15]
            # self.menu.aButton['text'] = "烧掉其他书"
        elif goods.Name == "mirror_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "显示出一模一样的情景。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "vase_box":
            self.menu.selectDialog.show()
            if self.outFlowerNum > 0:
                self.menu.textLabel['text'] = "花瓶里面有" + str(self.outFlowerNum) + "朵纸花。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得纸花*1", goods, "", ["outflower"]]
                self.menu.aButton['text'] = "拿走一朵"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "花瓶里面现在没有纸花。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "invase_box":
            self.menu.selectDialog.show()
            if self.inFlowerNum > 0:
                self.menu.textLabel['text'] = "花瓶里面有" + str(self.inFlowerNum) + "朵纸花。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得纸花*1", goods, "", ["inflower"]]
                self.menu.aButton['text'] = "拿走一朵"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "花瓶里面现在没有纸花。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "bookshelf_box":
            self.menu.selectDialog.show()
            if self.goods.state == '':
                self.menu.textLabel['text'] = "书架里有：A:《莎士比亚悲剧集》, B:《高等代数分析》"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得《莎士比亚悲剧集》", goods, "searched", ["sadBook"]]
                self.menu.aButton['text'] = "拿走A书"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["为什么抽走书之后…书架后会有人影？", goods, "", None, "endG", None]
                self.menu.bButton['text'] = "拿走B书"
            else:
                self.menu.textLabel['text'] = "书架里只是一些没用的书。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "inbookshelf_box":
            self.menu.selectDialog.show()
            if self.goods.state == '':
                self.menu.textLabel['text'] = "书架里有：A:《莎士比亚喜剧集》, B:《高等代数分析》"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得《莎士比亚喜剧集》", goods, "searched", ["funBook"]]
                self.menu.aButton['text'] = "拿走A书"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["你看到书架后方有一个人影。\n"
                                                  "不对啊…书架明明是在墙角才对……", goods, "", ["gaoshuBook"], "endG", None]
                self.menu.bButton['text'] = "拿走B书"
            else:
                self.menu.textLabel['text'] = "书架里只是一些没用的书。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "hammer_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "桌子上这把锤子是在逗我吗？"
            self.menu.aButton['command'] = self.showInfo
            self.menu.aButton['extraArgs'] = ["获得锤子*1", goods, "picked", ["hammer"]]
            self.menu.aButton['text'] = "拿走锤子"
            self.menu.bButton['command'] = self.doNothing
            self.menu.bButton['extraArgs'] = []
            self.menu.bButton['text'] = "离开"
        else:
            self.resume()

    def checkFlowerNum(self, task):
        if self.inFlowerNum == self.outFlowerNum and self.inFlowerNum == 4:
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
            self.player.endTask()
            if self.manager.GoodsIta['furnace_box'].state == 'burned' and self.player.goodmanager.GoodsIta['infurnace_box'].state == 'burned':
                self.showInfo("花瓶底部机关开启，\n获得锈迹斑斑的铜片,\n获得记忆碎片Ⅴ", self.manager.GoodsIta['furnace_box'],
                              'burned', ['copperplate_rusted'], 4)
                self.showTips("花瓶底部机关开启，\n获得锈迹斑斑的铜片,\n获得记忆碎片Ⅴ")
                self.checkState = True
                return task.done
            else:
                self.showInfo("花瓶底部机关开启，\n获得锈迹斑斑的铜片", self.manager.GoodsIta['furnace_box'], 'burned',
                              ['copperplate_rusted'])
                self.showTips("花瓶底部机关开启，\n获得锈迹斑斑的铜片")
                self.checkState = True
                return task.done
        return task.cont

    def initFlowers(self):
        for i in range(self.inFlowerNum):
            self.player.goodmanager.staticGoods["inflowers" + str(i+1)].Node.show()
            print "inflowers" + str(i+1) + " show"
        for i in range(8-self.inFlowerNum - 1):
            self.player.goodmanager.staticGoods["inflowers" + str(8 - (i + 1))].Node.hide()
            print "inflowers" + str(8 - (i + 1)) + " hide"
        for i in range(self.outFlowerNum):
            self.player.goodmanager.staticGoods["outflowers" + str(i + 1)].Node.show()
            print "outflowers" + str(i + 1) + " show"
        for i in range(8 - self.outFlowerNum - 1):
            self.player.goodmanager.staticGoods["outflowers" + str(8 - (i + 1))].Node.hide()
            print "outflowers" + str(8 - (i + 1)) + " hide"

    def openLabDoor(self):
        if self.goods.state == 'unlockedOpen':
            self.goods.state = 'unlockedClose'
            self.goods.CloseDoor()
        else:
            self.goods.state = 'unlockedOpen'
            self.goods.OpenDoor()
        self.resume()
        self.player.initTask()

    def waitCopper(self, task):
        if self.copperState == True:
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            base.accept("escape", self.player.game.pauseGame)
            self.player.bag.copperFrame.hide()
            self.player.mission.copperState = True
            self.player.initTask()
            return task.done
        return task.cont

    '''
    hall door
    '''
    def openHallDoor(self):
        if self.hallPassword is None:
            self.hallPassword = Epassword()
            self.hallPassword.reloadLeap()
        else:
            self.hallPassword.reloadLeap()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        if self.hallPassword.passState == False:
            self.hallPassword.passwordFrame.show()
        self.menu.selectDialog.hide()
        taskMgr.add(self.waitHallPass, "waitHallPass")
        base.accept('escape', self.waitHallPassReturn)

    def waitHallPass(self, task):
        if self.hallPassword.passState:
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            # self.hallPassword.passwordFrame.hide()
            self.hallPassword.unloadLeap()
            # self.goods.OpenDoor()
            if self.goods.state == "unlockedOpen":
                self.goods.state = "unlockedClose"
                self.goods.CloseDoor()
            elif self.goods.state == "unlockedClose":
                self.goods.state = "unlockedOpen"
                self.goods.OpenDoor()
            else:
                self.goods.state = "unlockedOpen"
                self.goods.OpenDoor()
                if self.goods.Name == "Backdoor":
                    self.manager.GoodsIta['Frontdoor'].state = "unlockedClose"
                else:
                    self.manager.GoodsIta['Backdoor'].state = "unlockedClose"
            self.resume()
            self.player.initTask()
            base.accept('escape', self.player.game.pauseGame)
            return
        if self.hallPassword.wrongTime == 1:
            # self.hallPassword.passwordFrame.hide()
            self.hallPassword.wrongTime = 0
            self.hallPassword.unloadLeap()
            self.showInfo("密码错误，侵蚀度+5", self.goods, "", None, None, 5)
            base.accept('escape', self.player.game.pauseGame)
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            return task.done

        return task.cont

    def waitHallPassReturn(self):
        self.resume()
        self.player.initTask()
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
        base.accept('escape', self.player.game.pauseGame)
        self.hallPassword.passwordFrame.hide()

    '''
    safe box
    '''
    def openSafe(self):
        if self.boxPassword is None:
            self.boxPassword = Boxpassword()
        else:
            self.boxPassword.reloadInput()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.boxPassword.passwordFrame.show()
        self.menu.selectDialog.hide()
        base.accept('b', self.menu.nothing)
        taskMgr.add(self.waitSafePass, "waitSafePass")
        base.accept('escape', self.waitSafePassReturn)

    def waitSafePass(self, task):
        if self.boxPassword.passState:
            self.boxPassword.passwordFrame.hide()
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            # self.boxPassword.unloadLeap()
            self.menu.infoDialog.show()
            self.menu.infoLabel['text'] = '密码锁被打开了，获得一个金属钥匙'
            self.player.bag.addItem(Goods("res/models/items/" + "goldenKey" + ".png",
                                          self.player.bag.goldenKey, "一把钥匙"))
            self.resume()
            self.player.initTask()
            self.goods.state = "unlocked"
            base.accept('b', self.player.game.openBag)
            base.accept('escape', self.player.game.pauseGame)
            return
        if self.boxPassword.wrongTime == 1:
            self.boxPassword.passwordFrame.hide()
            self.boxPassword.wrongTime = 0
            self.boxWrongTimes += 1
            if self.boxWrongTimes < 3:
                self.showInfo("保险柜没有丝毫动静。你觉得这个\n密码不是这么快就能解开的。", self.goods, "")
            elif self.player.bag.haveItem("res/models/items/" + "copperplate_rusted" + ".png") or \
                    self.player.bag.haveItem("res/models/items/" + "copperplate_rusted" + ".png"):
                self.showInfo("似乎只有一个数字没有出现过呢。\n而且那个9的数字…好像只是用来迷惑\n我的，什么线都没有连。侵蚀度+5", self.goods, "", None, None, 5)
            else:
                self.showInfo("似乎还有些线索没有收集到，\n先不要管这个了吧。 侵蚀度+5", self.goods, "", None, None, 5)
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            # self.boxPassword.unloadLeap()
            base.accept('escape', self.player.game.pauseGame)
            return task.done

        return task.cont

    def waitSafePassReturn(self):
        self.resume()
        self.player.initTask()
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
        base.accept('escape', self.player.game.pauseGame)
        base.accept('b', self.player.game.openBag)
        self.boxPassword.passwordFrame.hide()

    '''
    password door
    '''
    def openDoor(self):
        if self.password is None:
            self.password = Password()
            self.password.password = "5387"
        else:
            self.password.reloadLeap()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.password.passwordFrame.show()
        self.menu.selectDialog.hide()
        taskMgr.add(self.waitPass, "waitPass")
        base.accept('escape', self.waitPassReturn)

    def waitPass(self, task):
        if self.password.passState:
            self.password.passwordFrame.hide()
            self.password.unloadLeap()
            self.goods.OnClick()
            if self.goods.state == "unlockedOpen":
                self.goods.state = "unlockedClose"
            else:
                self.goods.state = "unlockedOpen"
            self.resume()
            self.player.initTask()
            base.accept('escape', self.player.game.pauseGame)
            return
        if self.password.wrongTime == 1:
            self.password.passwordFrame.hide()
            self.password.wrongTime = 0
            self.password.unloadLeap()
            self.showInfo("密码错误，侵蚀度+5", self.goods, "", None, None, 5)
            base.accept('escape', self.player.game.pauseGame)
            return task.done

        return task.cont

    def waitPassReturn(self):
        self.resume()
        self.player.initTask()
        base.accept('escape', self.player.game.pauseGame)
        self.password.unloadLeap()
        self.password.passwordFrame.hide()

    def openExitDoor(self):
        if self.passwordExit is None:
            self.passwordExit = Password()
        else:
            self.passwordExit.reloadLeap()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.player.endTask()
        self.passwordExit.passwordFrame.show()
        self.menu.selectDialog.hide()
        taskMgr.add(self.waitExitPass, "waitExitPass")
        base.accept('escape', self.waitExitPassReturn)

    def waitExitPass(self, task):
        if self.passwordExit.passState:
            self.passwordExit.passwordFrame.hide()
            self.passwordExit.unloadLeap()
            self.goods.OnClick()
            if self.goods.state == "unlockedOpen":
                self.goods.state = "unlockedClose"
            else:
                self.goods.state = "unlockedOpen"
            self.resume()
            self.player.initTask()
            base.accept('escape', self.player.game.pauseGame)
            return
        return task.cont

    def waitExitPassReturn(self):
        self.resume()
        self.player.initTask()
        base.accept('escape', self.player.game.pauseGame)
        self.passwordExit.unloadLeap()
        self.passwordExit.passwordFrame.hide()

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

    def startAI(self):
        self.menu.tutorialDialog.hide()
        self.menu.ocanioDialog.hide()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        self.player.initTask()
        self.player.game.enemy.setupAI()

    def showInfo(self, info, goods, state, items=None, index=None, addErosion=None):
        self.menu.infoDialog.show()
        goods.state = state
        self.menu.infoLabel['text'] = info
        if items is not None:
            for item in items:
                if item == "rabbit_alive":
                    self.player.bag.removeItem('carrot')
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.rabbit, "一只实验兔"))
                elif item == "rabbit_dead":
                    self.player.bag.removeItem('rabbit_alive')
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.deadRabbit, "一只死兔"))
                elif item == "copperplate_rusted":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.copperplate_rusted, "锈迹斑斑的铜板"))
                elif item == "copperplate_clean":
                    self.player.bag.removeItem('copperplate_rusted')
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.copperplate_clean, "干净的铜板"))
                elif item == "hammer":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.hammer, "一只锤子"))
                    self.player.goodmanager.GoodsIta['hammer_box'].Node.hide()
                elif item == "injection":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.injection, "抑制剂"))
                    self.player.goodmanager.GoodsIta[self.goods.Name].Node.hide()
                    self.player.goodmanager.UnLoad(self.goods.Name)
                    # print self.goods.Name
                elif item == "goldenKey":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.goldenKey, "一把金色钥匙"))
                elif item == "carrot":
                    if not self.player.bag.haveItem('res/models/items/carrot.png'):
                        self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.carrot, "一根胡萝卜"))
                elif item == "cake":
                    if not self.player.bag.haveItem('res/models/items/cake.png'):
                        self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.cake, "一块大蛋糕"))
                        taskMgr.add( self.deadCake, 'deadCake')
                elif item == "funBook":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.funBook, "《莎士比亚喜剧集》"))
                elif item == "sadBook":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.sadBook, "《莎士比亚悲剧集》"))
                elif item == "gaoshuBook":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.gaoshuBook, "《高等代数分析》"))
                elif item == "knife":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.knife, "一把裁纸刀"))
                    self.player.goodmanager.GoodsIta['knife_box'].Node.hide()
                    self.player.goodmanager.UnLoad(self.goods.Name)
                elif item == "inknife":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.inknife, "一把裁纸刀"))
                    self.player.goodmanager.GoodsIta['inknife_box'].Node.hide()
                    self.player.goodmanager.UnLoad(self.goods.Name)
                elif item == "inflower":
                    self.player.bag.addItem(Goods("res/models/items/" + "flower" + ".png", self.player.bag.flower, "一朵纸花"))
                    self.inFlowerNum -= 1
                    self.player.goodmanager.staticGoods["inflowers" + str(self.inFlowerNum + 1)].Node.hide()
                elif item == "outflower":
                    self.player.bag.addItem(Goods("res/models/items/" + "flower" + ".png", self.player.bag.flower, "一朵纸花"))
                    self.outFlowerNum -= 1
                    self.player.goodmanager.staticGoods["outflowers" + str(self.outFlowerNum + 1)].Node.hide()
                elif item == "setInflower":
                    self.player.bag.removeItem('flower')
                    self.inFlowerNum += 1
                    self.player.goodmanager.staticGoods["inflowers" + str(self.inFlowerNum)].Node.show()
                elif item == "setOutflower":
                    self.player.bag.removeItem('flower')
                    self.outFlowerNum += 1
                    self.player.goodmanager.staticGoods["outflowers" + str(self.outFlowerNum)].Node.show()
                elif item == "cutFlower":
                    self.player.bag.addItem(Goods("res/models/items/" + "flower" + ".png", self.player.bag.flower, "一朵纸花"))
                    self.player.goodmanager.GoodsIta['painting_cut'].Node.show()
                    self.player.goodmanager.GoodsIta['painting_8'].Node.hide()
                elif item == "openLabDoor":
                    self.openLabDoor()
                elif item == "broken_dianti":
                    self.player.goodmanager.GoodsIta['dianti_box'].Node.hide()
                    self.player.goodmanager.UnLoad('dianti_box')
                    self.player.goodmanager.GoodsIta['broken_dianti_box'].Node.show()
                else:
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.panda, "这是啥？"))
        if index is not None:
            if index == 3:
                self.memoryNum += 1
                self.beginMemory(0)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 4:
                self.memoryNum += 1
                self.beginMemory(0, 4)
                self.menu.selectDialog.hide()
                self.skip()
            elif index == 2:
                self.memoryNum += 1
                self.beginMemory(0, 2)
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
            if memIndex == 2:
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
            elif memIndex == 0:
                if index < 1:
                    self.menu.tutorialDialog.hide()
                    self.menu.ocanioDialog.show()
                    props = WindowProperties()
                    props.setCursorHidden(False)
                    base.win.requestProperties(props)
                    self.player.endTask()
                    self.menu.ocanioButton['text'] = '你…你是Kura？'
                    self.menu.ocanioButton['command'] = self.beginMemory
                    self.menu.ocanioButton['extraArgs'] = [index + 1, 0]
                else:
                    self.menu.tutorialDialog.show()
                    self.menu.ocanioDialog.hide()
                    self.menu.nextButton['text'] = '不，我只是皇后大人的棋子。杀掉所有进入这间屋子的人，就是我的使命。'
                    self.menu.nextButton['command'] = self.startAI
                    self.menu.nextButton['extraArgs'] = []
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

    def deadCake(self, task):
        # 持有蛋糕走到走廊触发结局
        # print self.player.node.getPos()
        # print self.player.node.getX()
        if self.player.node.getX() > 372:
            self.end('endC')
            return task.done
        return task.cont

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
        if task.time < 1.0:
            return task.cont
        self.menu.infoDialog.hide()
        return task.done

    def showTips(self, tips):
        self.menu.infoDialog.hide()
        self.menu.tipDialog.show()
        self.menu.tipLabel['text'] = tips
        taskMgr.add(self.fadeTipsTask, 'fadeTipsTask')

    def fadeTipsTask(self, task):
        if task.time < 5.0:
            return task.cont
        self.menu.tipDialog.hide()
        return task.done

    def resume(self):
        self.menu.bButton.show()
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
            return task.done
        elif self.endFun == "endE":
            self.endE()
        elif self.endFun == "endF":
            self.endF()
        elif self.endFun == "endG":
            self.endG()
            self.showEndPicture('deadend2+.png')
        elif self.endFun == "trueEnd":
            self.trueEnd()
            return task.done
        else:
            return task.done
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

    # def endD(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = '活该'
    #     self.menu.infoDialog.hide()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()

    def endD(self):
        self.player.mouseIconNormal.show()
        self.player.mouseIconWatch.hide()
        self.player.isInteractive = False
        self.playPostVideo()

    def playPostVideo(self):
        media_file = "res/videos/xiaren.avi"
        self.tex = MovieTexture("xiarenVideo")
        success = self.tex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("xiarenVideo Card")
        # cm.setFrameFullscreenQuad()
        cm.setFrame(-1, 1, -1, 1)

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
            self.showEndPicture('deadend_text.png')
            return task.done
        return task.cont

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
        self.menu.infoLabel['text'] = '因为你抽走了错误的书本啊。'
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

    def showEndPicture(self, pic):
        self.menu.endBackground.setImage('res/end/' +  pic)
        self.menu.endPictureFrame.show()
        base.accept('mouse1-up', self.removeEndPicture)

    # def fadeEnd(self, task):
    #     if task.time < 1.0:
    #         self.menu.passFrame['frameColor'] = (0, 0, 0, task.time)
    #         return task.cont
    #     self.menu.passFrame.hide()
    #     self.menu.infoDialog.hide()
    #     if self.endFun == "endA":
    #         self.endA()
    #     elif self.endFun == "end1":
    #         self.end1()
    #     elif self.endFun == "endB":
    #         self.endB()
    #     elif self.endFun == "endC":
    #         self.endC()
    #     elif self.endFun == "endD":
    #         self.endD()
    #     elif self.endFun == "endE":
    #         self.endE()
    #     elif self.endFun == "endF":
    #         self.endF()
    #     elif self.endFun == "endG":
    #         self.endG()
    #     return task.done
    #
    # def endA(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.infoLabel['text'] = "Erosion max!"
    #     self.skip()
    #
    # def endB(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = "Kura被你吓死了！"
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()
    #
    # def endC(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = '谁动了我的蛋糕?'
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()
    #
    # def endD(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = '活该'
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()
    #
    # def endE(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = '活该'
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()
    #
    # def endF(self):
    #     self.resume()
    #     self.player.initTask()
    #
    # def endG(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = '书不能乱读'
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.skip()
    #
    # def end1(self):
    #     props = WindowProperties()
    #     props.setCursorHidden(False)
    #     base.win.requestProperties(props)
    #     self.player.endTask()
    #     self.menu.mainFrame.show()
    #     self.menu.infoLabel['text'] = "Erosion max!"
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.skip()

    def enterElevator(self):
        self.player.mouseIconNormal.show()
        self.player.mouseIconWatch.hide()
        self.player.isInteractive = False
        self.player.node.setPos(-250, 265, 0)
        self.menu.passFrame.show()
        taskMgr.add(self.fadeMove, "fadeMove")
        self.resume()

    def moveToLevelThree(self):
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
        names = ['light', 'wall', 'dianti_box', 'dianti_box', 'broken_dianti_box', 'clock_box', 'ElectricBox',
                 'entrance_box',
                 'painting_1', 'painting_2', 'painting_3', 'painting_4', 'painting_5', 'painting_6',
                 'painting_7', 'painting_8', 'painting_9', 'painting_cut', 'outdoor_box', 'food_box', 'cake_box',
                 'diary_box',
                 'safe_box', 'carrot_box', 'window_box', 'window_broken_box', 'biaoyu_box', 'hammer_box', 'rabbit_cage',
                 'hallvaccine_box',
                 'fridge_box', 'rabbit_box', 'yuanzhuo_box', 'changzhuo_box', 'Frontdoor', 'Backdoor', 'vase_box',
                 'knife_box',
                 'jiazi_box', 'rongqi_box', 'vaccine_box', 'lavabo_box', 'mirror_box', 'furnace_box', 'bookshelf_box',
                 'xiaozhuozi_box',
                 'infireish', 'insteam', 'Scene2_book-beijuji', 'Scene2_book-xijuji',
                 'outflowers1', 'outflowers2', 'outflowers3', 'outflowers4', 'outflowers5', 'outflowers6',
                 'outflowers7', 'outflowers8',
                 'inflowers1', 'inflowers2', 'inflowers3', 'inflowers4', 'inflowers5', 'inflowers6', 'inflowers7',
                 'inflowers8',
                 'invase_box', 'inknife_box', 'injiazi_box', 'inlavabo_box',
                 'inrongqi_box', 'infurnace_box', 'inbookshelf_box', 'inxiaozhuozi_box',
                 'fireish', 'steam', 'H2SO4', 'smo', 'surface-1']
        for name in names:
            self.player.goodmanager.UnLoad(name)

    def fadeMove(self, task):
        if task.time < 1.0:
            self.menu.passFrame['frameColor'] = (0, 0, 0, task.time)
            return task.cont
        else:
            self.menu.passFrame.hide()
            self.moveToLevelThree()
            return task.done
