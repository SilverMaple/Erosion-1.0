# -*-coding:utf-8 -*-
import sys, os, random, thread, time, inspect

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = './lib/x64' if sys.maxsize > 2 ** 32 else './lib/x86'
lib_dir = './lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.append(os.path.join(sys.path[0], './lib/'))

from direct.gui.DirectGui import *
# import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase import DirectObject
import Leap


# leapmotion 监听器
class TouchListener(Leap.Listener):
    def on_init(self, controller):
        print "initialized"

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands[0]
        self.pitch = hand.direction.pitch
        self.yaw = hand.direction.yaw
        self.roll = hand.palm_normal.roll
        messenger.send("rotate", [self.pitch, self.yaw, self.roll])


# 物品类，需要物品的平面图，模型和介绍文字
class Goods:
    def __init__(self, picture, model, text):
        self.picture = picture
        self.model = model
        self.text = text
        # useless just to flag
        self.state = ""


# 背包类
class Bag(DirectObject.DirectObject):
    def __init__(self, p):
        DirectObject.DirectObject.__init__(self)
        self.model = None
        self.player = p
        self.bagframe = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.bagframe.hide()
        self.background = OnscreenImage('res/bag-background.png', pos=(0, 0, 0), scale=(1.4, 1, 1.05))
        self.background.reparentTo(self.bagframe)

        # 显示物品图片的滚动条区域
        # self.left = -0.5
        # self.right = 0.3
        # self.bottom = -0.8
        # self.up = 0.8
        self.left = -0.555
        self.right = 0.22
        self.bottom = -0.6
        self.up = 0.96
        self.item_num = 0
        self.current_item = 0
        self.col_num = 3
        self.half = (self.right - self.left) / self.col_num / 2
        # print self.half
        self.itemframe = DirectScrolledFrame(canvasSize=(self.left, self.right, self.bottom * 2, self.up * 2),
                                             frameSize=(self.left, self.right, self.bottom, self.up),
                                             frameColor=(0, 0, 0, 0))
        self.itemframe.reparentTo(self.bagframe)
        self.itemframe.setPos(-0.65, 0, -0.2)
        self.mycamvas = self.itemframe.getCanvas()
        # self.camvasImage = OnscreenImage('res/models/itemsBackground.png', pos=(-.05, 0, 1.1), scale=(.3, .5, 1))
        # self.camvasImage.reparentTo(self.mycamvas)
        # self.camvasImage.setTransparency(TransparencyAttrib.MAlpha)
        self.itemframe.horizontalScroll.hide()
        self.itemframe.verticalScroll.incButton.hide()
        self.itemframe.verticalScroll.decButton.hide()
        self.itemframe["verticalScroll_frameSize"] = (0, 0, 0, 0)

        self.items = []
        self.injectTimes = 0
        self.accept("item", self.setItem)
        base.accept("wheel_up", self.switchItemFor)
        base.accept("wheel_down", self.switchItemBack)
        base.accept("e", self.interact)
        base.accept("E", self.interact)
        self.enemyInteractTimes = 0
        self.paperFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.paperImage = OnscreenImage('res/paper.png', pos=(0, 0, 0),
                                        scale=(1.4, 1, 1))
        self.paperImage.reparentTo(self.paperFrame)
        # self.leaveButton=DirectButton
        self.paperFrame.hide()

        self.copperFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.copperImage = OnscreenImage('res/end/copper.png', pos=(0, 0, 0),
                                        scale=(1.4, 1, 1))
        self.copperImage.reparentTo(self.copperFrame)
        # self.leaveButton=DirectButton
        self.copperFrame.hide()

        # 显示模型区域
        self.showdisplay = base.win.makeDisplayRegion(0.4, 1.0, 0.2, 0.9)
        self.showdisplay.setClearColorActive(False)
        self.showdisplay.setClearDepthActive(True)
        self.showdisplay.setSort(10)
        self.renderR = NodePath('root')
        self.cam2 = self.renderR.attachNewNode(Camera('cam2'))
        self.showdisplay.setCamera(self.cam2)
        self.cam2.setPos(0, -10, 0)

        # 显示文字区域
        self.text = " "
        self.textObject = OnscreenText(text=self.text, pos=(0.5, -0.7),
                                       scale=0.1, fg=(1, 1, 0.5, 1), align=TextNode.ACenter, mayChange=1)
        self.textObject.setWordwrap(15.0)
        self.loadScene1()
        self.loadScene2()

    def loadScene1(self):
        # 添加物品测试
        self.panda = loader.loadModel('panda.egg')
        self.panda.setPos(0, 0, -2)
        self.panda.setScale(0.3, 0.3, 0.3)
        self.ralph = loader.loadModel('res/models/ralph.egg')
        self.ralph.setPos(0, 0, -2)
        self.ralph.setScale(0.3, 0.3, 0.3)

        self.paper = loader.loadModel('res/models/Scene1_Paper.egg')
        self.paper.setPos(0, 0, 0)
        self.paper.setScale(.2)

        self.torch = loader.loadModel('res/models/Scene1_flashlight1.egg')
        self.torch.setPos(0, 0, 0)
        self.torch.setScale(.02)

        self.spring = loader.loadModel('res/models/Scene1_spring_Ver1.0.egg')
        self.spring.setPos(0, 0, 0)
        self.spring.setScale(.8)

        self.photo = loader.loadModel('res/models/Scene1_Photo_Ver1.0.egg')
        self.photo.setPos(0, 0, 0)
        self.photo.setScale(.2)

        self.injection = loader.loadModel('res/models/Scene1_Vaccine_Ver1.1.egg')
        self.injection.setPos(0, 0, 0)
        self.injection.setScale(.2)

    def loadScene2(self):
        '''
        scene 2
        '''
        self.hammer = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_hallhammer.egg')
        self.hammer.setPos(0, 0, 0)
        self.hammer.setScale(.05)

        self.cake = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_hallcake.egg')
        self.cake.setPos(0, 0, 0)
        self.cake.setScale(.05)

        self.carrot = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_onecarrot.egg')
        self.carrot.setPos(0, 0, 0)
        self.carrot.setScale(.08)

        self.knife = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_outknife.egg')
        self.knife.setPos(0, 0, 0)
        self.knife.setScale(.15)

        self.inknife = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_inknife.egg')
        self.inknife.setPos(0, 0, 0)
        self.inknife.setScale(.15)

        self.rabbit = loader.loadModel('res/models/Scene2/Scene2Interaction/rabbit_alive.egg')
        self.rabbit.setPos(0, 0, 0)
        self.rabbit.setScale(.04)

        self.deadRabbit = loader.loadModel('res/models/Scene2/Scene2Interaction/rabbit_dead.egg')
        self.deadRabbit.setPos(0, 0, 0)
        self.deadRabbit.setScale(.04)

        self.copperplate_rusted = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_copperplate_rusted.egg')
        self.copperplate_rusted.setPos(0, 0, 0)
        self.copperplate_rusted.setScale(.04)

        self.copperplate_clean = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_copperplate_clean.egg')
        self.copperplate_clean.setPos(0, 0, 0)
        self.copperplate_clean.setScale(.04)

        self.funBook = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_book-beijuji.egg')
        self.funBook.setPos(0, 0, 0)
        self.funBook.setScale(.04)

        self.sadBook = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_book-xijuji.egg')
        self.sadBook.setPos(0, 0, 0)
        self.sadBook.setScale(.04)

        self.gaoshuBook = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_book-gaoshu.egg')
        self.gaoshuBook.setPos(0, 0, 0)
        self.gaoshuBook.setScale(.04)

        self.goldenKey = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_key.egg')
        self.goldenKey.setPos(0, 0, 0)
        self.goldenKey.setScale(.3)

        self.flower = loader.loadModel('res/models/Scene2/Scene2Cat/oneflower.egg')
        self.flower.setPos(0, 0, 0)
        self.flower.setScale(.04)

        self.bottle = loader.loadModel('res/models/Scene3/Scene3Interaction/Scene3_bottle.egg')
        self.bottle.setPos(0, 0, 0)
        self.bottle.setScale(.1)

        self.emptyBottle = loader.loadModel('res/models/Scene3/Scene3Interaction/Scene3_emptybottle.egg')
        self.emptyBottle.setPos(0, 0, 0)
        self.emptyBottle.setScale(.1)

        self.roomKey = loader.loadModel('res/models/Scene2/Scene2Interaction/Scene2_key.egg')
        self.roomKey.setPos(0, 0, 0)
        self.roomKey.setScale(.3)

        self.addItem(Goods("res/models/items/injection.png", self.injection, "抑制剂"))
        # self.addItem(Goods("res/models/items/copperplate_rusted.png", self.copperplate_rusted, "锈迹斑斑的铜板"))
        self.bagframe.hide()

    # 交互接口，调用此函数将物品放入背包
    def addItem(self, goods):
        item = Item(self.item_num, goods)
        item.button.reparentTo(self.mycamvas)
        # print Bag.item_num
        col = self.item_num % self.col_num
        row = self.item_num / self.col_num
        # print col, row
        item.button.setScale(self.half * 10)
        item.button.setPos(self.left + (self.half + 2 * self.half * col), 0,
                           2 * self.up - (self.half + 2 * self.half * row))

        self.items.append(item)
        self.item_num += 1
        self.current_item = self.item_num - 1
        imageSrc = self.items[self.current_item].goods.picture
        self.player.currentItemFrame['image'] = imageSrc

    def setItem(self, id):
        # print id
        if self.item_num == 0:
            return
        self.item = self.items[id]
        self.textObject.setText(self.item.goods.text)
        if self.model is not None:
            self.model.detachNode()
        self.model = self.item.goods.model
        self.model.reparentTo(self.renderR)
        self.loadLeap(True)
        base.accept("rotate", self.rotate)

    def haveItem(self, name):
        for i in self.items:
            if i.goods.picture == name:
                return True
        return False

    def switchItemFor(self):
        if self.current_item == -1 or self.player.game.gameState == 'pause':
            return
        if self.current_item == self.item_num - 1:
            self.current_item = 0
        else:
            self.current_item += 1
        imageSrc = self.items[self.current_item].goods.picture
        self.player.currentItemFrame['image'] = imageSrc

    def switchItemBack(self):
        if self.current_item == -1 or self.player.game.gameState == 'pause':
            return
        if self.current_item == 0:
            self.current_item = self.item_num - 1
        else:
            self.current_item -= 1
        imageSrc = self.items[self.current_item].goods.picture
        self.player.currentItemFrame['image'] = imageSrc

    def interact(self):
        # print self.items[self.current_item].goods.picture
        if self.item_num == 0:
            return
        #
        # scene 1
        #
        elif self.items[self.current_item].goods.picture == "res/models/items/torch.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "enemy" and self.enemyInteractTimes < 2:
                self.showInfo(self.player.mission.kuraText[self.enemyInteractTimes])
                self.enemyInteractTimes += 1
                return
            elif self.player.currentInteract.Name == "enemy" and self.enemyInteractTimes == 2:
                self.enemyInteractTimes = 0
                self.player.menu.tutorialDialog.show()
                props = WindowProperties()
                props.setCursorHidden(False)
                base.win.requestProperties(props)
                self.player.endTask()
                self.player.menu.nextButton['text'] = self.player.mission.kuraText[2]
                self.player.menu.nextButton['command'] = self.player.mission.end
                # self.player.menu.nextButton['extraArgs'] = "endB"
            elif self.player.currentInteract.Name == "yaoshui":
                if self.player.currentInteract.state is not 'shined':
                    self.player.mission.changWord("后方墙上的一些文字在光芒照射下\n变成了蓝色。手电筒电量耗尽了。",
                                             self.player.goodmanager.GoodsIta['yaoshui'], "shined")
            elif self.player.currentInteract.Name == "bed_box":
                if self.player.currentInteract.state is not 'searched':
                    self.player.mission.showInfo("用手电筒照了一下床底，\n找到了一支抑制剂。",
                                                 self.player.goodmanager.GoodsIta['bed_box'], "searched", ["injection"])
        elif self.items[self.current_item].goods.picture == "res/models/items/spring.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "enemy":
                self.showInfo(self.player.mission.kuraText[3])
                return
            if self.player.currentInteract.Name == "MusicBox":
                goods = self.player.currentInteract
                if goods.state is not 'played':
                    self.player.mission.showInfo("随着八音盒的旋转一张\n纸条掉了出来，获得纸条。", goods, "played", ["paper"], 5)
                    self.player.mission.showTips("随着八音盒的旋转一张\n纸条掉了出来，获得纸条。")
                    self.musicBoxSound=loader.loadSfx("res/sounds/music_box.mp3")
                    self.musicBoxSound.play()
                    props = WindowProperties()
                    props.setCursorHidden(False)
                    base.win.requestProperties(props)
                    self.player.endTask()
        elif self.items[self.current_item].goods.picture == "res/models/items/paper.png":
            if self.player.mission.paperState:
                self.paperFrame.show()
                self.player.mission.paperState = False
                self.player.endTask()
                taskMgr.add(self.player.mission.waitPaper, 'waitPaper')
                base.accept("mouse1", self.player.mission.__setattr__, ["paperState", True])
                base.accept("mouse1-up", self.player.mission.__setattr__, ["paperState", True])
                base.accept("escape", self.player.mission.__setattr__, ["paperState", True])
            else:
                self.paperFrame.hide()
                self.player.mission.paperState = True
                self.player.initTask()
        #
        # scene 2
        #
        elif self.items[self.current_item].goods.picture == "res/models/items/knife.png" \
                or self.items[self.current_item].goods.picture == "res/models/items/inknife.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "painting_8" and self.player.currentInteract.state == '':
                self.player.mission.showInfo('你从这个画上剪下一朵花,\n获得纸花*1', self.player.currentInteract, "cut", ['cutFlower'])
                self.player.currentInteract.state = 'done'
        elif self.items[self.current_item].goods.picture == "res/models/items/carrot.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "rabbit_cage":
                self.player.mission.showInfo("你使用胡萝卜引诱兔子出来，抓出了一只兔子。\n"
                                             "获得兔子*1", self.player.currentInteract, "", ["rabbit_alive"])
        elif self.items[self.current_item].goods.picture == "res/models/items/rabbit_alive.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "food_box":
                self.player.mission.showInfo("实验兔吃下了发霉的食物，蹬了一下腿\n"
                                             "就一动不动了。获得死兔", self.player.currentInteract, "eaten", ["rabbit_dead"])
            elif self.player.currentInteract.Name == "window_box" or self.player.currentInteract.Name == "window_broken_box":
                if self.player.currentInteract.state is not 'smashed':
                    self.player.mission.showInfo("窗户似乎打不开呢……没有办法放兔子进去。", self.player.currentInteract, "")
            elif self.player.currentInteract.Name == "outdoor_box":
                self.player.mission.showInfo("你将实验兔放在门口，之后躲在大厅门旁暗中观察。\n"
                                             "这时，一只血红色的手抓住了兔子，将其拉入\n"
                                             "了门内。你似乎听到门内传来“我……还……要”", self.player.currentInteract, "rabbit")
                self.removeItem('rabbit_alive')
        elif self.items[self.current_item].goods.picture == "res/models/items/rabbit_dead.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "window_box" or self.player.currentInteract.Name == "window_broken_box":
                if self.player.currentInteract.state is not 'smashed':
                    self.player.mission.showInfo("窗户似乎打不开呢……没有办法放兔子进去。", self.player.currentInteract, "")
            elif self.player.currentInteract.Name == "outdoor_box":
                self.player.mission.showInfo("你将死兔放在门口，之后躲在大厅门旁暗中观察。\n"
                                             "这时，一只血红色的手抓住了兔子，将其拉入\n"
                                             "了门内。不久，门内传来哀嚎声。", self.player.currentInteract, "unlockedCloseFirst", )
                self.removeItem('rabbit_dead')
        elif self.items[self.current_item].goods.picture == "res/models/items/hammer.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "window_box" or self.player.currentInteract.Name == "window_broken_box":
                if self.player.EROSION < 80:
                    self.player.mission.showInfo("实验室窗户异常坚硬，砸不开。", self.player.currentInteract, "")
                else:
                    self.brokeWindowSound=loader.loadSfx("res/sounds/Crash.mp3")
                    self.brokeWindowSound.play()
                    self.player.mission.showInfo("你用锤子直接砸碎了窗户。\n一个锈迹斑斑的铜板掉了下来。\n"
                                                 "获得锈迹斑斑的铜板*1", self.player.currentInteract,
                                                 "smashed", ["copperplate_rusted"])
                    self.player.goodmanager.GoodsIta['window_broken_box'].state = 'smashed'
                    self.player.goodmanager.GoodsIta['window_box'].state = 'smashed'
                    self.player.goodmanager.GoodsIta['window_broken_box'].Node.show()
                    taskMgr.add(self.disappearWindow, "disappear")
                    self.player.goodmanager.GoodsIta['window_box'].Node.hide()
                    self.player.goodmanager.UnLoad('window_box')
            elif self.player.currentInteract.Name == "mirror_box":
                self.brokeWindowSound = loader.loadSfx("res/sounds/Crash.mp3")
                self.brokeWindowSound.play()
                self.player.mission.showInfo("你用锤子砸碎了镜子，发现这其实是一块玻璃，\n"
                    "表里两侧除了光线以外完全相同。", self.player.currentInteract, "smashed")
                self.player.goodmanager.GoodsIta['mirror_box'].Node.hide()
                self.player.game.UnLoadmirror()
                self.player.goodmanager.UnLoad('mirror_box')
                    # props = WindowProperties()
                    # props.setCursorHidden(False)
                    # base.win.requestProperties(props)
                    # self.player.endTask()
                    # self.player.menu.selectDialog.show()
                    # self.player.menu.textLabel['text'] = "你用锤子直接砸碎了窗户。同时，窗户内传来镜子破碎的声音。"
                    # self.player.menu.aButton['command'] = self.player.mission.showInfo
                    # self.player.menu.aButton['extraArgs'] = ["一个锈迹斑斑的铜板掉了下来。\n"
                    #                                          "获得锈迹斑斑的铜板*1", self.player.currentInteract,
                    #                                          "smashed",
                    #                                          ["copperplate_rusted"]]
                    # self.player.menu.aButton['text'] = "用锤子砸"
                    # self.player.menu.bButton['command'] = self.player.mission.doNothing
                    # self.player.menu.bButton['extraArgs'] = []
                    # self.player.menu.bButton['text'] = "离开"
            elif self.player.currentInteract.Name == "ElectricBox":
                self.player.mission.showInfo('你砸开了配电盒，此时从配电盒里传来\n'
                                             '巨大电流，你被电成了焦炭。', self.player.currentInteract, "smashed",
                                             None, 'endD', None)
            elif self.player.currentInteract.Name == "dianti_box":
                self.player.mission.showInfo('你愤怒的抄起锤子砸向电梯门。\n'
                                             '门似乎被砸出了一点缝隙。', self.player.currentInteract, "cracked",
                                             ['broken_dianti'])
            elif self.player.currentInteract.Name == "broken_dianti_box":
                self.player.mission.showInfo('你愤怒的抄起锤子砸向有一点裂缝\n'
                                             '的电梯门。电梯间的门被砸开了。', self.player.currentInteract, "smashed",
                                             None, 'endD', None)
            elif self.player.currentInteract.Name == "outdoor_box" \
                    and self.player.currentInteract.state is not 'unlockedOpen'\
                    and self.player.currentInteract.state is not 'unlockedClose':
                self.player.mission.showInfo("你把门敲开了，看到了一群满身血迹的怪物。\n"
                                             "这时谁都救不了你了。", self.player.currentInteract, "", None, "endE", None)
        elif self.items[self.current_item].goods.picture == "res/models/items/goldenKey.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "ElectricBox" and self.player.currentInteract.state is not 'opened':
                self.player.mission.showInfo('配电盒的锁被打开了。你拉下了电闸，\n'
                                             '看到电梯的按钮亮了起来。', self.player.currentInteract, "opened")
                self.player.goodmanager.GoodsIta['dianti_box'].state = 'ready'
                self.player.goodmanager.GoodsIta['broken_dianti_box'].state = 'ready'
        elif self.items[self.current_item].goods.picture == "res/models/items/flower.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "vase_box":
                self.player.mission.showInfo('插入了一朵纸花', self.player.currentInteract, "", ['setOutflower'])
            elif self.player.currentInteract.Name == "invase_box":
                self.player.mission.showInfo('插入了一朵纸花', self.player.currentInteract, "", ['setInflower'])
        elif self.items[self.current_item].goods.picture == "res/models/items/funBook.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "furnace_box":
                self.player.mission.showInfo('你把莎士比亚喜剧集烧掉，\n火焰变的更旺了。', self.player.currentInteract, "burned", None)
                self.player.goodmanager.GoodsIta['Scene2_book-xijuji'].burning()
                self.player.bag.removeItem('funBook')
            elif self.player.currentInteract.Name == "infurnace_box":
                self.player.mission.showInfo('这时火焰突然跃起，侵蚀度+15。', self.player.currentInteract, "", None, None, 15)
                self.player.bag.removeItem('funBook')
        elif self.items[self.current_item].goods.picture == "res/models/items/sadBook.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "infurnace_box":
                self.player.mission.showInfo('你把莎士比亚悲剧集烧掉，\n火焰变的更旺了。', self.player.currentInteract, "burned", None)
                self.player.goodmanager.GoodsIta['Scene2_book-beijuji'].burning()
                self.player.bag.removeItem('sadBook')
            elif self.player.currentInteract.Name == "furnace_box":
                self.player.mission.showInfo('这时火焰突然跃起，侵蚀度+15。', self.player.currentInteract, "", None, None, 15)
                self.player.bag.removeItem('sadBook')
        elif self.items[self.current_item].goods.picture == "res/models/items/copperplate_rusted.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "lavabo_box" \
                    or self.player.currentInteract.Name == "inlavabo_box":
                self.player.mission.showInfo("你用稀硫酸除去了铁锈，看到了铜片上的文字。",
                                             self.player.currentInteract, "", ["copperplate_clean"])
        elif self.items[self.current_item].goods.picture == "res/models/items/copperplate_clean.png":
            if self.player.mission.copperState:
                self.copperFrame.show()
                self.player.mission.copperState = False
                self.player.endTask()
                taskMgr.add(self.player.mission.waitCopper, 'waitCopper')
                base.accept("mouse1", self.player.mission.__setattr__, ["copperState", True])
                base.accept("mouse1-up", self.player.mission.__setattr__, ["copperState", True])
                base.accept("escape", self.player.mission.__setattr__, ["copperState", True])
            else:
                self.copperFrame.hide()
                self.player.mission.copperState = True
                self.player.initTask()
                # props = WindowProperties()
                # props.setCursorHidden(False)
                # base.win.requestProperties(props)
                # self.player.endTask()
                # self.player.menu.selectDialog.show()
                # self.player.menu.textLabel['text'] = "硫酸槽中盛满了稀硫酸。"
                # self.player.menu.aButton['command'] = self.player.mission.showInfo
                # self.player.menu.aButton['extraArgs'] = ["你用稀硫酸除去了铁锈，看到了铜片上的文字。",
                #                                          self.player.currentInteract, "", ["copperplate_clean"]]
                # self.player.menu.aButton['text'] = "使用铜板"
                # self.player.menu.bButton['command'] = self.player.mission.doNothing
                # self.player.menu.bButton['extraArgs'] = []
                # self.player.menu.bButton['text'] = "离开"
        #
        # scene3
        #
        elif self.items[self.current_item].goods.picture == "res/models/items/roomKey.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "chessdoor_box":
                self.player.goodmanager.GoodsIta['chessdoor_box'].state = 'unlockedOpen'
                self.player.goodmanager.GoodsIta['chessdoor_box'].OpenDoor()
        elif self.items[self.current_item].goods.picture == "res/models/items/bottle_empty.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "pool_box":
                self.player.mission.showInfo("装了一小瓶灰色的水。\n获得装满水的小瓶子",
                                             self.player.currentInteract, "", ["bottle"])
        elif self.items[self.current_item].goods.picture == "res/models/items/bottle.png":
            if self.player.currentInteract is None:
                return
            if self.player.currentInteract.Name == "bookshelf_box":
                if self.player.goodmanager.GoodsIta['bookshelf_box'].state == 'stage3':
                    props = WindowProperties()
                    props.setCursorHidden(False)
                    base.win.requestProperties(props)
                    self.player.endTask()
                    self.player.mission.showInfo("你看到《如何把马画成骆驼》突然跳了起来，\n"
                                                 "还好你及时泼上了水。你打开了这本书，\n"
                                                 "书上写着：将我移动至C3，礼拜堂即可打开。",
                                                 self.player.currentInteract, "stage4", None, 3, None)
                    self.player.menu.infoDialog.hide()
                    self.player.menu.tipDialog.show()
                    self.player.menu.tipLabel['text'] = '你看到《如何把马画成骆驼》突然跳了起来，\n' \
                                                        '还好你及时泼上了水。你打开了这本书，\n' \
                                                        '书上写着：将我移动至C3，礼拜堂即可打开。'
                    taskMgr.add(self.player.mission.fadeTipsTask, 'fadeTipsTask')
                    self.removeItem('bottle')
                    self.addItem(Goods("res/models/items/" + 'bottle_empty' + ".png", self.player.bag.emptyBottle, "一个空瓶子"))
        elif self.items[self.current_item].goods.picture == "res/models/items/injection.png":
            self.useInjection()

    def disappearWindow(self, task):
        if task.time < 1:
            return task.cont
        else:
            self.player.goodmanager.UnLoad('window_broken_box')
            return task.done

    def useInjection(self):
        if self.current_item < 0:
            return
        if self.items[self.current_item].goods.picture == "res/models/items/injection.png":
            self.items[self.current_item].button.hide()
            self.items.remove(self.items[self.current_item])
            self.item_num -= 1
            self.current_item = self.item_num - 1
            self.adjustItem()
            if self.current_item == -1:
                imageSrc = "res/models/items/blank.png"
                self.player.currentItemFrame['image'] = imageSrc
            else:
                imageSrc = self.items[self.current_item].goods.picture
                self.player.currentItemFrame['image'] = imageSrc
            decrease = 30 - 3 * self.injectTimes
            self.injectTimes += 1
            self.healSound=loader.loadSfx("res/sounds/Heal7.mp3")
            self.healSound.play()
            if decrease < 0:
                decrease = 0
            if self.player.EROSION < decrease:
                self.player.EROSION = 0
            else:
                self.player.EROSION -= decrease
            # self.showInfo("使用了抑制剂，侵蚀度-"+str(decrease))
            self.showInfo("使用了抑制剂，\n感觉自己的神志清醒了一点。")

    def removeItem(self, name):
        for it in self.items:
            if it.goods.picture == "res/models/items/" + name + ".png":
                # if it.id == self.current_item:
                #     self.current_item = self.item_num - 2
                # else:
                #     self.current_item = self.item_num - 1
                self.current_item = self.item_num - 2
                it.button.hide()
                self.items.remove(it)
                self.item_num -= 1
                self.adjustItem()
                # print self.current_item
                if self.current_item == -1:
                    imageSrc = "res/models/items/blank.png"
                    self.model = None
                else:
                    imageSrc = self.items[self.current_item].goods.picture
                    self.model = self.items[self.current_item].goods.model
                self.player.currentItemFrame['image'] = imageSrc
                return

    def removeAllItem(self):
        for it in self.items:
            self.current_item = self.item_num - 2
            it.button.hide()
            self.items.remove(it)
            self.item_num -= 1
            self.adjustItem()
            # print self.current_item
            if self.current_item <= -1:
                imageSrc = "res/models/items/blank.png"
                self.model = None
            else:
                imageSrc = self.items[self.current_item].goods.picture
                self.model = self.items[self.current_item].goods.model
            self.player.currentItemFrame['image'] = imageSrc

    def adjustItem(self):
        index = 0
        for item in self.items:
            item.id = index
            col = index % self.col_num
            row = index / self.col_num
            item.button.setPos(self.left + (self.half + 2 * self.half * col), 0,
                               2 * self.up - (self.half + 2 * self.half * row))
            index += 1

    def showInfo(self, info):
        self.player.menu.infoDialog.show()
        self.player.menu.infoLabel['text'] = info
        self.player.mission.resume()
        self.player.initTask()

    def rotate(self, p, y, r):
        self.model.setHpr(y * 180, p * 180, r * 180)

    def loadLeap(self, b):
        if b == True:
            # 加载leap motion
            self.leapController = Leap.Controller()
            self.touchListener = TouchListener()
            self.leapController.add_listener(self.touchListener)


class Item:
    def __init__(self, id, goods):
        self.id = id
        self.goods = goods
        self.button = DirectButton()

        self.button["command"] = self.sendMessage
        self.button["image"] = self.goods.picture
        self.button["image_scale"] = 0.1

    def sendMessage(self):
        messenger.send("item", [self.id])
