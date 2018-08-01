from pandac.PandaModules import *
from math import pi, sin, cos, atan, acos
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
import gc


class GoodsManager(object):
    GoodsIta = {}
    staticGoods = {}

    def __init__(self):
        pass

    def AddGoods(self, Node, CollisionName, Name, Interactive):
        if Interactive:
            self.GoodsIta[Name] = Goods(Node, CollisionName, Name, True)
        else:
            self.staticGoods[Name] = Goods(Node, CollisionName, Name, False)

    def UnLoad(self, name):
        if self.GoodsIta.get(name):
            self.GoodsIta[name].UnLoad()
        if self.staticGoods.get(name):
            self.staticGoods[name].UnLoad()

    def Load(self, name):
        if self.GoodsIta.get(name):
            self.GoodsIta[name].Load()
        if self.staticGoods.get(name):
            self.staticGoods[name].Load()


class Goods(object):
    def __init__(self, Node, CollisionName, Name, Interactive):
        self.Node = Node
        self.state = ""
        self.Node.reparentTo(render)
        self.CollisionName = CollisionName
        self.Name = Name
        self.Interactive = Interactive
        self.CloseHighLight()
        self.DisableTransparency()
        self.Node.hide(BitMask32.bit(1))
        if (self.Name == "Scene1_wallword_2"):
            self.Node.hide()

    def UnLoad(self):
        if self.Node.is_empty():
            return
        texList = self.Node.findAllTextures()
        num = texList.getNumTextures()
        for i in range(num):
            texList[i].releaseAll()
            loader.unloadTexture(texList[i])
        self.Node.detachNode()
        gc.collect()

    def Load(self):
        # self.Node = loader.loadModel(self.modelPathName)
        self.Node.reparentTo(render)

    def CloseHighLight(self):
        self.Node.hide(BitMask32.bit(0))
        # print self.Node, 'close'

    def OpenHighLight(self):
        self.Node.show(BitMask32.bit(0))
        # print self.Node, 'open'

    def SetTransparency(self):
        self.Node.setColorScale((1, 1, 1, 0.8))
        self.Node.setTransparency(TransparencyAttrib.MDual)
        print self.Node, self.Name

    def DisableTransparency(self):
        self.Node.setColorScaleOff()
        self.Node.setTransparency(TransparencyAttrib.MNone)

    def OnClick(self):
        print self.Name, ' click'

    def disable(self):
        self.Interactive = False

    def enable(self):
        self.Interactive = True


class Door(Goods):
    SPEED = 50
    OPEN = 0
    CLOSE = 1
    MOVE = 2
    In = 1
    Out = -1

    def __init__(self, axis, name, pathname, starttheta, Dir):
        node = loader.loadModel(pathname)
        self.doornode = NodePath("doornode")
        self.doornode.reparentTo(render)
        node.reparentTo(self.doornode)
        node.setPos(-axis.x, -axis.y, -axis.z)
        self.doornode.setPos(axis.x, axis.y, axis.z)
        # self.doornode.setSy(1.05)
        # self.doornode.setSz(1.05)
        self.doornode.setH(starttheta + 90 * Dir)
        Goods.__init__(self, self.doornode, [name], name, True)
        self.theta = 90.
        self.starttheta = starttheta
        self.doorstate = self.CLOSE
        self.Dir = Dir
        # self.OpenDoor()

    def OpenDoor(self):
        if (self.doorstate == self.CLOSE):
            self.openDoorSound = loader.loadSfx("res/sounds/open_iron_door.mp3")
            self.openDoorSound.play()
            self.doorstate = self.MOVE
            taskMgr.add(self.open, 'openDoor')

    def CloseDoor(self):
        if (self.doorstate == self.OPEN):
            self.openDoorSound = loader.loadSfx("res/sounds/open_iron_door.mp3")
            self.openDoorSound.play()
            self.doorstate = self.MOVE
            taskMgr.add(self.close, 'closeDoor')

    def open(self, task):
        self.theta -= globalClock.getDt() * self.SPEED
        self.doornode.setH(self.starttheta + self.theta * self.Dir)
        if (self.theta < 0):
            self.theta = 0
            self.doorstate = self.OPEN
            Goods.enable(self)
            return
        return task.cont

    def OnClick(self):
        Goods.OnClick(self)
        Goods.disable(self)
        if self.doorstate == self.CLOSE:
            self.OpenDoor()
        elif self.doorstate == self.OPEN:
            self.CloseDoor()

    def close(self, task):
        self.theta += globalClock.getDt() * self.SPEED
        self.doornode.setH(self.starttheta + self.theta * self.Dir)
        if (self.theta > 90):
            self.theta = 90.
            self.doorstate = self.CLOSE
            Goods.enable(self)
            return
        return task.cont


class GoodsParticle(Goods):
    def __init__(self, name, pos, scale, parent, sort):
        base.enableParticles()
        self.particle = ParticleEffect()
        self.particle.loadConfig(Filename("res/particles/" + name + ".ptf"))
        self.particle.start(render)
        self.particle.setPos(pos)
        self.particle.setBin("fixed", sort)
        self.particle.setDepthWrite(False)
        self.particle.setScale(scale)
        Goods.__init__(self, self.particle, [name], name, False)


class Book(Goods):
    def __init__(self, pathname, name, pos):
        self.Node = loader.loadModel(pathname)
        Goods.__init__(self, self.Node, [name], name, False)
        self.Node.setTransparency(TransparencyAttrib.MDual)
        self.Node.setPos(pos)
        self.Node.hide()
        self.Node.setLightOff()
        # self.burning()

    def burning(self):
        self.Node.show()
        print 'ok'
        taskMgr.add(self.burningtask, 'burningtask')

    def burningtask(self, task):
        print self.Node.getPos()
        if task.time < 10:
            print 'ing'
            self.Node.setSa(1 - task.time / 10.)
            pos = self.Node.getPos()
            pos.z += sin(task.time) * 0.1
            self.Node.setPos(pos)
            return task.cont
        self.Node.detachNode()
        return
