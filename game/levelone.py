from direct.stdpy import threading
from direct.stdpy.threading import currentThread
from pandac.PandaModules import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
import sys, os, math
from math import pi, sin, cos, atan, acos
from direct.actor.Actor import Actor
from role.player import Player
from role.enemy import Enemy
from resourcemanager.GoodsManager import GoodsManager
from bag import Bag
from direct.showbase.ShowBase import ShowBase


class LevelOne(object):

    def __init__(self, m):
        """
        :param m: Menu
        """
        self.levelName = "levelOne"
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
        self.menu.passFrame.show()
        self.node.erosionFrame.show()
        self.node.currentItemFrame.show()
        taskMgr.add(self.waitOne, "waitOne")

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
            self.menu.nextButton['extraArgs'] = [index+1]
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
        print 'b'
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
        else:
            self.node.bag.bagframe.hide()
            self.node.bag.showdisplay.setActive(False)
            self.bagText = self.node.bag.textObject.getText()
            self.node.bag.textObject.setText("")
            self.node.bag.textObject.setWordwrap(0)
            self.bagState = not self.bagState
            self.gameState = ''
            self.node.state = ''
            self.node.initTask()
            # threading.currentThread().join('gameThread')
            props = WindowProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)

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
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene2/Scene2Cat/Scene2_test2.egg'), ["Wall1", "Wall2", "floor"],
                                  "wall", False)
        self.goodmanager.AddGoods(loader.loadModel('res/models/Scene1_Ver6.0_bed_2.egg'), ["bed_box"], "bed_box", True)

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
        self.menu.pauseFrame.show()

    def escapeEvent(self):
        self.menu.pauseFrame.hide()
        self.node.state = ''
        self.node.initTask()
        self.node.erosionFrame.show()
        self.node.currentItemFrame.show()
        base.accept('escape', self.pauseGame)
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
        dlight = DirectionalLight('dlight')
        alight = AmbientLight('alight')
        dlnp = render.attachNewNode(dlight)
        alnp = render.attachNewNode(alight)
        dlight.setColor(LVector4(0.3, 0.3, 0.3, 1))
        alight.setColor(LVector4(0.8, 0.8, 0.8, 1))
        dlnp.setHpr(0, -60, 0)
        render.setLight(dlnp)
        render.setLight(alnp)

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
                                       ColorBlendAttrib.O_fbuffer_alpha)
        self.finalcard.setAttrib(Attrib)

        # This attribute is used to add the results of the post-processing
        # effects to the existing framebuffer image, rather than replace it.
        # This is mainly useful for glow effects like ours.
        # self.finalcard.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))

        # Panda contains a built-in viewer that lets you view the results of
        # your render-to-texture operations.  This code configures the viewer.
        # base.accept("v", base.bufferViewer.toggleEnable)
        # base.accept("V", base.bufferViewer.toggleEnable)
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setLayout("hline")
        base.bufferViewer.setCardSize(0.652, 0)

        # event handling
        base.accept("tab", self.toggleGlow)
        # base.accept("enter", self.toggleDisplay)
        self.glowOn = True

    def limitGlow(self, task):
        if task.time < 5:
            return task.cont
        else:
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
        taskMgr.add(self.limitGlow, "limitGlow")
        if self.node.EROSION + 10 > 100:
            self.node.EROSION = 100
        else:
            self.node.EROSION += 10
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

    def initMania(self):
        base.accept("space", self.mania)
        self.maniaState = False

    def mania(self):
        if self.maniaState:
            return
        self.node.speed *= 1.4
        self.maniaState = True
        if self.node.EROSION + 10 > 100:
            self.node.EROSION = 100
        else:
            self.node.EROSION += 10
        taskMgr.add(self.fadeSpeed, "fadeSpeed")

    def fadeSpeed(self, task):
        if task.time < 10:
            return task.cont
        else:
            self.node.speed /= 1.4
            self.maniaState = False
        return task.done