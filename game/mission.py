#-*- coding: utf-8 -*-
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
from password import Gpassword

class Mission(object):

    def __init__(self, p, m):
        self.menu = m
        self.player = p
        self.memoryNum = 0
        self.password = None
        self.passwordExit = None
        self.bookIndex = 0
        # self.manager = GoodsManager()
        self.manager = self.player.goodmanager
        self.tutorialText = range(10)
        self.plotText = [[0]*10]*10
        self.memoryText = [[0]*10]*10
        self.kuraText = range(10)
        self.initTutorial()
        self.initPlot()
        self.initMemory()
        self.initKuraMessage()
        self.paperState = True

    def initTutorial(self):
        self.tutorialText[0] = ""
        self.tutorialText[1] = "被Erosion感染的人存在侵蚀度这个概念。侵蚀度越高你的身体机能也就越强，\n" \
                               "但是一定不要为了力量而盲目提升侵蚀度，因为你的侵蚀度达到100%之后意识" \
                               "就会立刻消亡，成为Erosion病毒的傀儡。"
        self.tutorialText[2] = "如果真的需要力量的话，可以发动技能入魔，通过提升侵蚀度的代价短暂提升\n" \
                               "自身的速度，同时随着侵蚀度上升可以做一些平时力量达不到的事情。但是一\n" \
                               "定给我不要滥用啊，不然的话就去死吧，笨蛋。"
        self.tutorialText[3] = "你终于想起来一些事情了呢~这个房间中有好多能让你找回记忆的东西。找到\n" \
                               "那些东西，也是拯救我们的办法呢。"
        self.tutorialText[4] = "我们这种被Erosion寄生的人呢，在危险的时候会有一种直觉，这种直觉会让\n" \
                               "你在遭遇危险时听到自己的心跳声。说来，为什么我的心跳这么剧烈呢…"
        self.tutorialText[5] = "在遇到无法通过的障碍时，使用侵蚀之门可以在空间中制造通道从而进行穿梭。\n" \
                               "我先在这里制造一扇给你示范一下，看好了哦。"
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
        self.memoryText[5][0] = "这个合影……我依稀记得这是我和女儿一起照的……感觉……记忆在涌上来"
        self.memoryText[5][1] = "她应该也在这个实验室中……在不久之前她被一些实验体咬伤了\n……不行，" \
                                "我一定要活着出去，并且找到她……"
        self.memoryText[5][2] = "说起来kura，你长的真的很像我的女儿呢。可是你为什么会在这里呢？\n"
        self.memoryText[5][3] = "是吗？那你就把我当成你的女儿呗，爸爸。"
        self.memoryText[5][4] = "……"
        self.memoryText[5][5] = "当然是开玩笑的啦，我也不知道我为什么在这里，我只知道我也\n" \
                                "被Erosion感染了。不管这些，你一定要逃出去哦，无论是为了你\n" \
                                "的女儿亦或是你自己，或者说……为了我？"
        self.memoryText[5][6] = "嗯，一定。"

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
        if goods.Name == "box":
            self.menu.selectDialog.show()
            if goods.state == "smashed":
                self.menu.textLabel['text'] = "这个箱子已经被砸碎了，没必要再去探索了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            elif goods.state == "moved":
                if self.player.EROSION >= 50:
                    self.menu.textLabel['text'] = "你无法控制暴怒，砸坏了箱子。"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["箱子中掉出了一张合影。", goods, "smashed", ["groupPhoto"], 3, -15]
                    self.menu.aButton['text'] = "查看箱子"
                    self.menu.bButton.hide()
                else:
                    self.menu.textLabel['text'] = "这个箱子背后已经没有什么可以探索的了。"
                    self.menu.aButton['command'] = self.doNothing
                    self.menu.aButton['extraArgs'] = []
                    self.menu.aButton['text'] = "离开"
                    self.menu.bButton.hide()
            else:
                if self.player.EROSION < 5:
                    self.menu.textLabel['text'] = "这个箱子太重了，我推不动它。\n可能我还需要更强的力量。"
                    self.menu.aButton['command'] = self.showTutorial
                    self.menu.aButton['extraArgs'] = [2]
                    self.menu.aButton['text'] = "暂时离开"
                    self.menu.bButton.hide()
                elif self.player.EROSION <50:
                    self.menu.textLabel['text'] = "看起来很重的箱子，\n是否要搬开看看？"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["从箱子的后面发现了一个手电筒，\n似乎还有着一点电量。", goods, "moved", ["torch"]]
                    self.menu.aButton['text'] = "搬开"
                    self.menu.bButton['command'] = self.doNothing
                    self.menu.bButton['extraArgs'] = []
                    self.menu.bButton['text'] = "不搬开"
                else:
                    self.menu.textLabel['text'] = "你无法控制暴怒，砸坏了箱子。"
                    self.menu.aButton['command'] = self.showInfo
                    self.menu.aButton['extraArgs'] = ["箱子中掉出了一张合影，并且\n"
                                                      "从箱子的后面发现了一个手电筒，\n"
                                                      "似乎还有着一点电量。", goods, "smashed", ["torch", "groupPhoto"], 3, -15]
                    self.menu.aButton['text'] = "查看箱子"
                    self.menu.bButton.hide()
        elif goods.Name == "yaoshui":
            self.menu.selectDialog.show()
            if goods.state == "":
                self.showTutorial(4)
                self.menu.nextButton['command'] = self.hideTutorial
                self.menu.nextButton['extraArgs'] = []
                goods.state = "skipTutorial"
            if goods.state == "shined":
                self.menu.textLabel['text'] = "这瓶蓝色药水没什么用了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                # if self.player.bag.haveItem("res/models/items/" + "torch" + ".png"):
                #     self.menu.textLabel['text'] = "桌子上怎么有瓶蓝色药水？"
                #     self.menu.aButton['command'] = self.showInfo
                #     self.menu.aButton['extraArgs'] = ["不对…头好晕…这药水有毒！ ", goods, "drinked", None, None, 100]
                #     self.menu.aButton['text'] = "喝一口"
                #     self.menu.bButton['command'] = self.changWord
                #     self.menu.bButton['extraArgs'] = ["后方墙上的一些文字在光芒照射下\n变成了蓝色。手电筒电量耗尽了。", goods, "shined"]
                #     self.menu.bButton['text'] = "用手电筒照一下."
                # else:
                self.menu.textLabel['text'] = "桌子上怎么有瓶蓝色药水？"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["不对…头好晕…这药水有毒！", goods, "drinked", None, None, 100]
                self.menu.aButton['text'] = "喝一口"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "放弃"
        elif goods.Name == "toilet_door":
            self.menu.selectDialog.show()
            if self.player.EROSION >= 50 and self.goods.state == "":
                self.menu.textLabel['text'] = "你的焦虑影响了你的思维。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["你用力向前一拍，砸碎了厕所的门。", goods, "unlockedOpen"]
                self.menu.aButton['text'] = "我..."
                self.menu.bButton.hide()
                self.goods.OnClick()
                self.password = Password()
                self.password.passwordFrame.hide()
                self.password.unloadLeap()
                self.password.passState = True
            else:
                if self.goods.state == "unlockedOpen":
                    self.menu.textLabel['text'] = "厕所门上现在没有上锁。"
                    self.menu.aButton['command'] = self.openDoor
                    self.menu.aButton['extraArgs'] = []
                    self.menu.aButton['text'] = "关闭厕所门"
                    self.menu.bButton['command'] = self.doNothing
                    self.menu.bButton['extraArgs'] = []
                    self.menu.bButton['text'] = "离开"
                elif self.goods.state == "unlockedClose":
                    self.menu.textLabel['text'] = "厕所门上现在没有上锁。"
                    self.menu.aButton['command'] = self.openDoor
                    self.menu.aButton['extraArgs'] = []
                    self.menu.aButton['text'] = "打开厕所门"
                    self.menu.bButton['command'] = self.doNothing
                    self.menu.bButton['extraArgs'] = []
                    self.menu.bButton['text'] = "离开"
                else:
                    self.menu.textLabel['text'] = "厕所门上有一个四位数的密码锁。"
                    self.menu.aButton['command'] = self.openDoor
                    self.menu.aButton['extraArgs'] = []
                    self.menu.aButton['text'] = "输入密码"
                    self.menu.bButton['command'] = self.showInfo
                    self.menu.bButton['extraArgs'] = ["这个密码到底是什么呢……", goods, ""]
                    self.menu.bButton['text'] = "暂时离开"
        elif goods.Name == "matong_box3":
            self.menu.selectDialog.show()
            if goods.state == "searched":
                self.menu.textLabel['text'] = "这个马桶已经被调查过了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "上完厕所后冲了一下水，\n发现一个发条卡在马桶的排水口。"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["获得发条", goods, "searched", ["spring"]]
                self.menu.aButton['text'] = "拿起发条"
                self.menu.bButton.hide()
                self.getSpringSound=loader.loadSfx("res/sounds/toilte.mp3")
                self.getSpringSound.setPlayRate(1.5)
                self.getSpringSound.play()
        elif goods.Name == "bookshelf_box":
            self.menu.selectDialog.show()
            if self.bookIndex == 3:
                self.bookIndex = 0
            if self.bookIndex == 0:
                self.menu.textLabel['text'] = "《Erosion研究报告IV》根据我对数据研究证明，被Erosion侵蚀的人在晚期\n" \
                                              "会看到海市蜃楼景象，甚至分不清什么是真实什么是虚妄的幻境。如果没人\n" \
                                              "提醒，那些人会沉湎在幻想美梦中而无法醒来，从而被Erosion完全控制。"
            elif self.bookIndex == 1:
                self.menu.textLabel['text'] = "《格林童话集》为什么这个房间会有这种书？但是我没时间在这里浪费了。"
            elif self.bookIndex == 2:
                self.menu.textLabel['text'] = "《人民日报》上面日期写着2011年2月5日。\n报纸都泛黄了，似乎已经过去了很久。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
            self.bookIndex += 1
        elif goods.Name == "bed_box":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "一点都不困，还是不要睡了。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "离开"
            self.menu.bButton.hide()
        elif goods.Name == "xishoupen":
            self.menu.selectDialog.show()
            if goods.state is not "searched":
                self.menu.textLabel['text'] = "洗手台里好像有什么东西？"
                self.menu.aButton['command'] = self.showInfo
                self.menu.aButton['extraArgs'] = ["在洗手台的上方\n发现了一支抑制剂。", goods, "searched", ["injection"]]
                self.menu.aButton['text'] = "查看"
                self.menu.bButton.hide()
            else:
                self.menu.textLabel['text'] = "洗手台里什么都没有了。"
                self.menu.aButton['command'] = self.doNothing
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "离开"
                self.menu.bButton.hide()
        elif goods.Name == "MusicBox":
            self.menu.selectDialog.show()
            self.menu.textLabel['text'] = "一个装饰精美的八音盒，貌似缺少了什么。"
            self.menu.aButton['command'] = self.doNothing
            self.menu.aButton['extraArgs'] = []
            self.menu.aButton['text'] = "暂时离开"
            self.menu.bButton.hide()
        elif goods.Name == "Scene1_Exit":
            self.menu.selectDialog.show()
            if self.goods.state == "unlockedOpen":
                self.menu.textLabel['text'] = "房间门上现在没有上锁。"
                self.menu.aButton['command'] = self.openExitDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "关闭房间门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            elif self.goods.state == "unlockedClose":
                self.menu.textLabel['text'] = "房间门上现在没有上锁。"
                self.menu.aButton['command'] = self.openExitDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "打开房间门"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
            else:
                self.menu.textLabel['text'] = "房间门上有一个密码锁。"
                self.menu.aButton['command'] = self.openExitDoor
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['text'] = "输入密码"
                self.menu.bButton['command'] = self.showInfo
                self.menu.bButton['extraArgs'] = ["这个密码到底是什么呢……", goods, ""]
                self.menu.bButton['text'] = "暂时离开"
        elif goods.Name == "Scene1_wallword_1":
            self.menu.selectDialog.show()
            if goods.state=="changed":
                self.menu.textLabel['text'] = "之前我记得有这么几道文字被凸显了出来"
                self.menu.aButton['text'] = "查看文字"
                self.menu.aButton['extraArgs'] = []
                self.menu.aButton['command'] = self.showWordAfter
                self.menu.bButton['text'] = "离开"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
            else:
                if (self.player.bag.haveItem("res/models/items/" + "torch" + ".png")):
                    self.menu.textLabel['text'] = "文字并没有发生任何变化"
                else:
                    self.menu.textLabel['text'] = "墙上这些文字和鬼画符一样，用肉眼难以看懂"
                self.menu.aButton['text'] = "查看文字"
                self.menu.aButton['command'] = self.showWordBefore
                self.menu.aButton['extraArgs'] = []
                self.menu.bButton['text'] = "离开"
                self.menu.bButton['command'] = self.doNothing
                self.menu.bButton['extraArgs'] = []
        elif goods.Name == "enemy":
            self.menu.infoDialog.show()
            if goods.state ==1:
                self.showTutorial(1)
                self.showTips('系统提示：请时刻注意你的侵蚀度。')
                goods.state=2
            elif goods.state ==2:
                self.showTutorial(2)
                self.showTips('系统提示：按下Space发动入魔。')
                goods.state=3
            elif goods.state == 3:
                self.showTutorial(3)
                self.showTips('系统提示：在侵蚀度高于50%时你会有破坏\n'
                              '东西的冲动和焦虑感，可能会影响剧情的发展。')
                goods.state=4
            elif goods.state == 4:
                self.showTutorial(4)
                self.showTips('系统提示：留意自己的心跳声。')
                goods.state=5
            elif goods.state == 5:
                self.showTutorial(5)
                self.showTips('系统提示：按下鼠标右键可以\n'
                              '向前方发射侵蚀之门，如果场景中\n'
                              '存在两个侵蚀之门即可互相穿梭。')
                goods.state=1
        else:
            self.resume()

    def waitPaper(self, task):
        if self.paperState == True:
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            base.accept("escape", self.player.game.pauseGame)
            self.player.bag.paperFrame.hide()
            self.player.mission.paperState = True
            self.player.initTask()
            return task.done
        return task.cont

    '''
    wall word
    '''
    def showWordBefore(self):
        self.menu.selectDialog.hide()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.wordframe = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.wordImage = OnscreenImage('res/models/SceneJPG/Scene1_Wall_Hall.png', pos=(0, 0, 0),
                                             scale=(1.4, 1, 1))
        self.wordImage.reparentTo(self.wordframe)
        # self.leaveButton=DirectButton
        self.wordframe.show()
        self.player.initTask()
        base.accept("mouse1", self.wordReturn)
        base.accept("escape",self.wordReturn)

    def showWordAfter(self):
        self.menu.selectDialog.hide()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.wordframe = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.wordImage = OnscreenImage('res/models/SceneJPG/Scene1_Wall_Hall2.png', pos=(0, 0, 0),
                                            scale=(1.4, 1, 1))
        self.wordImage.reparentTo(self.wordframe)
        # self.wordImage.removeNode()
        self.wordframe.show()
        self.player.initTask()
        base.accept("escape", self.wordReturn)
        base.accept("mouse1", self.wordReturn)

    def wordReturn(self):
        self.wordframe.hide()
        self.resume()
        self.player.initTask()
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept('escape', self.player.game.pauseGame)

    def changWord(self, info, goods, state, items=None):
        goods.state = state
        self.manager.GoodsIta["Scene1_wallword_1"].CloseHighLight()
        self.manager.GoodsIta["Scene1_wallword_1"].Node.hide()
        self.manager.GoodsIta["Scene1_wallword_1"].state = "changed"
        self.manager.GoodsIta["Scene1_wallword_2"].Node.show()
        self.menu.infoLabel['text'] = info
        self.menu.infoDialog.show()

        self.resume()
        self.player.initTask()

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
        if self.password.passState == False:
            self.password.passwordFrame.show()
        self.menu.selectDialog.hide()
        taskMgr.add(self.waitPass, "waitPass")
        base.accept('escape', self.waitPassReturn)

    def waitPass(self, task):
        if self.password.passState:
            self.password.passwordFrame.hide()
            self.password.unloadLeap()
            self.goods = self.player.goodmanager.GoodsIta['toilet_door']
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
            self.passwordExit = Gpassword()
        else:
            self.passwordExit.reloadLeap()
        base.accept('b', self.menu.nothing)
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
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            self.goods.OnClick()
            if self.goods.state == "unlockedOpen":
                self.goods.state = "unlockedClose"
            else:
                self.goods.state = "unlockedOpen"
            self.resume()
            self.player.initTask()
            base.accept('escape', self.player.game.pauseGame)
            # self.moveToLevelTwo()
            self.player.mouseIconNormal.show()
            self.player.mouseIconWatch.hide()
            self.player.isInteractive = False
            self.player.node.setPos(-250, 265, 0)
            self.menu.passFrame.show()
            taskMgr.add(self.fadeMove, "fadeMove")
            self.resume()
            return
        if self.passwordExit.wrongTime == 1:
            self.passwordExit.passwordFrame.hide()
            self.passwordExit.wrongTime = 0
            self.passwordExit.clear()
            self.passwordExit.unloadLeap()
            base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
            base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
            self.showInfo("房间门没有任何反应。", self.goods, "")
            base.accept('escape', self.player.game.pauseGame)
            return task.done
        return task.cont

    def waitExitPassReturn(self):
        self.resume()
        self.player.initTask()
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
        # self.player.game.
        base.accept('escape', self.player.game.pauseGame)
        base.accept('b', self.player.game.openBag)
        self.passwordExit.unloadLeap()
        self.passwordExit.clear()
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

    def showInfo(self, info, goods, state, items=None, index=None, addErosion=None):
        self.menu.infoDialog.show()
        goods.state = state
        self.menu.infoLabel['text'] = info
        if items is not None:
            for item in items:
                if item == "paper":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.paper, "一张纸条"))
                elif item == "torch":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.torch, "一个手电筒"))
                elif item == "groupPhoto":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.photo, "一张合影"))
                    self.memoryNum = 1
                elif item == "injection":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.injection, "抑制剂"))
                elif item == "spring":
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.spring, "发条"))
                else:
                    self.player.bag.addItem(Goods("res/models/items/" + item + ".png", self.player.bag.panda, "这是啥？"))
        if index is not None:
            if index == 3:
                self.beginMemory(0)
                self.menu.selectDialog.hide()
                self.skip()
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

    def beginMemory(self, index):
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
        if task.time < 3.0:
            return task.cont
        self.menu.tipDialog.hide()
        return task.done

    def resume(self):
        self.menu.bButton.show()
        self.menu.selectDialog.hide()
        # self.menu.tutorialDialog.hide()
        taskMgr.remove("fadeTask")
        self.skip()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)

    def end(self, fun="endB"):
        self.endFun = fun
        self.menu.tutorialDialog.hide()
        taskMgr.add(self.fadeEnd, "fadeEnd")
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.menu.passFrame.show()

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
        self.menu.infoDialog.show()
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

    def showEndPicture(self, pic):
        self.menu.endBackground.setImage('res/end/' +  pic)
        self.menu.endPictureFrame.show()
        base.accept('mouse1-up', self.removeEndPicture)
    # def fadeEnd(self, task):
    #     if task.time < 2.0:
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
    #     self.menu.infoDialog.show()
    #     self.player.erosionFrame.hide()
    #     self.player.currentItemFrame.hide()
    #     self.menu.tutorialDialog.hide()
    #     self.menu.infoDialog['text'] = "Kura被你吓死了！"
    #     self.skip()

    def moveToLevelTwo(self):
        self.removeGame()
        self.player.erosionFrame.hide()
        self.player.currentItemFrame.hide()
        self.player.shoot.TwoBullet[0].Disappera()
        self.player.shoot.TwoBullet[1].Disappera()
        self.menu.selectedSave = 2
        self.menu.tempPlayer = self.player
        self.menu.loadSave()

    def removeGame(self):
        '''
        释放内存
        '''
        names = ['wall', 'bed_box', 'bookshelf_box', 'box', 'chair1', 'chair2', 'chair3', 'chair4',
                 'desk2', 'desk3_2', 'matong_box3', 'xishoupen', 'yaoshui', 'Scene1_Exit',
                 'Scene1_wallword_1', 'Scene1_wallword_2', 'MusicBox', 'toilet_door', 'enemy']
        for name in names:
            self.player.goodmanager.UnLoad(name)

    def fadeMove(self, task):
        if task.time < 1.0:
            self.menu.passFrame['frameColor'] = (0, 0, 0, task.time)
            return task.cont
        else:
            self.menu.passFrame.hide()
            self.moveToLevelTwo()
            return task.done
