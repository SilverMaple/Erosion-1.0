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
from resourcemanager.GoodsManager import GoodsManager, Door
from bag import Bag
from direct.showbase.ShowBase import ShowBase


class Game(object):
    def __init__(self, m):
        """
        :param m: Menu
        """
        self.levelName = "tutorial"
        self.gameState = ''
        m.game = self
        self.menu = m
        self.initCollision()
        self.loadScene()
        self.initPlayer()
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
        # self.menu.passFrame.show()
        # self.node.erosionFrame.show()
        # self.node.currentItemFrame.show()
        # taskMgr.add(self.waitOne, "waitOne")
        self.maniaSound = loader.loadSfx("res/sounds/Darkness3.mp3")
        self.setupskillpattern()
        self.SetLight()
        if not self.menu.skipUseless:
            self.initVideo()
            self.attachControls()
            self.IgnoreControls()

    def IgnoreControls(self):
        for name in self.keyEven:
            base.ignore(name)
        print base.getAllAccepting()

    def attachControls(self):
        self.keyEven = ["tab", 'escape', 'b', 'space']
        base.accept('b', self.openBag)
        base.accept("tab", self.toggleGlow)
        base.accept("escape", self.pauseGame)
        base.accept('space', self.mania)

    def initVideo(self):
        self.node.endTask()
        media_file = "res/videos/begining.avi"
        self.tex = MovieTexture("preVideo")
        success = self.tex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("preVideo Card")
        # cm.setFrameFullscreenQuad()
        # cm.setFrame(-1.3, 1.3, -1, 1)
        cm.setFrame(-1.2, 1.2, -.95, .95)

        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.tex)
        self.card = NodePath(cm.generate())
        self.card.reparentTo(base.render2d)
        self.card.setTexture(self.tex)
        self.videoSound = loader.loadSfx(media_file)
        self.tex.synchronizeTo(self.videoSound)
        self.videoSound.play()

        taskMgr.add(self.playVideo, 'playGameVideo')

    def playVideo(self, task):
        if self.videoSound.status() != AudioSound.PLAYING:
            self.videoSound.stop()
            self.menu.soundMgr.setMusicVolume(0)
            self.menu.musicVolume = 0
            self.card.hide()
            # self.menu.soundMgr.playMusic('bgm1.mp3')
            self.menu.passFrame.show()
            self.node.erosionFrame.show()
            self.node.currentItemFrame.show()
            taskMgr.add(self.waitOne, "waitOne")
            self.attachControls()
            self.node.initTask()
            return task.done
        return task.cont

    def waitOne(self, task):
        if task.time < 2:
            self.menu.passFrame['frameColor'] = (0, 0, 0, 1 - task.time)
            return task.cont
        self.menu.passFrame['frameColor'] = (0, 0, 0, 0)
        self.menu.passFrame.hide()
        self.beginPlot()
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
            # threading.currentThread().join('gameThread')

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

        # self.goodmanager.AddGoods(loader.loadModel('res/models/Scene3/Scene3_Ver3.0.egg'), ["Wall1", "Wall2", "floor"],
        # #                           "wall", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver7.0_wall.egg'), ["Wall1", "Wall2", "floor"],
                                  "wall", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_bed_2.egg'), ["bed_box"], "bed_box", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_bookshelf.egg'), ["bookshelf_box"],
                                  "bookshelf_box", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_box.egg'), ["box"], "box", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_light.egg'), ["light"], "light", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_chair1.egg'), ["chair1"], "chair1",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_chair2.egg'), ["chair2"], "chair2",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_chair3.egg'), ["chair3"], "chair3",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_chair4.egg'), ["chair4"], "chair4",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_desk2.egg'), ["desk2"], "desk2",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_desk3.egg'), ["desk3_2"], "desk3_2",
                                  False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_matong.egg'), ["matong_box3"],
                                  "matong_box3", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_xishoupen.egg'), ["xishoupen"],
                                  "xishoupen", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_yaoshui.egg'), ["yaoshui"], "yaoshui",
                                  True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Exit.egg'), ["Scene1_Exit"], "Scene1_Exit",
                                  True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_wallword_1.egg'), ["Scene1_wallword_1"],
                                  "Scene1_wallword_1", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_wallword_2.egg'), ["Scene1_wallword_2"],
                                  "Scene1_wallword_2", True)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_MusicBox.egg'), ["MusicBox"], "MusicBox",
                                  True)
        self.goodmanager.GoodsIta["toilet_door"] = Door(Vec3(305, -762.5, 100), "toilet_door",
                                                        'res/models/Scene1_Ver6.0_toilet_door.egg', 0, Door.In)
        self.goodmanager.GoodsIta["yaoshui"].Node.setPos(0, -350, 0)
        self.goodmanager.GoodsIta['MusicBox'].Node.setPos(400, 200, 90)
        self.goodmanager.GoodsIta['MusicBox'].Node.setHpr(-90, 0, 0)
        self.goodmanager.GoodsIta['MusicBox'].Node.setScale(1.5)

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
        self.goodmanager.GoodsIta["enemy"] = Enemy(self.node)
        self.goodmanager.GoodsIta["enemy"].state = 1

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

    def SetLight(self):
        render.setLightOff()
        alight = AmbientLight('alight')
        alnp = render.attachNewNode(alight)
        alight.setColor(LVector4(0.1, 0.1, 0.1, 1))
        #render.setLight(alnp)
        plight = PointLight('plight')
        plight.setColor(VBase4(3,3, 3, 1))
        plight.setAttenuation(Point3(0.1,0.1, 0))
        plnp = render.attachNewNode(plight)
        plnp.setPos(0, 0, 200)
        render.setLight(plnp)
        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        plight.setAttenuation(Point3(0.10, 0.1, 0))
        plnp = render.attachNewNode(plight)
        plnp.setPos(333, -900, 217)
        render.setLight(plnp)
        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        plight.setAttenuation(Point3(0.10, 0.1, 0))
        plnp = render.attachNewNode(plight)
        plnp.setPos((-438.104, 377.736, 400))
        render.setLight(plnp)

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
            self.goodmanager.GoodsIta["box"].CloseHighLight()
            self.goodmanager.GoodsIta["yaoshui"].CloseHighLight()
            self.goodmanager.GoodsIta["MusicBox"].CloseHighLight()
            self.goodmanager.GoodsIta["matong_box3"].CloseHighLight()
            self.goodmanager.GoodsIta["Scene1_Exit"].CloseHighLight()
            self.goodmanager.GoodsIta["Scene1_wallword_1"].CloseHighLight()
            self.goodmanager.GoodsIta["Scene1_wallword_2"].CloseHighLight()
            self.goodmanager.GoodsIta["enemy"].CloseHighLight()
            self.goodmanager.GoodsIta["xishoupen"].CloseHighLight()
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

        self.toggleGlowSound = loader.loadSfx("res/sounds/Raise3.mp3")
        self.toggleGlowSound.play()
        self.finalcard.reparentTo(render2d)
        self.goodmanager.GoodsIta["box"].OpenHighLight()
        self.goodmanager.GoodsIta["yaoshui"].OpenHighLight()
        self.goodmanager.GoodsIta["MusicBox"].OpenHighLight()
        self.goodmanager.GoodsIta["matong_box3"].OpenHighLight()
        self.goodmanager.GoodsIta["Scene1_Exit"].OpenHighLight()
        self.goodmanager.GoodsIta["Scene1_wallword_1"].OpenHighLight()
        self.goodmanager.GoodsIta["Scene1_wallword_2"].OpenHighLight()
        self.goodmanager.GoodsIta["enemy"].OpenHighLight()
        self.goodmanager.GoodsIta["xishoupen"].OpenHighLight()
        # if not self.glowOn:
        #     self.finalcard.reparentTo(hidden)
        #     self.goodmanager.GoodsIta["box"].CloseHighLight()
        #     self.goodmanager.GoodsIta["yaoshui"].CloseHighLight()
        #     self.goodmanager.GoodsIta["MusicBox"].CloseHighLight()
        #     self.goodmanager.GoodsIta["matong_box3"].CloseHighLight()
        #     self.goodmanager.GoodsIta["Scene1_Exit"].CloseHighLight()
        #     self.goodmanager.GoodsIta["Scene1_wallword_1"].CloseHighLight()
        #     self.goodmanager.GoodsIta["Scene1_wallword_2"].CloseHighLight()
        #     self.goodmanager.GoodsIta["enemy"].CloseHighLight()
        #     self.goodmanager.GoodsIta["xishoupen"].CloseHighLight()
        # else:
        #     self.finalcard.reparentTo(render2d)
        #     self.goodmanager.GoodsIta["box"].OpenHighLight()
        #     self.goodmanager.GoodsIta["yaoshui"].OpenHighLight()
        #     self.goodmanager.GoodsIta["MusicBox"].OpenHighLight()
        #     self.goodmanager.GoodsIta["matong_box3"].OpenHighLight()
        #     self.goodmanager.GoodsIta["Scene1_Exit"].OpenHighLight()
        #     self.goodmanager.GoodsIta["Scene1_wallword_1"].OpenHighLight()
        #     self.goodmanager.GoodsIta["Scene1_wallword_2"].OpenHighLight()
        #     self.goodmanager.GoodsIta["enemy"].OpenHighLight()
        #     self.goodmanager.GoodsIta["xishoupen"].OpenHighLight()
        #     self.node.EROSION += 10
        #     #print self.goodmanager.staticGoods['wall'].Node
        #
        # self.glowOn = not (self.glowOn)

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
        self.screen_patternArray["eyepattern"] = [self.eyepattern, False, 5.0]
        self.screen_patternArray["maniapattern"] = [self.maniapattern, False, 5.0]
        self.patterntask = False

    def showskillpattern(self, patternname):
        self.screen_patternArray[patternname][2] = 10.
        self.screen_patternArray[patternname][1] = True
        self.screen_patternArray[patternname][0].show()
        if self.patterntask == False:
            taskMgr.add(self.showskillpatterntask, "showskillpatterntask")

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
