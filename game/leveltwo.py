# -*- coding:utf-8 -*-
from direct.stdpy import threading
from direct.stdpy.threading import currentThread
from pandac.PandaModules import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import sys, os, math
from math import pi, sin, cos, atan, acos
from direct.actor.Actor import Actor
from role.player import Player
from role.enemy import Enemy
from resourcemanager.GoodsManager import GoodsManager, GoodsParticle, Door, Book
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from bag import Bag
from direct.showbase.ShowBase import ShowBase
from role.enemy import *
from save import Save


class LevelTwo(object):
    def __init__(self, m):
        """
        :param m: Menu
        """
        self.levelName = "levelTwo"
        self.gameState = ''
        m.game = self
        self.menu = m
        self.setLight()
        self.loadScene()
        if self.menu.tempPlayer is None:
            self.initCollision()
            self.initPlayer()
        else:
            print 'temp not none'
            self.node = self.menu.tempPlayer
            self.node.node.setPos(-250, 265, 20)
            self.node.game = self
            self.node.initMission()
            self.node.mission.memoryNum = self.menu.tempPlayer.mission.memoryNum
            self.enemy = Enemylevel2(self.node)
        # self.node.node.setPos(-800, 0, 20)
        # self.node.node.setPos(-370, 2800, 25)
        self.node.node.setPos(-700, 0, 25)
        self.node.node.setHpr(-90, 0, 0)
        base.accept("escape", self.pauseGame)
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.mutableMap = {}
        self.glowFilter()
        self.initMania()
        self.finalcard.reparentTo(hidden)
        self.initBag()
        # self.menu.loadState = True
        self.menu.passFrame.show()
        self.node.erosionFrame.show()
        self.node.currentItemFrame.show()
        if not self.menu.skipUseless:
            self.menu.loadState = True
            taskMgr.add(self.waitOne, "waitOne")
        else:
            self.save = Save(self)
            if self.menu.selectedSave == 2:
                self.save.loadFile('gameinfo_2.save')
            elif self.menu.selectedSave == 3:
                self.save.loadFile('gameinfo_3.save')
            self.node.changeCamera()
            self.menu.loadState = True
            self.menu.passFrame.hide()
        self.setupskillpattern()

    def waitOne(self, task):
        if task.time < 1:
            self.menu.passFrame['frameColor'] = (0, 0, 0, 1 - task.time)
            return task.cont
        self.menu.passFrame['frameColor'] = (0, 0, 0, 0)
        self.menu.passFrame.hide()
        self.beginPlot()
        return task.done

    def beginPlot(self):
        self.menu.ocanioDialog.show()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.node.endTask()
        self.nextPlot()

    def nextPlot(self):
        self.menu.ocanioButton['text'] = '刚一踏出房间，房间的门就被重重的锁上了。无论我怎么叫喊，\n' \
                                       '里面都没有回应。我尽可能不去想最糟糕的情况，大概kura不会有什么问题的吧。'
        self.menu.ocanioButton['command'] = self.node.mission.hideOcanio
        self.menu.ocanioButton['extraArgs'] = []

    def initBag(self):
        self.bagState = True
        self.bagText = ""
        if self.menu.tempPlayer is not None:
            self.node.bag = self.menu.tempPlayer.bag
        else:
            self.node.bag = Bag(self.node)
        base.accept("b", self.openBag)

    def openBag(self):
        # print 'b'
        if self.bagState:
            self.node.bag.bagframe.show()
            self.node.bag.showdisplay.setActive(True)
            self.node.bag.textObject.setText(self.bagText)
            self.bagState = not self.bagState
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
            self.menu.selectDialog.hide()
            self.gameState = 'pause'
            self.node.state = 'pause'
            self.node.endTask()
            base.accept('escape', self.openBag)
        else:
            self.node.bag.bagframe.hide()
            self.node.bag.showdisplay.setActive(False)
            self.bagText = self.node.bag.textObject.getText()
            self.node.bag.textObject.setText("")
            self.node.bag.textObject.setWordwrap(0)
            self.bagState = not self.bagState
            props = WindowProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
            self.gameState = ''
            self.node.state = ''
            self.node.initTask()
            base.accept('escape', self.pauseGame)

    def initCollision(self):
        """ create the collision system """
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        base.cTrav.setRespectPrevTransform(True)

    def loadScene(self):
        """ load the self.sceneModel
            must have
            <Group> *something* {
              <Collide> { Polyset keep descend }
            in the egg file
        """
        self.goodmanager = GoodsManager()
        # AddGoods(self,Node,CollisionName,Name,Interactive)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene2/Scene2Cat/Scene2_light.egg'),
                                  ["light"], "light", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene2/Scene2Cat/Scene2_Ver7.0_wall.egg'),
                                  ["Wall", "floor"], "wall", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene2/Scene2Cat/Elevator/dianti.egg'),
                                  ["dianti"], "dianti_box", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene2/Scene2Cat/Elevator/broken_dianti.egg'),
                                  ["broken_dianti"], "broken_dianti_box", True)
        self.goodmanager.GoodsIta['broken_dianti_box'].Node.hide()

        '''
        corridor
        '''
        prefix = 'res/models/Scene2/Scene2Cat/Corridor/Scene2_Ver5.0_'
        self.loadIn(prefix + 'clock_2.egg', "clock_box", True)
        # self.loadIn(prefix + 'Outdoor.egg', "outdoor_box", True)
        self.loadIn(prefix + 'ElectricBox_2.egg', "ElectricBox", True)
        self.loadIn(prefix + 'entrance.egg', "entrance_box", True)
        self.loadIn(prefix + 'picture1.egg', "painting_1", True)
        self.loadIn(prefix + 'picture2.egg', "painting_2", True)
        self.loadIn(prefix + 'picture3.egg', "painting_3", True)
        self.loadIn(prefix + 'picture4.egg', "painting_4", True)
        self.loadIn(prefix + 'picture5.egg', "painting_5", True)
        self.loadIn(prefix + 'picture6.egg', "painting_6", True)
        self.loadIn(prefix + 'picture7.egg', "painting_7", True)
        self.loadIn(prefix + 'picture8.egg', "painting_8", True)
        self.loadIn(prefix + 'picture9.egg', "painting_9", True)
        self.loadIn(prefix + 'picture8_cut.egg', "painting_cut", True)
        self.goodmanager.GoodsIta["painting_cut"].Node.hide()
        self.goodmanager.GoodsIta["outdoor_box"] = Door(Vec3(374.1351, 1973.22, 105.000), "outdoor_box",
                                                           prefix + 'Outdoor.egg', 90, Door.Out)

        '''
        hall
        '''
        prefix = 'res/models/Scene2/Scene2Cat/Hall/Scene2_Ver5.0_'
        self.loadIn(prefix + 'food.egg', 'food_box', True)
        self.loadIn(prefix + 'cake.egg', 'cake_box', True)
        self.loadIn(prefix + 'diary.egg', 'diary_box', True)
        self.loadIn(prefix + 'safe_2.egg', 'safe_box', True)
        self.loadIn(prefix + 'carrot.egg', 'carrot_box', True)
        self.loadIn(prefix + 'window.egg', 'window_box', True)
        self.loadIn(prefix + 'window_broken.egg', 'window_broken_box', True)
        self.goodmanager.GoodsIta['window_broken_box'].Node.hide()
        self.loadIn(prefix + 'biaoyu.egg', 'biaoyu_box', True)
        # self.loadIn(prefix + 'Backdoor.egg', 'backdoor', True)
        # self.loadIn(prefix + 'Frontdoor.egg', 'frontdoor', True)
        self.loadIn(prefix + 'hammer_2.egg', 'hammer_box', True)
        self.loadIn(prefix + 'zhalan_2.egg', 'rabbit_cage', True)
        self.loadIn(prefix + 'vaccine.egg', 'hallvaccine_box', True)
        self.loadIn(prefix + 'refrigerator_2.egg', 'fridge_box', True)

        self.loadIn(prefix + 'rabbit.egg', 'rabbit_box', False)
        self.loadIn(prefix + 'yuanzhuo.egg', 'yuanzhuo_box', False)
        self.loadIn(prefix + 'changzhuo_2.egg', 'changzhuo_box', False)
        self.goodmanager.GoodsIta["Frontdoor"] = Door(Vec3(342.9760, 357.22, 105.000), "Frontdoor",
                                                         prefix + 'Frontdoor.egg', 90, Door.Out)
        self.goodmanager.GoodsIta["Backdoor"] = Door(Vec3(342.9760, 1571.22, 105.000), "Backdoor",
                                                        prefix + 'Backdoor.egg', 90, Door.Out)

        '''
        Outroom
        '''
        prefix = 'res/models/Scene2/Scene2Cat/Outroom/Scene2_Ver5.0_'
        self.loadIn(prefix + 'vase_2.egg', 'vase_box', True)
        self.loadIn(prefix + 'knife.egg', 'knife_box', True)
        self.loadIn(prefix + 'jiazi_2.egg', 'jiazi_box', False)
        self.loadIn(prefix + 'rongqi.egg', 'rongqi_box', False)
        self.loadIn(prefix + 'vaccine.egg', 'vaccine_box', True)
        self.loadIn(prefix + 'lavabo_2.egg', 'lavabo_box', True)
        self.loadIn(prefix + 'mirror.egg', 'mirror_box', True)
        self.loadIn(prefix + 'furnace_2.egg', 'furnace_box', True)
        self.loadIn(prefix + 'bookshelf.egg', 'bookshelf_box', True)
        self.loadIn(prefix + 'xiaozhuozi_2.egg', 'xiaozhuozi_box', False)
        self.goodmanager.staticGoods["infireish"] = GoodsParticle("fireish", (-370, 3183, 25), 16, render,31)
        self.goodmanager.staticGoods["insteam"] = GoodsParticle("steam", (-370, 3183, 50), 5, render,30)
        self.goodmanager.GoodsIta['Scene2_book-beijuji'] = Book(prefix+'beijuji.egg','beijuji',(-350, 3183, 50))
        self.goodmanager.GoodsIta['Scene2_book-beijuji'].Node.setHpr(30, 30, 30)
        for i in range(8):
            name = "outflowers" + str(i+1)
            self.goodmanager.AddGoods(loader.loadModel(prefix + name + '.egg'),
                                      [name], name, False)
            self.goodmanager.staticGoods[name].Node.setTwoSided(True)
        self.goodmanager.staticGoods['outflowers7'].Node.hide()
        self.goodmanager.staticGoods['outflowers8'].Node.hide()
        self.mirrorShader = loader.loadShader("shaders/mirrorShader.sha")
        self.goodmanager.GoodsIta['mirror_box'].Node.setShader(self.mirrorShader)
        # self.goodmanager.GoodsIta['mirror_box'].Node.setTwoSided(True)
        self.mirror(self.goodmanager.GoodsIta['mirror_box'].Node)

        '''
        Inroom
        '''
        prefix = 'res/models/Scene2/Scene2Cat/Inroom/Scene2_Ver5.0_'
        self.loadIn(prefix + 'invase.egg', 'invase_box', True)
        self.loadIn(prefix + 'inknife.egg', 'inknife_box', True)
        self.loadIn(prefix + 'injiazi.egg', 'injiazi_box', False)
        self.loadIn(prefix + 'inlavabo.egg', 'inlavabo_box', True)
        self.loadIn(prefix + 'inrongqi.egg', 'inrongqi_box', False)
        self.loadIn(prefix + 'infurnace.egg', 'infurnace_box', True)
        self.loadIn(prefix + 'inbookshelf.egg', 'inbookshelf_box', True)
        self.loadIn(prefix + 'inxiaozhuozi.egg', 'inxiaozhuozi_box', False)
        self.goodmanager.staticGoods["fireish"] = GoodsParticle("fireish", (-370, 2870, 25), 16, render, 31)
        self.goodmanager.staticGoods["steam"] = GoodsParticle("steam", (-370, 2870, 50), 5, render, 30)
        self.goodmanager.GoodsIta['Scene2_book-xijuji'] = Book(prefix + 'inxijuji.egg', 'inxijuji', (-350, 2870, 50))
        self.goodmanager.GoodsIta['Scene2_book-xijuji'].Node.setHpr(30, 30, 30)
        for i in range(8):
            name = "inflowers" + str(i+1)
            self.goodmanager.AddGoods(loader.loadModel(prefix + name + '.egg'),
                                      [name], name, False)
            self.goodmanager.staticGoods[name].Node.hide()
            self.goodmanager.staticGoods[name].Node.setTwoSided(True)
        self.goodmanager.staticGoods['inflowers1'].Node.show()

        self.h2so4_1 = GoodsParticle("H2SO4", (-380, 2270, 136), 6, render, 32)
        self.h2so4_2 = GoodsParticle("smo", (-380, 2270, 110), 5, render, 33)
        self.h2so4_3 = GoodsParticle("surface-1",  (-365, 2270, 100), 10, render, 34)
        self.h2so4_3.particle.setScale(10, 20, 10)

        self.h2so4_4 = GoodsParticle("H2SO4", (-380, 3895.5, 136), 6, render, 32)
        self.h2so4_5 = GoodsParticle("smo", (-380, 3890, 110), 5, render, 33)
        self.h2so4_6 = GoodsParticle("surface-1", (-363, 3890, 100), 10, render, 34)
        self.h2so4_6.particle.setScale(10, 20, 10)

    def loadIn(self, path, name, b):
        self.goodmanager.AddGoods(loader.loadModel(path), [name], name, b)

    def itemCollision(self, model, name, radius):
        nodePath = NodePath(name)
        node = CollisionNode(name)
        node.addSolid(CollisionSphere(20, 0, radius, radius))
        solid = model.attachNewNode(node)
        nodePath.reparentTo(model)
        solid.show()
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, nodePath, base.drive.node())

    def initPlayer(self):
        """ loads the player and creates all the controls for him"""
        self.node = Player(self.goodmanager, self.menu, self)
        # self.enemy = Enemy(self.node)
        self.enemy = Enemylevel2(self.node)
        # self.goodmanager.GoodsIta["enemy"] = Enemy(self.node)
        # self.goodmanager.GoodsIta["enemy"].state = 1

    def pauseGame(self):
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.menu.selectDialog.hide()
        self.gameState = 'pause'
        self.node.state = 'pause'
        self.node.endTask()
        self.node.erosionFrame.hide()
        self.node.currentItemFrame.hide()
        base.accept('escape', self.escapeEvent)
        base.accept('b', self.menu.nothing)
        self.menu.pauseFrame.show()

    def escapeEvent(self):
        self.menu.pauseFrame.hide()
        self.node.state = ''
        self.node.initTask()
        self.node.erosionFrame.show()
        self.node.currentItemFrame.show()
        base.accept('escape', self.pauseGame)
        base.accept('b', self.openBag)
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

    def mirror(self,tex):
        self.mirrorBuffer = base.win.makeTextureBuffer("mirror", 512, 512)
        print 'mirrorBuffer',self.mirrorBuffer
        self.mirrorBuffer.setSort(-3)
        self.mirrorBuffer.setClearColor(LVector4(0, 0, 0, 1))
        print base.cam.node().getLens()
        self.mirrorCamera = base.makeCamera(self.mirrorBuffer)
        self.mirrorCamera.reparentTo(render)
        self.mirrorCamera.setPos((424,3080,104. ))
        self.mirrorCamera.setH(180)
        pl = self.mirrorCamera.node().getLens()
        pl.setFov(90)
        pl.setNear(100)
        self.mirrorCamera.node().setLens(pl)

        self.finalcard = self.mirrorBuffer.getTexture()
        tex.setTexture(self.finalcard,1)
        # self.UnLoadmirror()

    def UnLoadmirror(self):
        self.mirrorBuffer.getEngine().removeWindow(self.mirrorBuffer)
        self.mirrorBuffer = None
        self.mirrorCamera = None

    def makeFilterBuffer(self, srcbuffer, name, sort, prog):
        blurBuffer = base.win.makeTextureBuffer(name, 512, 512)
        blurBuffer.setSort(sort)
        blurBuffer.setClearColor(LVector4(1, 0, 0, 1))
        blurCamera = base.makeCamera2d(blurBuffer)
        blurScene = NodePath("new Scene")
        blurCamera.node().setScene(blurScene)
        shader = loader.loadShader(prog)
        card = srcbuffer.getTextureCard()
        card.reparentTo(blurScene)
        card.setShader(shader)
        return blurBuffer

    def glowFilter(self):
        glowShader = loader.loadShader("shaders/glowShader.sha")
        # dlight = DirectionalLight('dlight')
        # alight = AmbientLight('alight')
        # dlnp = render.attachNewNode(dlight)
        # alnp = render.attachNewNode(alight)
        # dlight.setColor(LVector4(0.3, 0.3, 0.3, 1))
        # alight.setColor(LVector4(0.8, 0.8, 0.8, 1))
        # dlnp.setHpr(0, -60, 0)
        # render.setLight(dlnp)
        # render.setLight(alnp)

        # create the glow buffer. This buffer renders like a normal scene,
        # except that only the glowing materials should show up nonblack.
        glowBuffer = base.win.makeTextureBuffer("Glow scene", 1024, 768)
        glowBuffer.setSort(-3)
        glowBuffer.setClearColor(LVector4(0, 0, 0, 1))

        # We have to attach a camera to the glow buffer. The glow camera
        # must have the same frustum as the main camera. As long as the aspect
        # ratios match, the rest will take care of itself.
        self.glowCamera = base.makeCamera(
            glowBuffer, lens=base.cam.node().getLens())

        # Tell the glow camera to use the glow shader
        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setShader(glowShader)
        self.glowCamera.node().setInitialState(tempnode.getState())

        self.glowCamera.node().setCameraMask(BitMask32.bit(0))

        # set up the pipeline: from glow scene to blur x to blur y to main
        # window.
        blurXBuffer = self.makeFilterBuffer(
            glowBuffer, "Blur X", -2, "shaders/XBlurShader.sha")
        blurYBuffer = self.makeFilterBuffer(
            blurXBuffer, "Blur Y", -1, "shaders/YBlurShader.sha")
        self.finalcard = blurYBuffer.getTextureCard()
        self.finalcard.reparentTo(render2d)

        Attrib = ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.O_incoming_alpha,
                                       ColorBlendAttrib.O_incoming_alpha)
        self.finalcard.setAttrib(Attrib)

        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setLayout("hline")
        base.bufferViewer.setCardSize(0.652, 0)

        base.accept("tab", self.toggleGlow)
        self.glowOn = False

    def limitGlow(self, task):
        if task.time < 5:
            return task.cont
        else:
            self.glowOn = False
            self.finalcard.reparentTo(hidden)
            # self.goodmanager.GoodsIta["box"].CloseHighLight()
        return task.done

    def toggleGlow(self):
        self.showskillpattern("eyepattern")
        if self.glowOn:
            return
        self.glowOn = True
        taskMgr.add(self.limitGlow, "limitGlow")
        if self.node.EROSION + 10 > 100:
            self.node.EROSION = 100
        else:
            self.node.EROSION += 10
        self.finalcard.reparentTo(render2d)
        # self.goodmanager.GoodsIta["box"].OpenHighLight()

    def initMania(self):
        base.accept("space", self.mania)
        self.maniaState = False

    def mania(self):
        self.showskillpattern("maniapattern")
        if not self.maniaState:
            self.node.speed *= 1.4
            self.maniaState = True
        if self.node.EROSION + 10 > 100:
            self.node.EROSION = 100
        else:
            self.node.EROSION += 10
        taskMgr.remove("fadeSpeed")
        taskMgr.add(self.fadeSpeed, "fadeSpeed")

    def fadeSpeed(self, task):
        if task.time < 10:
            return task.cont
        else:
            self.node.speed /= 1.4
            self.maniaState = False
        return task.done

    def setupskillpattern(self):
        self.eyepattern = OnscreenImage(image="res/skill_icon/eye-white.png", pos=(-1.2, 1, -0.8))
        self.eyepattern.setTransparency(TransparencyAttrib.MAlpha)
        self.eyepattern.setScale(0.1)
        self.eyepattern.setSa(0.8)
        self.eyepattern.hide()
        self.maniapattern = OnscreenImage(image="res/skill_icon/mania-white.png", pos=(-1.2 + 0.3, 1, -0.8))
        self.maniapattern.setTransparency(TransparencyAttrib.MAlpha)
        self.maniapattern.setScale(0.1)
        self.maniapattern.setSa(0.8)
        self.maniapattern.hide()
        self.screen_patternArray = {}
        self.screen_patternArray["eyepattern"] = [self.eyepattern, False, 5.0, 5.0]
        self.screen_patternArray["maniapattern"] = [self.maniapattern, False, 10.0, 10.]
        self.patterntask = False
        self.patterntaskpretime = 0
        # self.mouseIconNormal.setSa(0.5)

    def showskillpattern(self, patternname):
        self.screen_patternArray[patternname][2] = self.screen_patternArray[patternname][3]
        self.screen_patternArray[patternname][1] = True
        self.screen_patternArray[patternname][0].show()
        if self.patterntask == False:
            taskMgr.add(self.showskillpatterntask, "showskillpatterntask")
            self.patterntask = True

    def showskillpatterntask(self, task):
        num = 0
        for key in self.screen_patternArray:
            if self.screen_patternArray[key][1] == True:
                self.screen_patternArray[key][2] -= globalClock.getDt()
                if self.screen_patternArray[key][2] < 5.:
                    if sin(self.screen_patternArray[key][2] * pi * 5) > 0:
                        self.screen_patternArray[key][0].setSa(0)
                    else:
                        self.screen_patternArray[key][0].setSa(0.8)

                self.screen_patternArray[key][0].setPos(-1.2 + num * 0.3, 1, -0.8)
                if self.screen_patternArray[key][2] < 0:
                    self.screen_patternArray[key][1] = False
                    self.screen_patternArray[key][0].hide()
                    self.screen_patternArray[key][0].setSa(0.8)
                num += 1
        if num > 0:
            return task.cont
        self.patterntask = False
        return

    def setLight(self):
        render.setLightOff()
        alight=AmbientLight('alight')
        alnp=render.attachNewNode(alight)
        alight.setColor(VBase4(0.3,0.3,0.3,1))
        render.setLight(alnp)

        # myFog = Fog("Fog Name")
        # myFog.setColor(0.2,0.5, 0.1)
        # myFog.setExpDensity(0.5)
        # render.setFog(myFog)

        self.lightpivot1 = render.attachNewNode("lightpivot1")
        self.lightpivot1.setPos(-124, 947, 50)
        self.plight1=PointLight('plight1')
        self.plight1.setColor(VBase4(1, 0.5, 0, 1))
        self.temp=LVector3(0.6, 0.08, 0)
        self.plight1.setAttenuation(self.temp)
        plnp1=self.lightpivot1.attachNewNode(self.plight1)
        plnp1.setPos(0,0,50)
        render.setLight(plnp1)

        self.lightpivot2 = render.attachNewNode("lightpivot2")
        self.lightpivot2.setPos(0, 0, 50)
        self.plight2 = PointLight('plight2')
        self.plight2.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.08, 0)
        self.plight2.setAttenuation(self.temp)
        plnp2 = self.lightpivot2.attachNewNode(self.plight2)
        plnp2.setPos(-200, 0, 50)
        render.setLight(plnp2)

        self.lightpivot3 = render.attachNewNode("lightpivot3")
        self.lightpivot3.setPos(52, 2491, 50)
        self.plight3 = PointLight('plight3')
        self.plight3.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.08, 0)
        self.plight3.setAttenuation(self.temp)
        plnp3 = self.lightpivot3.attachNewNode(self.plight3)
        plnp3.setPos(-200, 0, 50)
        render.setLight(plnp3)

        slight = Spotlight('slight')
        slight.setColor(VBase4(0.1, 0.5, 0.1, 1))
        #slight.setAttenuation(LVector3(0.5,0.08,0))
        lens = PerspectiveLens()
        lens.setFov(10)
        slight.setLens(lens)
        slnp = render.attachNewNode(slight)
        slnp.setPos(-811, 3, 0)
        slnp.lookAt(415,10,0)
        # slnp.setPos(0,0,0)
        # slnp.lookAt(0,0,50)
        render.setLight(slnp)
        #render.setShaderAuto()
