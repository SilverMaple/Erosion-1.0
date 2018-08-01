from direct.stdpy import threading
from direct.stdpy.threading import currentThread
from pandac.PandaModules import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectWaitBar import DirectWaitBar
import sys, os, math
from math import pi, sin, cos, atan, acos
from direct.actor.Actor import Actor
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from game.mission import Mission
from game.missiontwo import MissionTwo
from game.missionthree import MissionThree


class Player(object):
    """
        Player is the main actor in the fps game
    """
    HP = 100
    EROSION = 0
    updateTime = 0
    speed = 10
    FORWARD = Vec3(0, 2, 0)
    BACK = Vec3(0, -1, 0)
    LEFT = Vec3(-1, 0, 0)
    RIGHT = Vec3(1, 0, 0)
    STOP = Vec3(0)
    walk = STOP
    strafe = STOP
    readyToJump = False
    jump = 0
    state = ''
    cameraState = 1
    visionState = 0
    RightButton = 0
    LeftButton = 0
    goodmanager = None
    isInteractive = False
    SLOW = 1
    End = 0
    Begin = 1
    TaskState = End

    def __init__(self, goodmanager, m, g):
        """ inits the player """
        # 6/17
        self.walksound = loader.loadSfx("res/sounds/footstep.mp3")
        self.goodmanager = goodmanager
        self.menu = m
        self.game = g
        self.loadModel()
        self.setUpCamera()
        self.setMouseIcon()
        self.createCollisions()
        self.attachControls()
        self.initSkill()
        self.shoot = Shoot()
        # init mouse update task
        self.initSave()
        self.initTask()
        self.initMission()

    def initMission(self):
        if self.game.levelName == "tutorial":
            self.mission = Mission(self, self.menu)
        elif self.game.levelName == "levelTwo":
            self.mission = MissionTwo(self, self.menu)
        elif self.game.levelName == "levelThree":
            self.mission = MissionThree(self, self.menu)

    def initSave(self):
        self.erosionFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-1, 1, -1, 1), pos=(-1.2, 0, 0))
        self.erosionFrame.hide()
        self.erosionFrame.setScale(.02, 1, .4)
        self.background = OnscreenImage('res/erosion_bar.png', pos=(0, 0, 0), scale=(1, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.erosionFrame)
        # self.erosionBar = DirectWaitBar(value=self.EROSION, pos=(0, 0, 0), barTexture='res/erosion_value.png',
        #                                 relief=None)
        # self.erosionBar.setHpr(0, 0, -90)
        # self.erosionBar.setScale(0.98, 1, 10)
        # self.erosionBar.hide()
        # self.erosionBar.reparentTo(self.erosionFrame)
        self.erosionBar = OnscreenImage('res/erosion_value.png', pos=(0, 0, 0), scale=(1, 1, 1))
        self.erosionBar.setScale(1)
        self.erosionBar.setTransparency(TransparencyAttrib.MAlpha)
        self.erosionBar.reparentTo(self.erosionFrame)

        self.currentItemFrame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-2, 2, -2, 2), pos=(-1.2, 0, .8),
                                            image='res/models/items/injection.png', scale=(.1))
        self.currentItemFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.currentItemFrame.hide()
        # self.currentItemFrame.show()

    def initTask(self):
        if self.TaskState == self.Begin: return
        self.TaskState = self.Begin
        self.state = ''
        self.game.gameState = ''
        self.mouseIconNormal.show()
        taskMgr.add(self.mouseUpdate, "mouse-task")
        taskMgr.add(self.moveUpdate, "move-task")
        taskMgr.add(self.jumpUpdate, 'jump-task')
        taskMgr.add(self.erosionUpdate, "erosion-task")

    def endTask(self):
        if self.TaskState == self.End: return
        self.TaskState = self.End
        self.state = 'pause'
        self.mouseIconWatch.hide()
        self.mouseIconNormal.hide()
        taskMgr.remove('mouse-task')
        taskMgr.remove('move-task')
        taskMgr.remove('jump-task')
        taskMgr.remove('erosion-task')
        # reset update time
        self.updateTime = 5

    def loadModel(self):
        """ make the nodepath for player """
        # self.playerModel = Actor("res/models/ralph", {"run": "res/models/ralph-run", "walk": "res/models/ralph-walk"})
        self.playerModel = Actor("res/models/hitman-model5",
                                 {"walk": "res/models/hitman-walk5", "stand": "res/models/hitman-stand"})
        # self.playerModel = Actor("res/models/hitman2-model", {"walk": "res/models/hitman2-walk", "stand":"res/models/hitman-stand"})
        self.playerModel.setH(180)
        self.playerModel.setZ(0)
        self.playerModel.setScale(1.1)
        # self.playerModel.hide()
        self.node = NodePath("player")
        self.node.reparentTo(render)
        self.playerModel.reparentTo(self.node)
        # self.node.setPos(0, 0, 10)
        self.node.setPos(-250, 265, 0)
        self.node.setHpr(150, 0, 0)
        self.node.setScale(20)
        self.node.hide(BitMask32.bit(0))
        self.node.hide(BitMask32.bit(1))

    def setMouseIcon(self):
        self.mouseIconNormal = OnscreenImage(image="res/mouse/mouse1.png", pos=(0, 1.1, 0))
        self.mouseIconNormal.setTransparency(TransparencyAttrib.MAlpha)
        self.mouseIconNormal.setScale(0.02)
        self.mouseIconNormal.setLightOff()
        self.mouseIconNormal.setSa(0.5)
        self.mouseIconWatch = OnscreenImage(image="res/mouse/mouse2.png", pos=(0, 1.1, 0))
        self.mouseIconWatch.setTransparency(TransparencyAttrib.MAlpha)
        self.mouseIconWatch.setScale(0.05)
        self.mouseIconWatch.setSa(0.5)
        self.mouseIconWatch.setLightOff()
        self.mouseIconNormal.reparentTo(base.camera)
        self.mouseIconWatch.reparentTo(base.camera)
        self.mouseIconWatch.hide()

    def SetMouseModeNormal(self, mode):
        if mode == 'Watch':
            self.mouseIconWatch.show()
            self.mouseIconNormal.hide()
        elif mode == 'Normal':
            self.mouseIconNormal.show()
            self.mouseIconWatch.hide()

    def setUpCamera(self):
        """ puts camera at the players node """
        pl = base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.node)
        base.cam.node().setCameraMask(BitMask32.bit(3))
        self.oldcameraState = 0
        self.cameranewPos = None
        self.cameranewH = None
        self.changeCamera()

    # 6/17
    def createCollisions(self):
        """ create a collision solid and ray for the player """
        cn = CollisionNode('PlayerCollideNode')
        cn.addSolid(CollisionSphere(0, 0, 4, 1))
        solid = self.node.attachNewNode(cn)
        solid.setScale(1, 1, 1)
        solid.setPos(0, 0, 0)
        # solid.show()
        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node, base.drive.node())
        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0, 0, 3)
        ray.setDirection(0, 0, -1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        # solid.show()
        base.cTrav.setRespectPrevTransform(True)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
        # init players Forward Ray
        ForwardSegment = CollisionSegment(0, 2, 0, 0, 20, 0)
        cn = CollisionNode('playerForwardSegment')
        cn.addSolid(ForwardSegment)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = base.camera.attachNewNode(cn)
        # solid.show()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
        # repair cross wall
        ForwardSegment = CollisionSegment(0, -4, 3, 0, 4, 3)
        cn = CollisionNode('PlayerMoveForwardSegment')
        cn.addSolid(ForwardSegment)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        # solid.show()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
        # init play Right Ray
        ForwardSegment = CollisionSegment(-2, 0, 3, 2, 0, 3)
        cn = CollisionNode('PlayerMoveRightSegment')
        cn.addSolid(ForwardSegment)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        # solid.show()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)

    def attachControls(self):
        """ attach key events """
        # base.accept("space", self.__setattr__, ["readyToJump", True])
        # base.accept("space-up", self.__setattr__, ["readyToJump", False])
        self.keyEven = ["s", "s-up", "w", "w-up", "a", "d", "a-up", "d-up", "c", "o", "mouse3", "mouse3-up", "mouse1",
                        "mouse1-up"]
        base.accept("s", self.__setattr__, ["walk", self.STOP])
        base.accept("w", self.__setattr__, ["walk", self.FORWARD])
        base.accept("s", self.__setattr__, ["walk", self.BACK])
        base.accept("s-up", self.__setattr__, ["walk", self.STOP])
        base.accept("w-up", self.__setattr__, ["walk", self.STOP])
        base.accept("a", self.__setattr__, ["strafe", self.LEFT])
        base.accept("d", self.__setattr__, ["strafe", self.RIGHT])
        base.accept("a-up", self.__setattr__, ["strafe", self.STOP])
        base.accept("d-up", self.__setattr__, ["strafe", self.STOP])
        base.accept("c", self.changeCamera)
        base.accept("o", self.doubleVision)
        base.accept("mouse3", self.__setattr__, ["RightButton", 1])
        base.accept("mouse3-up", self.__setattr__, ["RightButton", 0])
        base.accept("mouse1", self.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.__setattr__, ["LeftButton", 0])

    def IgnoreControls(self):
        for name in self.keyEven:
            base.ignore(name)
        print base.getAllAccepting()

    def initSkill(self):
        self.tex = Texture()
        self.tex.setMinfilter(Texture.FTLinear)
        base.win.addRenderTexture(self.tex,
                                  GraphicsOutput.RTMTriggeredCopyTexture)
        self.tex.setClearColor((0, 0, 0, 1))
        self.tex.clearImage()

        # Create another 2D camera. Tell it to render before the main camera.
        self.backcam = base.makeCamera2d(base.win, sort=-10)
        self.background = NodePath("background")
        self.backcam.reparentTo(self.background)
        self.background.setDepthTest(0)
        self.background.setDepthWrite(0)
        self.backcam.node().getDisplayRegion(0).setClearDepthActive(0)

        self.bcard = base.win.getTextureCard()
        self.bcard.reparentTo(base.render2d)
        self.bcard.setTransparency(1)
        self.fcard = base.win.getTextureCard()
        self.fcard.reparentTo(base.render2d)
        self.fcard.setTransparency(1)

        # Add the task that initiates the screenshots.
        taskMgr.add(self.takeSnapShot, "takeSnapShot")

        if base.win.getGsg().getCopyTextureInverted():
            # print("Copy texture is inverted.")
            self.bcard.setScale(1, 1, -1)
            self.fcard.setScale(1, 1, -1)

        self.bcard.hide()
        self.fcard.hide()
        self.nextclick = 0
        self.clickrate = 10000

    def takeSnapShot(self, task):
        if task.time > self.nextclick:
            self.nextclick += 1.0 / self.clickrate
            if self.nextclick < task.time:
                self.nextclick = task.time
            base.win.triggerCopy()
        return task.cont

    def doubleVision(self):
        self.visionState = 1 - self.visionState
        if self.visionState == 1:
            self.bcard.show()
            self.bcard.setColor(1, 1, 1, 0.60)
            self.bcard.setScale(1.0)
            self.bcard.setPos(-0.05, 0, 0)
            self.bcard.setR(0)
            self.fcard.show()
            self.fcard.setColor(1, 1, 1, 0.60)
            self.fcard.setScale(1.0)
            self.fcard.setPos(0.05, 0, 0)
            self.fcard.setR(0)
            self.clickrate = 10000
            self.nextclick = 0
        else:
            self.bcard.hide()
            self.fcard.hide()

    def changeCamera(self):
        if self.cameraState == 1:
            self.cameraState = 0
        else:
            self.cameraState = 1
        self.setCamera()

    def setCamera(self):
        self.cameraoldPos = base.camera.getPos()
        self.cameraoldNear = base.cam.node().getLens().getNear()
        if self.cameraState == 0:
            self.cameranewPos = Vec3(0, -5, 10)
            pl = base.cam.node().getLens()
            self.cameranewNear = 1
            base.cam.node().setLens(pl)
        elif self.cameraState == 1:
            self.cameranewPos = Vec3(0, -1, 8)
            self.cameranewNear = 1
            # self.playerModel.hide()
            self.playerModel.hide(BitMask32.bit(3))
        elif self.cameraState == 2:
            self.cameranewPos = Vec3(0, -1.5, 8)
            self.cameranewNear = 1
        taskMgr.add(self.updatecamera, "updatecamera")

    def updatecamera(self, task):
        if task.time < 0.2:
            camera.setPos((self.cameraoldPos * (0.2 - task.time) + self.cameranewPos * (task.time)) / 0.2)
            return task.cont
        if self.cameraState == 1:
            self.playerModel.hide(BitMask32.bit(3))
        else:
            self.playerModel.show(BitMask32.bit(3))
        pl = base.cam.node().getLens()
        pl.setNear(self.cameraoldNear)
        base.cam.node().setLens(pl)
        return

    def erosionUpdate(self, task):
        if self.EROSION >= 100:
            self.mission.end("endA")
            return
        if self.EROSION >= 80:
            self.visionState = 0
            self.doubleVision()
        else:
            self.visionState = 1
            self.doubleVision()
        # self.erosionBar['value'] = self.EROSION
        self.erosionBar.setScale(1, 1, self.EROSION / 100)
        self.erosionBar.setPos(0, 0, -1 + self.EROSION / 100)
        if task.time > self.updateTime:
            self.EROSION = math.pow(2, (self.EROSION / 20 - 1)) / 6 + self.EROSION
            # print task.time, 'time'
            # print self.EROSION
            self.updateTime += 10
            # print self.updateTime
        return task.cont

    def erosionUpdateTemp(self):
        if self.EROSION >= 100:
            if self.game.levelName == 'levelThree':
                self.mission.chessBoard.hide()
            self.mission.end("endA")
            return
        if self.EROSION >= 80:
            self.visionState = 0
            self.doubleVision()
        else:
            self.visionState = 1
            self.doubleVision()
        # self.erosionBar['value'] = self.EROSION
        self.erosionBar.setScale(1, 1, self.EROSION / 100)
        self.erosionBar.setPos(0, 0, -1 + self.EROSION / 100)

    def mouseUpdate(self, task):
        """ this task updates the mouse """
        if self.state == '':
            md = base.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            if base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2):
                self.node.setH(self.node.getH() - (x - base.win.getXSize() / 2) * 0.1)
                base.camera.setP(base.camera.getP() - (y - base.win.getYSize() / 2) * 0.1)
                if (base.camera.getP() < -45.): base.camera.setP(-45)
                if (base.camera.getP() > 45.): base.camera.setP(45)

        if self.RightButton == 1:
            self.shoot.MouseDown(self.node)
            self.EROSION += 5
            self.RightButton = 0

        # check Interactive Goods
        nearest = 1000.0
        goods = None
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            IntoName = entry.getIntoNode().getName()
            FromName = entry.getFromNode().getName()
            if FromName == 'playerForwardSegment':
                if entry.getSurfacePoint(base.camera).getY() < nearest:
                    nearest = entry.getSurfacePoint(base.camera).getY()
                    goods = self.goodmanager.GoodsIta.get(IntoName)
        if goods and goods.Interactive == True:
            # print goods.Name
            self.SetMouseModeNormal('Watch')
            self.isInteractive = True
            self.currentInteract = goods
        else:
            self.SetMouseModeNormal('Normal')
            self.isInteractive = False
            self.currentInteract = None

        if self.LeftButton == 1 and self.isInteractive:
            print 'trigger interactive event'
            print goods.Name
            self.mission.interactiveWith(goods)

        return task.cont

    def moveUpdate(self, task):
        """ this task makes the player move """
        # move where the keys set it
        # print self.node.getPos()
        nearestForward = 1000.0
        nearestRight = 1000.0
        RightEntry = None
        ForwardEntry = None
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            IntoName = entry.getIntoNode().getName()
            FromName = entry.getFromNode().getName()
            if FromName == 'PlayerMoveForwardSegment' and (
                        IntoName != 'PlayerCollideNode'):
                if entry.getSurfacePoint(self.node).getY() < nearestForward:
                    nearestForward = entry.getSurfacePoint(self.node).getY()
                    ForwardEntry = entry
            if FromName == 'PlayerMoveRightSegment' and (
                        IntoName != 'PlayerCollideNode'):
                if abs(entry.getSurfacePoint(self.node).getX()) < nearestRight:
                    nearestRight = abs(entry.getSurfacePoint(self.node).getX())
                    RightEntry = entry
        if nearestForward < 2 and nearestForward > -2:
            self.SLOW = abs(nearestForward) * 0.2
            self.node.setPos(self.node.getPos() + ForwardEntry.getSurfaceNormal(render))
        else:
            self.SLOW = 1
        if nearestRight < 2:
            self.node.setPos(self.node.getPos() + RightEntry.getSurfaceNormal(render))
        if (nearestForward < 0 and nearestForward > -5.) or nearestRight < 5:
            if self.cameraState == 0:
                self.cameraState = 2
                self.setCamera()
        else:
            if self.cameraState == 2:
                self.cameraState = 0
                self.setCamera()

        if self.state == '':
            self.walksound.setLoop(False)
            #self.walksound.stop()        	
            if ((self.walk == self.FORWARD) and
                    (self.playerModel.getAnimControl('walk').isPlaying() == False)):
                self.walksound.setLoop(True)
                self.walksound.setVolume(0.5)
                self.walksound.play()
                self.playerModel.getAnimControl('walk').play()

            elif self.walk == self.STOP and self.playerModel.getAnimControl('stand').isPlaying() == False:
                self.playerModel.getAnimControl('stand').play()
                self.playerModel.getAnimControl('walk').stop()
                self.walksound.setLoop(False)
                self.walksound.stop()
                if self.strafe == LVector3f(-1, 0, 0) or self.strafe == LVector3f(1, 0, 0):
                    self.walksound.setLoop(True)
                    # self.walksound.setVolume(0.5)
                    self.walksound.play()
                elif self.strafe == LVector3f(0, 0, 0):
                    self.walksound.setLoop(False)
                    self.walksound.stop()
            #elif self.walk == self.BACK:
                #self.walksound.setLoop(True)
                #self.walksound.setVolume(0.5)
                #self.walksound.play()

            self.node.setFluidPos(self.node, self.walk * globalClock.getDt() * self.speed * self.SLOW)
            self.node.setFluidPos(self.node, self.strafe * globalClock.getDt() * self.speed * self.SLOW)
        return task.cont

    # 6/17
    def jumpUpdate(self, task):
        """ this task simulates gravity and makes the player jump """
        # get the highest Z from the down casting ray
        highestZ = -100
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            # print entry
            z = entry.getSurfacePoint(render).getZ()
            # if z > highestZ and entry.getFromNode().getName() == 'playerRay' and entry.getIntoNode().getName() != "PlayerCollideNode":
            if z > highestZ and entry.getFromNode().getName() == 'playerRay' and entry.getIntoNode().getName() == "floor":
                highestZ = z
                # print highestZ
        # gravity effects and jumps
        self.node.setZ(self.node.getZ() + self.jump * globalClock.getDt() * 600)
        self.jump -= 1 * globalClock.getDt()
        if highestZ > self.node.getZ():
            self.jump = 0
            self.node.setZ(highestZ)
            if self.readyToJump:
                self.jump = 1
        return task.cont


class Shoot(object):
    nodeGroundHandler = None
    TwoBullet = None
    LastShoot = 0
    Player = None

    def __init__(self):
        self.nodeGroundHandler = CollisionHandlerQueue()
        self.TwoBullet = [Bullet(self.nodeGroundHandler, 'First'), Bullet(self.nodeGroundHandler, 'Second')]
        self.loadPortalshader()
        self.MoveUpdateOn = False

    def loadPortalshader(self):
        self.PortalShader = loader.loadShader("shaders/PortalShader.sha")
        PortalBuffer = base.win.makeTextureBuffer("Portalscene", 1024, 768)
        PortalBuffer.setSort(-3)
        PortalBuffer.setClearColor(LVector4(0, 0, 0, 1))
        self.PortalCamera = base.makeCamera(PortalBuffer, lens=base.cam.node().getLens())
        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setShader(self.PortalShader)
        self.PortalCamera.node().setInitialState(tempnode.getState())
        self.PortalCamera.node().setCameraMask(BitMask32.bit(1))
        self.finalcard = PortalBuffer.getTextureCard()
        self.finalcard.reparentTo(render2d)
        Attrib = ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.O_incoming_alpha,
                                       ColorBlendAttrib.O_incoming_alpha)
        self.finalcard.setAttrib(Attrib)
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setLayout("hline")
        base.bufferViewer.setCardSize(0.652, 0)
        render.setShaderInput("time", 1, 0, 0, 0)
        render.setShaderInput("time", 1, 0, 0, 0)

    def moveUpdate(self, task):
        if self.TwoBullet[0].isMove(): self.TwoBullet[0].MoveUpdate()
        if self.TwoBullet[1].isMove(): self.TwoBullet[1].MoveUpdate()
        self.nodeGroundHandler.sortEntries()
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            IntoName = entry.getIntoNode().getName()
            FromName = entry.getFromNode().getName()
            print FromName, IntoName
            if IntoName == "wall1" or IntoName == "wall2" or IntoName == "wall":
                if FromName == 'First' and self.TwoBullet[0].isMove():
                    distance = entry.getSurfacePoint(self.TwoBullet[0].shoot).y
                    if distance > 500: break
                    self.TwoBullet[0].HitPosition = entry.getSurfacePoint(render)
                    z = self.TwoBullet[0].HitPosition.z
                    # if z < 70: z = 70
                    # if z > 400: z = 400
                    self.TwoBullet[0].HitPosition.z = z
                    # print self.TwoBullet[0].HitPosition
                    self.TwoBullet[0].HitNormal = entry.getSurfaceNormal(render)
                    self.TwoBullet[0].SetStop()
                    length = self.TwoBullet[1].HitPosition - self.TwoBullet[0].HitPosition
                    L = length.x * length.x + length.y * length.y + length.z * length.z
                    if L < 10000: self.TwoBullet[1].Disappera()
                if FromName == 'Second' and self.TwoBullet[1].isMove():
                    distance = entry.getSurfacePoint(self.TwoBullet[1].shoot).y
                    if distance > 500: break
                    self.TwoBullet[1].HitPosition = entry.getSurfacePoint(render)
                    z = self.TwoBullet[1].HitPosition.z
                    # if z < 70: z = 70
                    # if z > 400: z = 400
                    self.TwoBullet[1].HitPosition.z = z
                    # print self.TwoBullet[1].HitPosition
                    self.TwoBullet[1].HitNormal = entry.getSurfaceNormal(render)
                    self.TwoBullet[1].SetStop()
                    length = self.TwoBullet[1].HitPosition - self.TwoBullet[0].HitPosition
                    L = length.x * length.x + length.y * length.y + length.z * length.z
                    if L < 10000: self.TwoBullet[0].Disappera()
            else:
                if FromName == 'First' and self.TwoBullet[0].isMove(): self.TwoBullet[0].Disappera()
                if FromName == 'Second' and self.TwoBullet[1].isMove(): self.TwoBullet[1].Disappera()
        # if
        if self.TwoBullet[0].NeedCheckPos == True: self.TwoBullet[0].checkPosition()
        if self.TwoBullet[1].NeedCheckPos == True: self.TwoBullet[1].checkPosition()

        if self.TwoBullet[0].isHit() and self.TwoBullet[1].isHit():
            self.ActivePortal()
            self.MoveUpdateOn = False
            return
        if not self.TwoBullet[0].isMove() and not self.TwoBullet[1].isMove():
            self.MoveUpdateOn = False
            return
        if task.time > 20.:
            self.MoveUpdateOn = False
            return
        return task.cont

    def MouseDown(self, Player):
        self.Player = Player

        Update = False
        if (not self.TwoBullet[0].isMove() and not self.TwoBullet[1].isMove()):
            Update = True
        if not self.TwoBullet[self.LastShoot].isMove():
            self.TwoBullet[self.LastShoot].SetMove()
        self.TwoBullet[self.LastShoot].Instance(Player)
        self.LastShoot = 1 - self.LastShoot
        self.nodeGroundHandler.clearEntries()
        if (Update == True):
            self.ClosePortal()
            if self.MoveUpdateOn == False:
                self.MoveUpdate = True
                taskMgr.add(self.moveUpdate, 'Forward')

    def ActivePortal(self):
        print 'Active'
        self.TwoBullet[0].ActivePortal()
        self.TwoBullet[1].ActivePortal()
        self.finalcard.reparentTo(render2d)
        taskMgr.add(self.PortalUpdate, 'Portal')

    def ClosePortal(self):
        print 'Close'
        self.TwoBullet[0].ClosePortal()
        self.TwoBullet[1].ClosePortal()
        self.finalcard.reparentTo(hidden)
        taskMgr.remove('Portal')

    # def PortalUpdate(self, task):
    #     for i in range(self.nodeGroundHandler.getNumEntries()):
    #         entry = self.nodeGroundHandler.getEntry(i)
    #         IntoName = entry.getIntoNode().getName()
    #         FromName = entry.getFromNode().getName()
    #         if IntoName == 'PlayerCollideNode':
    #             if FromName == 'First':
    #                 self.Player.setPos(self.TwoBullet[1].HitPosition + self.TwoBullet[1].HitNormal * 100)
    #                 taskMgr.doMethodLater(5, self.PortalUpdate, 'Portal')
    #                 return
    #             if FromName == 'Second':
    #                 self.Player.setPos(self.TwoBullet[0].HitPosition + self.TwoBullet[0].HitNormal * 100)
    #                 taskMgr.doMethodLater(5, self.PortalUpdate, 'Portal')
    #                 return
    #     return task.cont
    def PortalUpdate(self, task):
        render.setShaderInput("time", task.time, 0, 0, 0)
        # self.TwoBullet[0].Portal.setColorScale((sin(task.time * 0.5) + 2))
        # self.TwoBullet[1].Portal.setColorScale((sin(task.time * 0.5) + 2))
        # self.TwoBullet[0].Portal.setScale((sin(task.time * 0.5) / 2 + 5))
        # self.TwoBullet[1].Portal.setScale((sin(task.time * 0.5) / 2 + 5))
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            IntoName = entry.getIntoNode().getName()
            FromName = entry.getFromNode().getName()
            if IntoName == 'PlayerCollideNode':
                if FromName == 'Firstout':
                    # 6/17
                    newPos = self.TwoBullet[1].HitPosition + self.TwoBullet[1].HitNormal * 30
                    newPos.z -= 40
                    self.Player.setPos(newPos)
                    cos = self.TwoBullet[1].HitNormal.y
                    theta = acos(cos)
                    if self.TwoBullet[1].HitNormal.x > 0: theta = -theta
                    self.Player.setH(theta * 180 / pi)
                    taskMgr.doMethodLater(5, self.PortalUpdate, 'Portal')
                    return
                if FromName == 'Secondout':
                    # 6/17
                    newPos = self.TwoBullet[0].HitPosition + self.TwoBullet[0].HitNormal * 30
                    newPos.z -= 40
                    self.Player.setPos(newPos)
                    cos = self.TwoBullet[0].HitNormal.y
                    theta = acos(cos)
                    if self.TwoBullet[0].HitNormal.x > 0: theta = -theta
                    self.Player.setH(theta * 180 / pi)
                    taskMgr.doMethodLater(5, self.PortalUpdate, 'Portal')
                    return

        return task.cont


class Bullet(object):
    Forward = Vec3(0, 1, 0)
    Start = Vec3(0, 5, 0)
    speed = 1000
    time = 0
    shoot = None
    Move = 0
    Stop = 1
    Hit = 2
    state = Stop
    HitPosition = Vec3(0, 0, 0)
    HitNormal = Vec3(0, 0, 0)

    # CheckPostion = False

    def __init__(self, nodeGroundHandler, name):
        self.name = name
        self.bullet = NodePath("bullet")  # loader.loadModel('res/models/box.egg')
        self.bullet.setScale(1)
        self.shoot = NodePath("shoot")
        self.shoot.setPos(self.Start)
        self.bullet.reparentTo(self.shoot)
        DoorImage = OnscreenImage(image="res/portal/door.png", pos=(0, -2, 0), scale=(8.8, 1, 14.2))
        DoorImage.setTransparency(TransparencyAttrib.MAlpha)
        DoorImage.setSa(0.5)
        self.Portal = NodePath("Portal")
        DoorImage.reparentTo(self.Portal)
        self.Portal.setScale(5)
        # forward Segment
        forwardSegment = CollisionRay(0, 0, 0, 0, 1, 0)
        self.cn = CollisionNode(name)
        self.cn.addSolid(forwardSegment)
        self.cn.setFromCollideMask(BitMask32.bit(0))
        self.cn.setIntoCollideMask(BitMask32.allOff())
        self.solid = self.shoot.attachNewNode(self.cn)
        base.cTrav.addCollider(self.solid, nodeGroundHandler)
        # Right Segment
        RightSegment = CollisionSegment(-20, -0.2, 0, 20, -0.2, 0)
        self.cnRight = CollisionNode(name + 'right')
        self.cnRight.addSolid(RightSegment)
        self.cnRight.setFromCollideMask(BitMask32.allOff())
        self.cnRight.setIntoCollideMask(BitMask32.allOff())
        self.solid = self.Portal.attachNewNode(self.cnRight)
        self.RightSegmentCollisionHandlerQueue = CollisionHandlerQueue()
        base.cTrav.addCollider(self.solid, self.RightSegmentCollisionHandlerQueue)
        # self.solid.show()
        # Up Segment
        UpSegment = CollisionSegment(0, -0.2, -15, 0, -0.2, 15)
        self.cnUp = CollisionNode(name + 'up')
        self.cnUp.addSolid(UpSegment)
        self.cnUp.setFromCollideMask(BitMask32.allOff())
        self.cnUp.setIntoCollideMask(BitMask32.allOff())
        self.solid = self.Portal.attachNewNode(self.cnUp)
        # self.solid.show()
        base.cTrav.addCollider(self.solid, self.RightSegmentCollisionHandlerQueue)
        Sphere = CollisionSphere(0, 0, 0, 60)
        self.cnout = CollisionNode(name + 'out')
        self.cnout.addSolid(Sphere)
        self.cnout.setFromCollideMask(BitMask32.bit(0))
        self.cnout.setIntoCollideMask(BitMask32.allOff())
        self.solid = self.shoot.attachNewNode(self.cnout)
        # self.solid.show()
        base.cTrav.addCollider(self.solid, nodeGroundHandler)
        self.NeedCheckPos = False
        self.initParticle()

    def initParticle(self):
        base.enableParticles()
        self.particle = ParticleEffect()
        self.loadParticleConfig("res/particles/light.ptf")

    def loadParticleConfig(self, filename):
        self.particle.cleanup()
        self.particle = ParticleEffect()
        self.particle.loadConfig(Filename(filename))
        self.particle.start(self.bullet)
        self.particle.setPos(0, 0, 0)
        self.particle.setScale(10)

    def Instance(self, Player):
        self.time = 0
        self.Start = Player.getPos()
        self.Start.z += base.camera.getZ() * Player.getScale().z
        self.Start.x += -base.camera.getY() * Player.getScale().x * sin(Player.getH() / 180 * pi)
        self.Start.y += base.camera.getY() * Player.getScale().y * cos(Player.getH() / 180 * pi)
        self.Forward = Vec3(-sin(Player.getH() / 180 * pi) * cos(base.camera.getP() / 180 * pi),
                            cos(Player.getH() / 180 * pi) * cos(base.camera.getP() / 180 * pi),
                            sin(base.camera.getP() / 180 * pi))
        # self.Start += self.Forward * 100.
        self.shoot.setHpr(Player.getH(), base.camera.getP(), 0)
        self.shoot.reparentTo(render)
        self.shoot.setPos(self.Start)

    def MoveUpdate(self):
        self.shoot.setPos(self.Start + self.Forward * self.time * self.speed)
        self.time += globalClock.getDt()

    def Disappera(self):
        self.state = self.Stop
        self.shoot.detachNode()
        self.cn.setFromCollideMask(BitMask32.allOff())

    def isMove(self):
        return self.state == self.Move

    def isHit(self):
        return self.state == self.Hit

    def SetMove(self):
        self.state = self.Move
        self.shoot.reparentTo(render)
        self.bullet.reparentTo(self.shoot)
        self.cn.setFromCollideMask(BitMask32.bit(0))
        self.Portal.detachNode()

    def SetStop(self):
        self.state = self.Hit
        self.NeedCheckPos = True
        self.Portal.reparentTo(self.shoot)
        self.cn.setFromCollideMask(BitMask32.allOff())
        self.bullet.detachNode()
        self.shoot.setHpr(0, 0, 0)
        self.shoot.setPos(self.HitPosition)
        cos = -self.HitNormal.y
        theta = acos(cos)
        if self.HitNormal.x < 0: theta = -theta
        self.Portal.setH(theta * 180 / pi)

    def checkPosition(self):
        self.cnRight.setFromCollideMask(BitMask32.bit(0))
        self.cnUp.setFromCollideMask(BitMask32.bit(0))
        base.cTrav.traverse(render)
        FinalPos = self.shoot.getPos()
        for i in range(self.RightSegmentCollisionHandlerQueue.getNumEntries()):
            entry = self.RightSegmentCollisionHandlerQueue.getEntry(i)
            if entry.getFromNode().getName() == self.name + 'right':
                offset = entry.getSurfacePoint(render) - self.shoot.getPos()
                newPosition = Vec3(0, 0, 0) + offset
                offset.normalize()
                offset *= 36
                newPosition -= offset
                FinalPos += newPosition
            if entry.getFromNode().getName() == self.name + 'up':
                offset = entry.getSurfacePoint(render) - self.shoot.getPos()
                # print offset
                newPosition = Vec3(0, 0, 0) + offset
                offset.normalize()
                offset *= 60
                newPosition -= offset
                FinalPos += newPosition
                # print entry.getSurfacePoint(self.render) - self.
        self.shoot.setPos(FinalPos)
        self.cnRight.setFromCollideMask(BitMask32.allOff())
        self.cnUp.setFromCollideMask(BitMask32.allOff())
        self.NeedCheckPos = False

    def ActivePortal(self):
        self.cnout.setFromCollideMask(BitMask32.bit(0))

    def ClosePortal(self):
        self.cnout.setFromCollideMask(BitMask32.allOff())
