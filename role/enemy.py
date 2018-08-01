from direct.stdpy import threading
from direct.stdpy.threading import currentThread
from pandac.PandaModules import *
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
import sys, os, math
from math import pi, sin, cos, atan, acos
from direct.actor.Actor import Actor
from resourcemanager.GoodsManager import Goods
import threading

class Enemy(Goods):
    def __init__(self, node):
        """ inits the player """
        self.loadModel()
        self.createCollisions()
        self.initSound()
        Goods.__init__(self, self.enemy_node, ["enemy"], "enemy", True)
        # self.setAI(node)

    def initSound(self):
        self.heartbeat = base.loader.loadSfx("res/sounds/heartbeat.mp3")
        self.heartbeat.setVolume(1)
        self.heartbeat.setLoop(True)
        self.heartbeat.play()

        self.scream = base.loader.loadSfx("res/sounds/scream.mp3")
        self.scream.setVolume(1)
        self.scream.setLoop(False)
        self.scream.stop()

    def loadModel(self):
        """ make the nodepath for player """
        self.enemy_node = NodePath('enemy')

        self.enemyModel = Actor("res/models/kurasit/kura-sit")
        # self.sword = loader.loadModel("res/models/sword")
        # self.rightHand = self.enemyModel.exposeJoint(None, 'modelRoot', 'RightHand')
        # self.sword.reparentTo(self.rightHand)
        self.enemyModel.setH(90)
        self.enemyModel.setScale(.2)
        self.enemyModel.setZ(0)
        self.enemy_node.reparentTo(render)
        self.enemyModel.reparentTo(self.enemy_node)
        self.enemy_node.setPos(-326, 265, 8)
        self.enemy_node.setScale(5)

    def createCollisions(self):
        """ create a collision solid and ray for the player """
        enemy_cn = CollisionNode("enemy")
        enemy_cn.addSolid(CollisionSphere(0, 0, 3, 3))
        enemy_solid = self.enemyModel.attachNewNode(enemy_cn)
        # enemy_solid.show()

        # base.cTrav.addCollider(enemy_solid, base.pusher)
        # base.pusher.addCollider(enemy_solid, self.enemy_node, base.drive.node())
        # init players floor collisions

        # player_cn.setFromCollideMask(BitMask32.bit(0))
        # player_cn.setIntoCollideMask(BitMask32.allOff())
        # player_solid = self.player_node.attachNewNode(player_cn)
        # self.nodeGroundHandler = CollisionHandlerQueue()
        # base.cTrav.addCollider(player_solid, self.nodeGroundHandler)

    def setAI(self, node):
        self.AIworld = AIWorld(render)
        self.AIchar = AICharacter("enemy", self.enemy_node, 5, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.node = node
        taskMgr.add(self.AIUpdate, "AIUpdate")
        self.enemyModel.loop("walk")
        self.AIbehaviors.wander(50, 0, 100, 1.0)
        self.AIbehaviors.pursue(self.node.playerModel)

        # self.AIbehaviors.obstacleAvoidance(4.0)
        # self.AIworld.addObstacle(sceneModel)

    def AIUpdate(self, task):
        distance = math.hypot(math.fabs(self.enemy_node.getX() - self.node.node.getX()),
                              math.fabs(self.enemy_node.getY() - self.node.node.getY()))
        if distance < 150.0:
            self.AIbehaviors.pauseAi("wander")
            self.AIbehaviors.resumeAi("pursue")
            # print 'heartbeat'
            if self.heartbeat.status() != AudioSound.PLAYING:
                self.heartbeat.setVolume(100)
                self.heartbeat.play()
            if distance < 50:
                self.node.HP -= 0.1
                self.heartbeat.stop()
                self.scream.play()
                # print 'scream'
                # print self.node.HP

        if distance >= 150.0:
            self.AIbehaviors.pauseAi("pursue")
            self.AIbehaviors.resumeAi("wander")
            if self.heartbeat.status() != AudioSound.PLAYING:
                self.heartbeat.setVolume(100)
                self.heartbeat.play()
            # print 'nothing'

        self.AIworld.update()
        return task.cont


class Enemylevel2(Goods):
    # pos = [Point3(415, 10, 4), Point3(437, 93, 4), Point3(657, 85, 4), Point3(425, 412, 4),
    #        Point3(257, 405, 4), Point3(264, 1616, 4), Point3(428, 1623, 4), Point3(420, 2037, 4)]
    # posNode = [LPoint3(298, 2070, 0), LPoint3(298, 2070, 0), LPoint3(-156, 2048, 0),
    #        LPoint3(293, 2869, 0), LPoint3(52, 2875, 0), LPoint3(-135, 2874, 0)]
    posNode = [LPoint3(-45,2094,0),LPoint3(164,2113,0),LPoint3(161,2850,0),LPoint3(-48,2852,0)]
    def __init__(self, node):
        """ inits the player """
        self.node = node
        self.loadModel()
        Goods.__init__(self, self.enemy_node, ["enemylevel2"], "enemylevel2", False)
        self.createCollisions()
        taskMgr.add(self.enter_room_first,"enter_first")
        # self.setupAI()
        self.state=0

    def initState(self,state):
        # if state==0 do nothing
        if state == 1:
            taskMgr.remove("enter_first")
            taskMgr.add(self.leave_room,"leave_room")
            self.setupAI()
        elif state == 2:
            self.setupAI()
            taskMgr.remove("enter_first")
            taskMgr.add(self.enter_room_second,"enter_room_second")
        elif state == 3:
            taskMgr.remove("enter_first")
            self.enemy_node.removeNode()

    def enter_room_first(self,task):
        if(self.node.node.getY()>1973):
            taskMgr.add(self.leave_room,"leave_room")
            # self.setupAI()
            self.node.mission.beginMemory(0, 0)
            self.state=1
            return task.done
        return  task.cont

    def leave_room(self,task):
        if(self.node.node.getY()<1973 and self.node.node.getX()>300):
            taskMgr.add(self.enter_room_second,"enter_room_second")
            return task.done
        return task.cont

    def enter_room_second(self,task):
        if(self.node.node.getY()>1973):
           self.destroyAI()
           self.state=2
           return task.done
        return task.cont

    def loadModel(self):
        """ make the nodepath for player """
        self.enemy_node = NodePath('enemy')

        # self.enemy_player = Actor("res/models/eve",  # Load our animated charachter
        #                         {'walk': "res/models/eve_walk"})
        self.enemy_player = Actor("res/models/kura2.egg",
                                  {'run':"res/models/kura2-run.egg"})
        # self.enemy_player.setH()
        self.enemy_player.setScale(1)
        self.enemy_player.setZ(0)
        self.enemy_node.reparentTo(render)
        self.enemy_player.reparentTo(self.enemy_node)
        self.enemy_node.setPos(-219, 2291, 0)
        self.enemy_node.setScale(5)
        self.pos=self.enemy_node.getPos()

    def createCollisions(self):
        """ create a collision solid and ray for the player """
        enemy_cn = CollisionNode("enemy")
        enemy_cn.addSolid(CollisionSphere(0, 0, 15, 3))
        enemy_solid = self.enemy_player.attachNewNode(enemy_cn)
        enemy_solid.show()
        base.cTrav.addCollider(enemy_solid, base.pusher)
        base.pusher.addCollider(enemy_solid, self.enemy_node, base.drive.node())

        self.segment = CollisionNode("segment")
        self.segment.addSolid(CollisionSegment(self.enemy_node.getPos() + (0, 4, 0), self.node.node.getPos()))
        self.enemy_view = render.attachNewNode(self.segment)
        self.segment.setFromCollideMask(BitMask32.bit(0))
        self.segment.setIntoCollideMask(BitMask32.allOff())
        #self.enemy_view.show()
        self.queue = CollisionHandlerQueue()
        base.cTrav.addCollider(self.enemy_view, self.queue)

        # self.obstacle = CollisionNode("obstacle")
        # self.obstacle_cn = render.attachNewNode(self.obstacle)
        # self.obstacle_queue = CollisionHandlerQueue()
        # self.obstacle.setFromCollideMask(BitMask32.bit(0))
        # self.obstacle.setIntoCollideMask(BitMask32.allOff())
        # self.obstacle_cn.show()
        # base.cTrav.addCollider(self.obstacle_cn, self.obstacle_queue)
        # base.cTrav.traverse(render)

    def setupAI(self):
        self.AIworld = AIWorld(render)
        self.AIchar = AICharacter("enemy", self.enemy_node, 100,500,450 )
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.enemy_player.loop("run")
        self.AIbehaviors.pursue(self.node.node)
        self.loadMusic()
        self.moving=True
        self.rightpos=0
        # timer=threading.Timer(0.5,self.isMoving)
        # timer.start()
        taskMgr.add(self.posUpdate,"posUpdate")
        taskMgr.add(self.AIUpdate, "AIUpdate")
        taskMgr.add(self.segmentUpdate, 'segmentUpdate')

    def destroyAI(self):
        taskMgr.remove("posUpdate")
        taskMgr.remove("AIUpdate")
        taskMgr.remove("segmentUpdate")
        taskMgr.add(self.unloadMusic,"unloadMusic")
        self.AIworld.removeAiChar("enemy")
        self.enemy_node.removeNode()

    def loadMusic(self):
        self.music=loader.loadSfx("res/sounds/pursue.wav")
        self.music.setLoop(True)
        self.music.play()
        base.sfxManagerList[0].update()
    def unloadMusic(self,task):
        volume=task.time*-0.25+1
        self.music.setVolume(volume)
        if(volume<=0):
            self.music.stop()
            return task.done
        return task.cont

    def posUpdate(self,task):
        # if(self.node.node.getY()>1989):
        #     self.destroyAI()
        #     return
        distance=math.hypot(math.fabs(self.enemy_node.getX()-self.node.node.getX()),
                            math.fabs(self.enemy_node.getY()-self.node.node.getY()))
        # print distance
        if(distance<200):
            self.node.EROSION+=0.2
            if(distance<=150):
                self.AIbehaviors.pauseAi("pursue")
                taskMgr.remove("segmentUpdate")
            elif(distance>150):
                self.AIbehaviors.resumeAi("pursue")
                taskMgr.add(self.segmentUpdate,'segmentUpdate')
        return task.cont

    def segmentUpdate(self, task):
        self.segment.clearSolids()
        self.segment.addSolid(CollisionSegment(self.enemy_node.getPos() + (0, 4, 4), self.node.node.getPos()+(0,0,80)))
        if (self.queue.getNumEntries() != 0):
            entry = self.queue.getEntry(0)
            intoName = entry.getIntoNode().getName()
            #print intoName

            if (intoName == "PlayerCollideNode"):
                # print "4"
                self.AIbehaviors.pauseAi("seek")
                self.AIbehaviors.resumeAi("pursue")
            elif (intoName =="wall" or intoName =="floor"):
                if(self.node.node.getY()<2000 and self.enemy_node.getY()>1700 and self.enemy_node.getX()<429):
                    # print "1"
                    self.AIbehaviors.pauseAi("pursue")
                    self.AIbehaviors.resumeAi("seek")
                    self.AIbehaviors.seek((430,2100,0))
                if(self.node.node.getY()<2000 and self.enemy_node.getY()>2000 and self.enemy_node.getX()>=429):
                    # print "2"
                    self.AIbehaviors.pauseAi("seek")
                    self.AIbehaviors.resumeAi("pursue")
                elif (self.node.node.getY() > 288 and self.node.node.getY() < 1700):
                    # if(self.enemy_node.getY()<=2060 and self.enemy_node.getX()):
                    #     self.AIbehaviors.seek
                    if (self.node.node.getY() > 1004):
                        #print "seak 1"
                        self.AIbehaviors.pauseAi("pursue")
                        self.AIbehaviors.resumeAi("seek")
                        self.AIbehaviors.seek(Vec3(342, 1630, 8))
                    elif (self.node.node.getY() <= 1004):
                        #print "seek 2"
                        self.AIbehaviors.pauseAi("pursue")
                        self.AIbehaviors.resumeAi("seek")
                        self.AIbehaviors.seek(Vec3(345, 380, 8))
            elif (intoName == "bookshelf_box"):
                self.AIbehaviors.pauseAi("pursue")
                self.AIbehaviors.resumeAi("seek")
                if(self.node.node.getY()<2606):
                    self.AIbehaviors.seek((68,1823,0))
                elif(self.node.node.getY()>2606):
                    self.AIbehaviors.seek((58,2959,0))
            elif (intoName == "yuanzhuo_box"):
                self.AIbehaviors.pauseAi("pursue")
                self.AIbehaviors.resumeAi("seek")
                if(self.node.node.getY()<865):
                    self.AIbehaviors.seek((77,451,0))
                else:
                    self.AIbehaviors.seek((84,1284,0))

        return task.cont

    def AIUpdate(self, task):
        self.AIworld.update()
        return task.cont


class Enemylevel3(Goods):

    def __init__(self, node):
        """ inits the player """
        self.node = node
        self.loadModel()
        Goods.__init__(self, self.enemy_node1, ["enemyLevel3_1"], "enemyLevel3_1", False)
        self.createCollisions()
        self.setupAI()
        taskMgr.add(self.leave_room, "leaveroom")


    def leave_room(self,task):
        if(self.node.node.getX()>-836):
            self.destroyAI()
            return task.done
        return task.cont

    def loadModel(self):
        """ make the nodepath for player """
        self.enemy_node1= NodePath('enemy1')
        self.enemy_player1 =  Actor("res/models/kura2.egg",
                                  {'run':"res/models/kura2-run.egg"})
        self.enemy_node1.reparentTo(render)
        self.enemy_player1.reparentTo(self.enemy_node1)
        self.enemy_node1.setPos(-929, 6, 0)
        self.enemy_node1.setScale(5)

    def createCollisions(self):
        """ create a collision solid and ray for the player """
        enemy_cn1 = CollisionNode("enemy1")
        enemy_cn1.addSolid(CollisionSphere(0, 0, 15, 4))
        enemy_solid1 = self.enemy_player1.attachNewNode(enemy_cn1)
        enemy_solid1.show()
        base.cTrav.addCollider(enemy_solid1, base.pusher)
        base.pusher.addCollider(enemy_solid1, self.enemy_node1, base.drive.node())




    def setupAI(self):
        self.AIworld = AIWorld(render)
        self.AIchar1 = AICharacter("enemy1", self.enemy_node1, 100,500,450 )
        self.AIworld.addAiChar(self.AIchar1)
        self.AIbehaviors1 = self.AIchar1.getAiBehaviors()
        self.AIbehaviors1.pursue(self.node.node)
        self.enemy_player1.loop("run")



        self.loadMusic()

        # timer=threading.Timer(0.5,self.isMoving)
        # timer.start()
        taskMgr.add(self.posUpdate,"posUpdate")
        taskMgr.add(self.AIUpdate, "AIUpdate")


    def destroyAI(self):
        taskMgr.remove("AIUpdate")
        taskMgr.remove("posUpdate")
        taskMgr.add(self.unloadMusic,"unloadMusic")
        self.AIworld.removeAiChar("enemy1")

        self.enemy_node1.removeNode()


    def loadMusic(self):
        self.music=loader.loadSfx("res/sounds/pursue.wav")
        self.music.setLoop(True)
        self.music.play()
        base.sfxManagerList[0].update()
    def unloadMusic(self,task):
        volume=task.time*-0.25+1
        self.music.setVolume(volume)
        if(volume<=0):
            self.music.stop()
            return task.done
        return task.cont

    def posUpdate(self,task):
        distance1=math.hypot(math.fabs(self.enemy_node1.getX()-self.node.node.getX()),
                            math.fabs(self.enemy_node1.getY()-self.node.node.getY()))
        if(distance1<200):
            self.node.EROSION+=0.2
            if(distance1<=150):
                self.AIbehaviors1.pauseAi("pursue")
            elif(distance1>150):
                self.AIbehaviors1.resumeAi("pursue")

        return task.cont

    def AIUpdate(self, task):
        self.AIworld.update()
        return task.cont
