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
from resourcemanager.GoodsManager import GoodsManager, GoodsParticle, Door
from bag import Bag
from direct.showbase.ShowBase import ShowBase
from role.enemy import *


class LevelThree(object):
    def __init__(self, m):
        """
        :param m: Menu
        """
        self.levelName = "levelThree"
        self.gameState = ''
        m.game = self
        self.menu = m
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
            # self.enmey = self.menu.tempPlayer.game.enemy
            self.enemy = Enemylevel2(self.node)
        self.node.node.setPos(200, 5, 20)
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
        self.menu.loadState = True
        self.menu.passFrame.show()
        self.node.erosionFrame.show()
        self.node.currentItemFrame.show()
        taskMgr.add(self.waitOne, "waitOne")
        self.setupskillpattern()
        self.setLight()

    def waitOne(self, task):
        if task.time < 1:
            self.menu.passFrame['frameColor'] = (0, 0, 0, 1 - task.time)
            return task.cont
        self.menu.passFrame['frameColor'] = (0, 0, 0, 0)
        self.menu.passFrame.hide()
        # self.beginPlot()
        return task.done

    def beginPlot(self):
        self.menu.tutorialDialog.show()
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.node.endTask()
        self.nextPlot(0)

    def nextPlot(self, index):
        if index == 1 or index == 0:
            self.menu.nextButton['text'] = self.node.mission.plotText[0][index]
            self.menu.nextButton['command'] = self.nextPlot
            self.menu.nextButton['extraArgs'] = [index + 1]
        elif index == 2:
            self.menu.ocanioButton['text'] = self.node.mission.plotText[0][index]
            self.menu.ocanioButton['command'] = self.nextPlot
            self.menu.ocanioButton['extraArgs'] = [index + 1]
            self.menu.tutorialDialog.hide()
            self.menu.ocanioDialog.show()
        elif index == 3:
            self.menu.nextButton['text'] = self.node.mission.plotText[0][index]
            self.menu.nextButton['command'] = self.node.mission.hideTutorial
            self.menu.nextButton['extraArgs'] = []
            self.menu.tutorialDialog.show()
            self.menu.ocanioDialog.hide()

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
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene3/Scene3Cat/Scene3_Ver3.0_wall.egg'), ["Wall1", "Wall2", "floor"],
                                  "wall", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene3/Scene3Cat/Scene3_light.egg'), ["light_box"], "light_box", False)

        '''
        studyroom
        '''
        prefix = 'res/models/Scene3/Scene3Cat/studyroom/Scene3_'
        self.loadIn(prefix + 'zhuozi.egg', "zhuozi_box", False)
        self.loadIn(prefix + 'biaoyu1.egg', "biaoyu1_box", True)
        self.loadIn(prefix + 'biaoyu2.egg', "biaoyu2_box", True)
        self.loadIn(prefix + 'biaoyu3.egg', "biaoyu3_box", True)
        self.loadIn(prefix + 'vaccine.egg', "vaccine_studyroom_box", True)
        self.loadIn(prefix + 'book_studyroom.egg', "book_studyroom_box", True)
        self.loadIn(prefix + 'bookshelf.egg', "bookshelf_box", True)

        '''
        lab
        '''
        prefix = 'res/models/Scene3/Scene3Cat/lab/Scene3_'
        self.loadIn(prefix + 'desk.egg', 'desk_box', False)
        # self.loadIn(prefix + 'bottle.egg', 'bottle_box', True)
        self.loadIn(prefix + 'emptybottle.egg', 'emptybottle_box', True)
        self.loadIn(prefix + 'biaoyu.egg', 'biaoyu_box', True)
        self.loadIn(prefix + 'labtable.egg', 'labtable_box', False)
        self.loadIn(prefix + 'notebook1.egg', 'notebook1_box', True)
        self.loadIn(prefix + 'notebook2.egg', 'notebook2_box', True)
        self.loadIn(prefix + 'notebook3.egg', 'notebook3_box', True)
        self.loadIn(prefix + 'pool.egg', 'pool_box', True)
        self.goodmanager.GoodsIta['pool_box'].Node.setTwoSided(True)

        '''
        hall
        '''
        prefix = 'res/models/Scene3/Scene3Cat/hall/Scene3_'
        self.loadIn(prefix + 'exit.egg', 'exit_box', True)
        self.loadIn(prefix + 'king.egg', 'king_box', False)
        self.loadIn(prefix + 'rook1.egg', 'rook1_box', False)
        self.loadIn(prefix + 'rook2.egg', 'rook2_box', False)
        self.loadIn(prefix + 'knight.egg', 'knight_box', False)
        self.loadIn(prefix + 'bishop.egg', 'bishop_box', False)
        self.loadIn(prefix + 'chessdesk.egg', 'chessdesk_box', True)
        self.goodmanager.GoodsIta["studydoor_box"] = Door(Vec3(-624.5253, -831.2924, 105.000), "studydoor_box",
                                                        prefix + 'studydoor.egg', 90, Door.Out)
        self.goodmanager.GoodsIta["labdoor_box"] = Door(Vec3(-272.8592, 182.9539, 105.000), "labdoor_box",
                                                        prefix + 'labdoor.egg', 90, Door.Out)
        self.goodmanager.GoodsIta["chessdoor_box"] = Door(Vec3(-837.2316, -684.3346, 105.000), "chessdoor_box",
                                                        prefix + 'chessdoor.egg', 90, Door.Out)

        '''
        chessroom
        '''
        prefix = 'res/models/Scene3/Scene3Cat/chessroom/Scene3_'
        self.loadIn(prefix + 'key.egg', 'key_box', True)
        self.loadIn(prefix + 'zitiao.egg', 'zitiao_box', True)
        self.loadIn(prefix + 'paints.egg', 'paints_box', True)
        self.loadIn(prefix + 'pillar.egg', 'pillar_box', False)
        self.loadIn(prefix + 'midpillar.egg', 'midpillar_box', True)
        self.loadIn(prefix + 'vaccine1.egg', 'vaccine1_box', True)
        self.loadIn(prefix + 'vaccine2.egg', 'vaccine2_box', True)
        self.loadIn(prefix + 'book_chessroom.egg', 'book_chessroom_box', True)

        '''
        elevator
        '''
        prefix = 'res/models/Scene3/Scene3Cat/elevator/Scene3_'
        self.loadIn(prefix + 'leftdianti.egg', 'leftdianti_box', False)
        self.loadIn(prefix + 'rightdianti.egg', 'rightdianti_box', False)
        self.loadIn(prefix + 'diantikuang.egg', 'diantikuang_box', False)
        self.loadIn(prefix + 'elebutton.egg', 'elebutton_box', True)


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
        # self.enemy = Enemylevel2(self.node)
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
        alight=AmbientLight("alight")
        alnp=render.attachNewNode(alight)
        alight.setColor(VBase4(0.1,0.1,0.1,1))
        render.setLight(alnp)

        self.lightpivot1 = render.attachNewNode("lightpivot1")
        self.lightpivot1.setPos(-371, -94, 100)
        self.plight1 = PointLight('plight1')
        self.plight1.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.08, 0)
        self.plight1.setAttenuation(self.temp)
        plnp1 = self.lightpivot1.attachNewNode(self.plight1)
        # plnp1.setPos(0, 0, 50)
        render.setLight(plnp1)
        # render.setShaderAuto()

        self.lightpivot2 = render.attachNewNode("lightpivot2")
        self.lightpivot2.setPos(131, -22, 100)
        self.plight2 = PointLight('plight2')
        self.plight2.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.1, 0)
        self.plight2.setAttenuation(self.temp)
        plnp2 = self.lightpivot2.attachNewNode(self.plight2)
        # plnp1.setPos(0, 0, 50)
        render.setLight(plnp2)

        self.lightpivot3 = render.attachNewNode("lightpivot3")
        self.lightpivot3.setPos(-426, -937, 100)
        self.plight3 = PointLight('plight3')
        self.plight3.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.1, 0)
        self.plight3.setAttenuation(self.temp)
        plnp3 = self.lightpivot3.attachNewNode(self.plight3)
        # plnp1.setPos(0, 0, 50)
        render.setLight(plnp3)

        self.lightpivot4 = render.attachNewNode("lightpivot4")
        self.lightpivot4.setPos(-1313, -532, 100)
        self.plight4 = PointLight('plight3')
        self.plight4.setColor(VBase4(1, 0.5, 0, 1))
        self.temp = LVector3(0.6, 0.1, 0)
        self.plight4.setAttenuation(self.temp)
        plnp4 = self.lightpivot4.attachNewNode(self.plight4)
        # plnp1.setPos(0, 0, 50)
        render.setLight(plnp4)

        slight = PointLight('slight')
        slight.setColor(VBase4(0.1, 0.5, 0.1, 1))
        # # slight.setAttenuation(LVector3(0.5,0.08,0))
        # lens = PerspectiveLens()
        # lens.setFov(10)
        # slight.setLens(lens)
        self.chessdesk=self.goodmanager.GoodsIta["chessdesk_box"].Node
        slnp = self.chessdesk.attachNewNode(slight)
        slnp.setPos(-486,-320,1000)
        # slnp.lookAt(self.goodmanager.GoodsIta["chessdesk_box"].Node)
        self.chessdesk.setLight(slnp)
