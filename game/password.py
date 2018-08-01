# -*- coding:utf-8 -*-
import inspect
import os
import sys

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = './lib/x64' if sys.maxsize > 2 ** 32 else './lib/x86'
lib_dir = './lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.append(os.path.join(sys.path[0], './lib/'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, './lib/zui/')))
from znode import ZNode, Draggable, Highlightable
from zcanvas import zcanvas

from direct.gui.DirectGui import *
# import direct.directbase.DirectStart
import Leap


class TouchListener(Leap.Listener):
    last_TouchZone = Leap.Pointable.ZONE_HOVERING

    def on_init(self, controller):
        print "initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        global last_TouchZone  # 上一帧的触摸情况
        frame = controller.frame()
        finger = frame.fingers.frontmost  # 获取最前面的手指位置
        # 实现触摸仿真时，必须将Leap Motion坐标空间映射到应用程序的屏幕空间。为了使此映射更容易，Leap Motion API提供了InteractionBox类
        interactionBox = frame.interaction_box
        normalizedPosition = interactionBox.normalize_point(finger.stabilized_tip_position)
        winW = base.win.getXSize()
        winH = base.win.getYSize()
        md = base.win.getPointer(0)
        base.win.movePointer(0, int((normalizedPosition.x) * winW), int(winH - winH * (normalizedPosition.y)))
        if (finger.touch_distance > 0 and finger.touch_zone == Leap.Pointable.ZONE_HOVERING):
            # 注意leap motion的坐标系的y轴与普通的计算机图形学坐标系不同，y是朝上的
            # print "close to but no touch"
            last_TouchZone = Leap.Pointable.ZONE_HOVERING
        elif (finger.touch_zone == Leap.Pointable.ZONE_TOUCHING and last_TouchZone != Leap.Pointable.ZONE_TOUCHING):
            print "touch"
            # 点击密码键
            if normalizedPosition.y > 0.3 and normalizedPosition.y < 0.6:
                if (normalizedPosition.x > 0.14 and normalizedPosition.x < 0.28):
                    messenger.send("Key0")
                elif (normalizedPosition.x > 0.32 and normalizedPosition.x < 0.46):
                    messenger.send("Key1")
                elif (normalizedPosition.x > 0.5 and normalizedPosition.x < 0.64):
                    messenger.send("Key2")
                elif (normalizedPosition.x > 0.68 and normalizedPosition.x < 0.82):
                    messenger.send("Key3")
            # 点击确定按钮
            elif normalizedPosition.y > 0.12 and normalizedPosition.y < 0.3:
                if normalizedPosition.x > 0.45 and normalizedPosition.x < 0.57:
                    messenger.send("Check")

            last_TouchZone = Leap.Pointable.ZONE_TOUCHING
        else:
            # print "too far"
            Last_TouchZone = Leap.Pointable.ZONE_NONE


class GTouchListener(Leap.Listener):
    def on_init(self, controller):
        self.last_TouchZone = Leap.Pointable.ZONE_HOVERING  # 上一帧的触摸情况
        print "initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands[0]  # 手部
        # strength = hand.grab_strength #抓力，握拳时为1
        radius = hand.sphere_radius  # 曲率半径
        finger = frame.fingers.frontmost  # 获取最前面的手指位置
        # 实现触摸仿真时，必须将Leap Motion坐标空间映射到应用程序的屏幕空间。为了使此映射更容易，Leap Motion API提供了InteractionBox类
        interactionBox = frame.interaction_box
        normalizedPosition = interactionBox.normalize_point(finger.stabilized_tip_position)
        winW = base.win.getXSize()
        winH = base.win.getYSize()
        # md = base.win.getPointer(0)
        base.win.movePointer(0, int((normalizedPosition.x) * winW), int(winH - winH * (normalizedPosition.y)))
        # 握拳清零
        # if strength == 1:
        # messenger.send("p")
        if radius <= 32:
            messenger.send("p")

        # 点击屏幕
        if (finger.touch_distance > 0 and finger.touch_zone == Leap.Pointable.ZONE_HOVERING):
            # 注意leap motion的坐标系的y轴与普通的计算机图形学坐标系不同，y是朝上的
            print "close to but no touch"
            if (self.last_TouchZone == Leap.Pointable.ZONE_TOUCHING):
                messenger.send("mouse1-up")
            self.last_TouchZone = Leap.Pointable.ZONE_HOVERING
        elif (
                        finger.touch_zone == Leap.Pointable.ZONE_TOUCHING and self.last_TouchZone != Leap.Pointable.ZONE_TOUCHING):
            print "touch"
            # 点击密码键
            messenger.send("mouse1")
            self.last_TouchZone = Leap.Pointable.ZONE_TOUCHING
        else:
            print "too far"
            if (self.last_TouchZone == Leap.Pointable.ZONE_TOUCHING):
                self.Last_TouchZone = Leap.Pointable.ZONE_NONE
            messenger.send("mouse1-up")


# 普通密码键
class KeyNode:
    def __init__(self, indexnum):
        self.word = 0
        self.indexnum = indexnum
        self.button = DirectButton(commandButtons=[DGG.LMB, DGG.RMB])  # 设置能够鼠标左右键点击按钮
        tex = loader.loadTexture("res/models/password/password" + str(self.word) + ".png")
        self.button["frameTexture"] = tex
        self.button["frameSize"] = (-0.2, 0.2, -0.3, 0.3)
        self.button["command"] = self.mouseClick
        # mySound = loader.loadSfx("2955.wav")
        # self.button["clickSound"]=mySound

        self.button.accept("Key" + str(self.indexnum), self.mouseClick)

        self.mySoundC = loader.loadSfx("res/sounds/change.wav")

    def setpos(self, a, b, c):
        self.button.setPos(a, b, c)

    def mouseClick(self):
        self.word = (self.word + 1) % 10
        tex = loader.loadTexture("res/models/password/password" + str(self.word) + ".png")
        self.button["frameTexture"] = tex

        self.mySoundC.play()

    def getWord(self):
        return self.word

    def getButton(self):
        return self.button


# 普通密码
class Password:
    def __init__(self):
        self.passwordFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        # self.passwordFrame.reparentTo(render2d)
        # 背景图片
        background = OnscreenImage(image='res/models/password/back.jpg', pos=(0, 0, 0), scale=2)
        background.reparentTo(self.passwordFrame)
        # 加载音效
        self.mySoundF = loader.loadSfx("res/sounds/fail.wav")
        # self.mySoundS = loader.loadSfx("res/sounds/success.wav")
        self.wrongTime = 0
        # 加载keynode
        self.keynode_list = []
        self.keynodeIndex = 0
        for x in (-0.75, -.25, .25, .75):
            self.keynode_list.append(KeyNode(self.keynodeIndex))
            self.keynode_list[self.keynodeIndex].setpos(x, 0, 0)
            self.keynode_list[self.keynodeIndex].button.reparentTo(self.passwordFrame)
            self.keynodeIndex += 1

        # 设置密码
        self.password = "5387"
        self.passState = False

        # 点击按钮检测是否正确
        maps = loader.loadModel('res/models/password/yuan.egg')
        self.enterButton = DirectButton(
            geom=(maps.find('**/yuan1'), maps.find('**/yuan2'), maps.find('**/yuan3'), maps.find('**/yuan4')),
            scale=0.3)
        self.enterButton["relief"] = None  # 去除frame的浮雕效果，这样才可以让button的形状与模型相同
        self.enterButton["frameSize"] = (-0.1, 0.1, -0.1, 0.1)
        self.enterButton.setPos(0, 0, -0.6)
        self.enterButton['command'] = self.check
        self.enterButton.accept("Check", self.check)
        self.enterButton.reparentTo(self.passwordFrame)
        self.loadLeap(True)

    def loadLeap(self, b):
        if b == True:
            # 加载leapmotion
            self.leapController = Leap.Controller()
            self.touchListener = TouchListener()
            self.leapController.add_listener(self.touchListener)

    def unloadLeap(self):
        self.leapController.remove_listener(self.touchListener)

    def reloadLeap(self):
        self.leapController.add_listener(self.touchListener)

    def isPassword(self):
        i = 0
        temp = ""
        while i < self.keynodeIndex:
            temp += str(self.keynode_list[i].getWord())
            i += 1
        if temp == self.password:
            return True
        else:
            return False

    def check(self):
        if self.isPassword():
            # self.mySoundS.play()
            self.passState = True
        else:
            self.mySoundF.play()
            self.passState = False
            self.wrongTime = 1


# 手势键
class GKeynode(ZNode, Draggable, Highlightable):
    def __init__(self, geom=None):
        ZNode.__init__(self, geomnode=geom)
        Draggable.__init__(self)
        Highlightable.__init__(self)
        self.set_draggable(True)
        self.set_highlightable(True)


# 手势密码
class Gpassword:
    def __init__(self):
        self.loadLeap(True)
        self.passwordFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage(image='res/models/password/Gpassword_bg.jpg', pos=(0, 0, 0), scale=(2.5, 1, 1))
        self.background.reparentTo(self.passwordFrame)
        self.keynode_list = []
        self.password = "5876301"
        self.passState = False
        self.wrongTime = 0
        self.maps = loader.loadModel('res/models/password/key_maps.egg')

        for i in range(9):
            self.keynode_list.append(GKeynode(geom=self.maps.find('**/Unpress').node()))
            self.keynode_list[i].index = i
            self.keynode_list[i].setPos(i % 3 * 0.5 - 0.5, 0, i / 3 * 0.5 - 0.5)
            self.keynode_list[i].reparentTo(self.passwordFrame)

            base.accept('p', self.clear)
            base.accept('mouse1', zcanvas.press)
            base.accept('mouse1-up', zcanvas.unpress)
            base.accept('changeGeom', self.changeGeom)
            taskMgr.add(self.check, "check-task")

    def changeGeom(self, i):
        if not self.keynode_list[i].isenable:
            self.keynode_list[i].change_geom(self.maps.find('**/Press').node())
            zcanvas.gesture += str(i)
            print zcanvas.gesture
            self.keynode_list[i].isenable = True

    # leap motion模块
    def loadLeap(self, b):
        if b == True:
            # 加载leapmotion
            self.leapController = Leap.Controller()
            self.touchListener = GTouchListener()
            self.leapController.add_listener(self.touchListener)

    def unloadLeap(self):
        self.leapController.remove_listener(self.touchListener)
        taskMgr.remove("check-task")

    def reloadLeap(self):
        self.leapController.add_listener(self.touchListener)
        base.accept('mouse1', zcanvas.press)
        base.accept('mouse1-up', zcanvas.unpress)
        taskMgr.add(self.check, "check-task")

    # 每帧都进行检测，看密码是否正确
    def check(self, task):
        if self.password == zcanvas.gesture:
            self.passState = True
            # self.passwordFrame.hide()
        elif len(zcanvas.gesture) >= 8:
            self.wrongTime = 1
        return task.cont

    # 清除之前的操作痕迹
    def clear(self):
        zcanvas.gesture = ""
        for i in range(9):
            self.keynode_list[i].change_geom(self.maps.find('**/Unpress').node())
            self.keynode_list[i].isenable = False


class Boxpassword():
    def __init__(self):
        self.passwordFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage(image='./res/models/password/Gpassword_bg.jpg', pos=(0, 0, 0),
                                        scale=(2.5, 1, 1))
        self.background.reparentTo(self.passwordFrame)
        self.tips = OnscreenText(text="tips:往相反方向转时此刻度即为输入，同一方向转两圈重置密码", pos=(0, 0.9), scale=0.06)
        self.tips.reparentTo(self.passwordFrame)

        self.password = [13, 7, 6, 8]
        self.clockwise = None  # 顺时针转动为True ,逆时针为False
        self.isinput = False
        self.input = []  # 用户输入的密码串
        self.passState = False
        self.wrongTime = 0

        # self.num=-1
        self.rSound = loader.loadSfx('res/sounds/rotate.wav')
        self.cSound = loader.loadSfx('res/sounds/correct.wav')
        self.precision = 0.3  # 精度
        self.lockfixed = loader.loadModel("res/models/password/boxlockf.egg")
        self.lockfixed.reparentTo(self.passwordFrame)
        self.lockrotate = loader.loadModel("res/models/password/boxlockr.egg")
        self.lockrotate.reparentTo(self.passwordFrame)
        self.lastAxis = 0
        base.accept("mouse1", self.rotate)
        base.accept("mouse1-up", self.Unrotate)

    def reloadInput(self):
        base.accept("mouse1", self.rotate)
        base.accept("mouse1-up", self.Unrotate)
        taskMgr.add(self.Frame_ratote, "rotate-task")
        self.lastAxis = 0
        self.lockrotate.setR(0)
        self.input = []
        self.clockwise = None

    def rotate(self):
        self.rSound.setLoop(True)
        self.rSound.play()
        taskMgr.add(self.Frame_ratote, "rotate-task")

    def Unrotate(self):
        self.rSound.setLoop(False)
        self.rSound.stop()
        taskMgr.remove('rotate-task')

    def Frame_ratote(self, task):
        if self.check():  # 检查密码是否输入正确
            print "success"
            self.passState = True
            self.passwordFrame.hide()
            return task.done

        axis = self.lockrotate.getR()
        self.MousePos = base.win.getPointer(0)
        Winwidth = base.win.getXSize()

        # 判断旋转方向及输入与否
        if self.MousePos.getX() > Winwidth / 2:  # 右转
            # 与之前旋转方向相反，相当于输入
            if self.clockwise == False:
                self.isinput = True
            self.clockwise = True

        elif self.MousePos.getX() < Winwidth / 2:  # 左转
            # 与之前旋转方向相反，相当于输入
            if self.clockwise == True:
                self.isinput = True
            self.clockwise = False

        # 输入
        if self.isinput:
            if abs(axis - self.lastAxis) > 720:
                self.lastAxis = axis
                self.input = []
                print "重置"
            print self.AxisToNum(axis)
            temp = self.AxisToNum(axis)
            self.input.append(temp)
            if len(self.input) < 4:
                index = len(self.input) - 1
                if self.password[index] > self.input[index] - self.precision and self.password[index] < self.input[
                    index] + self.precision:
                    self.cSound.play()
            self.isinput = False

        # 旋转
        if self.clockwise == True:
            self.lockrotate.setR(axis + 0.6)
        else:
            self.lockrotate.setR(axis - 0.6)
        return task.cont

    def AxisToNum(self, axis):
        num = 16 - ((axis) % 360) / 360.0 * 16
        # print num
        return num

    def check(self):
        success = False
        if len(self.input) == 4:
            success = True
            for i in range(4):
                if not (self.password[i] > self.input[i] - self.precision and self.password[i] < self.input[
                    i] + self.precision):
                    success = False
                    self.wrongTime = 1
                    self.input = []
                    self.isinput = False
                    self.Unrotate()
                    return success
            self.Unrotate()
        # print success
        return success


class Epassword:
    def __init__(self):
        self.loadLeap(True)
        self.password = "1563"
        self.passState = False
        self.wrongTime = 0
        self.passwordFrame = DirectFrame(frameSize=(-2, 2, -2, 2), pos=(0, 0, 0), frameColor=(0, 0, 0, 1))
        self.backg = OnscreenImage(image='res/models/password/ep_bk.png', pos=(0, 0, 0), scale=(2.5, 1, 1))
        self.backg.reparentTo(self.passwordFrame)
        self.interactiveframe = DirectFrame(frameSize=(-0.75, 0.75, -0.9, 0.9), pos=(0, 0, 0), frameColor=(1, 0, 0, 1))
        self.interactiveframe.reparentTo(self.passwordFrame)
        self.backg = OnscreenImage(image='res/models/password/ep_bk.png', pos=(0, 0, 0), scale=(0.75, 0, 0.9))
        self.backg.reparentTo(self.interactiveframe)
        self.showNum = DirectEntry(obscured=1, frameColor=(0, 1, 1, 0.4), scale=.1, numLines=1, width=6,
                                   text_scale=(2, 2), initialText="", focus=1, focusInCommand=self.inputText,
                                   focusOutCommand=self.clearText)
        self.maps = loader.loadModel('res/models/password/elec_lock.egg')
        self.showNum['frameTexture'] = loader.loadTexture('res/models/password/display.png')
        self.showNum.reparentTo(self.interactiveframe)
        self.showNum.setPos(-0.6, 0, 0.55)
        self.keynode_list = []
        self.presssound = loader.loadSfx('res/sounds/Epress.wav')

        # 0键
        self.keynode_list.append(GKeynode(geom=self.maps.find('**/0').node()))
        self.keynode_list[0].index = 0
        self.keynode_list[0].setPos(0.55, 0, - 0.5)
        self.keynode_list[0].reparentTo(self.interactiveframe)
        self.keynode_list[0].set_highlightable(False)
        # 1-9
        i = 1
        while i < 10:
            self.keynode_list.append(GKeynode(geom=self.maps.find('**/' + str(i)).node()))
            self.keynode_list[i].index = i
            self.keynode_list[i].setPos((i - 1) % 3 * 0.35 - 0.5, 0, (i - 1) / 3 * 0.35 - 0.5)
            self.keynode_list[i].reparentTo(self.interactiveframe)
            self.keynode_list[i].set_highlightable(False)
            i += 1

        # 回退键
        self.keynode_list.append(GKeynode(geom=self.maps.find('**/backspace').node()))
        self.keynode_list[10].index = 10
        self.keynode_list[10].setPos(0.55, 0, -.15)
        self.keynode_list[10].reparentTo(self.interactiveframe)
        self.keynode_list[10].set_highlightable(False)
        # 确认键
        self.keynode_list.append(GKeynode(geom=self.maps.find('**/ok').node()))
        self.keynode_list[11].index = 11
        self.keynode_list[11].setPos(0.55, 0, 0.2)
        self.keynode_list[11].reparentTo(self.interactiveframe)
        self.keynode_list[11].set_highlightable(False)

        base.accept('sure', self.check)
        base.accept('mouse1', zcanvas.press)
        base.accept('mouse1-up', zcanvas.unpress)
        base.accept('focusChange', self.focusChange)
        base.accept('changeGeom', self.changeGeom)
        base.accept('unpress', self.upspring)

    def changeGeom(self, i):
        self.presssound.play()
        if i in range(10):
            if self.showNum['frameColor'] == (1, 0, 0, 0.6):
                self.showNum['frameColor'] = (0, 1, 1, 0.6)
                zcanvas.gesture = ""
            self.keynode_list[i].change_geom(self.maps.find('**/' + str(i) + 'a').node())
            zcanvas.gesture += str(i)
        elif i == 10:  # 回退
            if self.showNum['frameColor'] == (1, 0, 0, 0.6):
                self.showNum['frameColor'] = (0, 1, 1, 0.6)
                zcanvas.gesture = ""
            self.keynode_list[i].change_geom(self.maps.find('**/backspace-a').node())
            if zcanvas.gesture != "":
                zcanvas.gesture = zcanvas.gesture[:-1]
        elif i == 11:  # 确认
            self.keynode_list[i].change_geom(self.maps.find('**/oka').node())
            self.check()

    def upspring(self, i):
        if i in range(10):
            self.keynode_list[i].change_geom(self.maps.find('**/' + str(i)).node())
        elif i == 10:  # 回退
            self.keynode_list[i].change_geom(self.maps.find('**/backspace').node())
        elif i == 11:  # 确认
            self.keynode_list[i].change_geom(self.maps.find('**/ok').node())

    def check(self):
        if self.password == zcanvas.gesture:
            self.showNum['frameColor'] = (0, 1, 0, 0.6)
            self.showNum.doMethodLater(0.5, self.delay, 'delayout-task')
            self.passState = True
            return True
        else:
            self.showNum['frameColor'] = (1, 0, 0, 0.6)
            print "false"
            self.wrongTime = 1
            self.showNum.doMethodLater(0.5, self.delay, 'delayout-task')
            return False

    def inputText(self):
        self.showNum.enterText(zcanvas.gesture)

    def clearText(self):
        self.showNum.enterText('')

    def focusChange(self):
        self.showNum['focus'] = 0
        self.showNum['focus'] = 1

    def delay(self, task):
        self.passwordFrame.hide()
        return task.done

    # leap motion模块
    def loadLeap(self, b):
        if b == True:
            # 加载leapmotion
            self.leapController = Leap.Controller()
            self.touchListener = GTouchListener()
            self.leapController.add_listener(self.touchListener)

    def unloadLeap(self):
        self.leapController.remove_listener(self.touchListener)
        # self.passwordFrame.hide()

    def reloadLeap(self):
        self.leapController.add_listener(self.touchListener)
        base.accept('mouse1', zcanvas.press)
        base.accept('mouse1-up', zcanvas.unpress)
        zcanvas.gesture = ''
        self.showNum.enterText('')
        self.showNum['frameColor'] = (0, 1, 1, 0.6)
