# -*- coding=utf-8 -*-
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3, BitMask32
from direct.gui.OnscreenText import OnscreenText
#from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
#from direct.directbase.DirectStart import *
from pandac.PandaModules import *

import sys

# First we define some constants for the colors
BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
HIGHLIGHT = (0, 1, 1, 1)
PIECEBLACK = (.15, .15, .15, 1)

# Now we define some helper functions that we will need later

# This function, given a line (vector plus origin point) and a desired z value,
# will give us the point on the line where the desired z value is what we want.
# This is how we know where to position an object in 3D space based on a 2D mouse
# position. It also assumes that we are dragging in the XY plane.
#
# This is derived from the mathematical of a plane, solved for a given point
def PointAtZ(z, point, vec):
    return point + vec * ((z - point.getZ()) / vec.getZ())

# A handy little function for getting the proper position for a given square1
def SquarePos(i):
    return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0)

# Helper function for determining whether a square should be white or black
# The modulo operations (%) generate the every-other pattern of a chess-board
def SquareColor(i):
    if (i + ((i // 8) % 2)) % 2:
        return BLACK
    else:
        return WHITE


class ChessboardDemo():
    def __init__(self,mission):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        self.mission=mission
        self.player=mission.player
        self.menu=mission.menu
        self.state=0
        self.frame=DirectFrame(frameColor=(0.1,0.1,0.1,0.5),frameSize=(-2,2,-2,2),pos=(0,0,0))
        self.frame.hide()
        self.dr2=base.win.makeDisplayRegion()
        #self.dr2.setActive(False)
        # self.frame.attachNewNode(self.dr2.node())
        #self.dr2.setActive(False)
        self.dr2.setClearColorActive(True)
        self.dr2.setClearColor(VBase4(0.1,0.1,0.1,1))
        self.dr2.setClearDepthActive(True)
        # base.win.setClearColor(VBase4(0.1,0.1,0.1,1))
        # base.win.setClearDepthActive()
        # base.win.setClearDepth(1)
        self.render2=NodePath("render2")
        self.camNode =Camera("cam2")
        self.cam2=self.render2.attachNewNode(self.camNode)
        self.dr2.setCamera(self.cam2)
        self.cam2.setPosHpr(0, -18, 10, 0, -30, 0)

         # Escape quits
        base.disableMouse()  # Disble mouse camera control
        # camera.setPosHpr(0, -12, 8, 0, -35, 0)  # Set the camera
        self.setupLights()  # Setup default lighting

        # Since we are using collision detection to do picking, we set it up like
        # any other collision detection system with a traverser and a handler
        self.picker = CollisionTraverser()  # Make a traverser
        self.pq = CollisionHandlerQueue()  # Make a handler
        # Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay')
        # Attach that node to the camera since the ray will need to be positioned
        # relative to it
        # self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNP = self.cam2.attachNewNode(self.pickerNode)
        # Everything to be picked will use bit 1. This way if we were doing other
        # collision we could separate it
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()  # Make our ray
        # Add it to the collision node
        self.pickerNode.addSolid(self.pickerRay)
        # Register the ray as something that can cause collisions
        self.picker.addCollider(self.pickerNP, self.pq)
        # self.picker.showCollisions(render)

        # Now we create the chess board and its pieces

        # We will attach all of the squares to their own root. This way we can do the
        # collision pass just on the squares and save the time of checking the rest
        # of the scene
        self.squareRoot = self.render2.attachNewNode("squareRoot")

        # For each square
        self.squares = [None for i in range(64)]
        self.pieces = [None for i in range(64)]
        for i in range(64):
            # Load, parent, color, and position the model (a single square
            # polygon)
            # self.squares[i] = loader.loadModel("../res/models/Scene3/Scene3Cat/hall/square")
            self.squares[i] = loader.loadModel("res/models/Scene3/Scene3Cat/hall/square")
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(SquarePos(i))
            self.squares[i].setColor(SquareColor(i))
            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

            # We will use this variable as a pointer to whatever piece is currently
            # in this square

        # The order of pieces on a chessboard from white's perspective. This list
        # contains the constructor functions for the piece classes defined
        # below
        pieceOrder = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        self.pieces[40] = Queen(self, 40, WHITE)
        self.pieces[51] = Bishop(self, 51, PIECEBLACK)
        self.pieces[33] = Knight(self, 33, PIECEBLACK)
        self.pieces[9] = Rook(self, 9, PIECEBLACK)
        self.pieces[20] = Rook(self,20,PIECEBLACK)
        # This will represent the index of the currently highlited square
        self.hiSq = False
        # This wil represent the index of the square where currently dragged piece
        # was grabbed from
        self.dragging = False

        # self.eight = OnscreenText(text="8", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                           pos=(-0.9, 0.35), scale=.07)
        # self.seven = OnscreenText(text="7", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                           pos=(-0.93, 0.27), scale=.07)
        # self.six = OnscreenText(text="6", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                         pos=(-0.97, 0.18), scale=.07)
        # self.five = OnscreenText(text="5", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                          pos=(-1.02, 0.1), scale=.07)
        # self.four = OnscreenText(text="4", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                          pos=(-1.06, 0.02), scale=.07)
        # self.three = OnscreenText(text="3", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                           pos=(-1.12, -0.1), scale=.07)
        # self.two = OnscreenText(text="2", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                         pos=(-1.16, -0.18), scale=.07)
        # self.one = OnscreenText(text="1", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                         pos=(-1.23, -0.32), scale=.07)
        x = -0.91
        y = 0.33
        dx = 0.04
        dy = 0.09
        self.eight = OnscreenText(text="8", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                  pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.seven = OnscreenText(text="7", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                  pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.six = OnscreenText(text="6", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.five = OnscreenText(text="5", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                 pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.four = OnscreenText(text="4", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                 pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.three = OnscreenText(text="3", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                  pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.two = OnscreenText(text="2", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                pos=(x, y), scale=.07)
        x -= dx
        y -= dy
        self.one = OnscreenText(text="1", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                pos=(x, y), scale=.07)

        self.A = OnscreenText(text="A", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(-1.05, -0.5), scale=.07)
        self.B = OnscreenText(text="B", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(-0.75, -0.5), scale=.07)
        self.C = OnscreenText(text="C", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(-0.45, -0.5), scale=.07)
        self.D = OnscreenText(text="D", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(-0.15, -0.5), scale=.07)
        self.E = OnscreenText(text="E", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(0.15, -0.5), scale=.07)
        self.F = OnscreenText(text="F", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(0.45, -0.5), scale=.07)
        self.G = OnscreenText(text="G", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(0.75, -0.5), scale=.07)
        self.H = OnscreenText(text="H", style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                              pos=(1.05, -0.5), scale=.07)
        self.A.reparentTo(self.frame)
        self.B.reparentTo(self.frame)
        self.C.reparentTo(self.frame)
        self.D.reparentTo(self.frame)
        self.E.reparentTo(self.frame)
        self.F.reparentTo(self.frame)
        self.G.reparentTo(self.frame)
        self.H.reparentTo(self.frame)
        self.one.reparentTo(self.frame)
        self.two.reparentTo(self.frame)
        self.three.reparentTo(self.frame)
        self.four.reparentTo(self.frame)
        self.five.reparentTo(self.frame)
        self.six.reparentTo(self.frame)
        self.seven.reparentTo(self.frame)
        self.eight.reparentTo(self.frame)
        self.hide()
        # Start the task that handles the picking
        self.mouseTask = taskMgr.add(self.mouseTask, 'mouseTask')
        base.accept("mouse1", self.grabPiece)  # left-click grabs a piece
        base.accept("mouse1-up", self.releasePiece)  # releasing places it
        base.accept("escape",self.hide)

    def hide(self):
        self.frame.hide()
        self.dr2.setActive(False)
        self.A.hide()
        self.B.hide()
        self.C.hide()
        self.D.hide()
        self.E.hide()
        self.F.hide()
        self.G.hide()
        self.H.hide()
        self.one.hide()
        self.two.hide()
        self.three.hide()
        self.four.hide()
        self.five.hide()
        self.six.hide()
        self.seven.hide()
        self.eight.hide()
        base.accept("escape", self.menu.game.pauseGame)
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])
        self.mission.resume()
        self.player.initTask()

    def show(self):
        self.frame.show()
        self.dr2.setActive(True)
        self.A.show()
        self.B.show()
        self.C.show()
        self.D.show()
        self.E.show()
        self.F.show()
        self.G.show()
        self.H.show()
        self.one.show()
        self.two.show()
        self.three.show()
        self.four.show()
        self.five.show()
        self.six.show()
        self.seven.show()
        self.eight.show()
        base.accept("escape", self.hide)

    # This function swaps the positions of two pieces
    def swapPieces(self, fr, to):
        temp = self.pieces[fr]
        self.pieces[fr] = self.pieces[to]
        self.pieces[to] = temp
        if self.pieces[fr]:
            self.pieces[fr].square = fr
            self.pieces[fr].obj.setPos(SquarePos(fr))
        if self.pieces[to]:
            self.pieces[to].square = to
            self.pieces[to].obj.setPos(SquarePos(to))

    def mouseTask(self, task):
        # This task deals with the highlighting and dragging based on the mouse

        # First, clear the current highlight
        if self.hiSq is not False:
            self.squares[self.hiSq].setColor(SquareColor(self.hiSq))
            self.hiSq = False

        # Check to see if we can access the mouse. We need it to do anything
        # else
        if base.mouseWatcherNode.hasMouse():
            # get the mouse position
            mpos = base.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())

            # If we are dragging something, set the position of the object
            # to be at the appropriate point over the plane of the board
            if self.dragging is not False:
                # Gets the point described by pickerRay.getOrigin(), which is relative to
                # camera, relative instead to render
                # nearPoint = render.getRelativePoint(
                #     camera, self.pickerRay.getOrigin())
                nearPoint = render.getRelativePoint(
                    self.cam2, self.pickerRay.getOrigin())
                # Same thing with the direction of the ray
                # nearVec = render.getRelativeVector(
                #     camera, self.pickerRay.getDirection())
                nearVec = render.getRelativeVector(
                    self.cam2, self.pickerRay.getDirection())
                self.pieces[self.dragging].obj.setPos(
                    PointAtZ(.5, nearPoint, nearVec))

            # Do the actual collision pass (Do it only on the squares for
            # efficiency purposes)
            self.picker.traverse(self.squareRoot)
            if self.pq.getNumEntries() > 0:
                # if we have hit something, sort the hits so that the closest
                # is first, and highlight that node
                self.pq.sortEntries()
                i = int(self.pq.getEntry(0).getIntoNode().getTag('square'))
                # Set the highlight on the picked square
                self.squares[i].setColor(HIGHLIGHT)
                self.hiSq = i

        return Task.cont

    def grabPiece(self):
        # If a square is highlighted and it has a piece, set it to dragging
        # mode
        if self.hiSq is not False and self.pieces[self.hiSq]:
            self.dragging = self.hiSq
            self.hiSq = False

    def releasePiece(self):
        # Letting go of a piece. If we are not on a square, return it to its original
        # position. Otherwise, swap it with the piece in the new square
        # Make sure we really are dragging something

        if self.dragging is not False:
            # We have let go of the piece, but we are not on a square
            if self.hiSq is False:
                self.pieces[self.dragging].obj.setPos(
                    SquarePos(self.dragging))
            else:
                if self.state == 0:
                    if self.dragging == 51 and self.hiSq == 58:
                        self.swapPieces(self.dragging, self.hiSq)
                        self.swapPieces(40, 32)
                        self.state = self.state + 1
                        self.mission.manager.GoodsIta['studydoor_box'].state = 'unlockedOpen'
                        self.mission.manager.GoodsIta['studydoor_box'].OpenDoor()
                        self.menu.infoDialog.show()
                        self.menu.infoLabel['text'] = '似乎传来咔嚓一声开锁的声音'
                        self.mission.skip()
                        self.hide()
                    else:
                        self.pieces[self.dragging].obj.setPos(
                            SquarePos(self.dragging))
                        if self.dragging != self.hiSq:
                            self.player.EROSION+=10
                        self.player.erosionUpdateTemp()

                elif self.state == 1:
                    if self.dragging == 33 and self.hiSq == 18:
                        self.swapPieces(self.dragging, self.hiSq)
                        self.state = self.state + 1
                        self.mission.manager.GoodsIta['chessdoor_box'].state = 'unlockedOpen'
                        self.mission.manager.GoodsIta['chessdoor_box'].OpenDoor()
                        self.mission.menu.infoDialog.show()
                        self.mission.menu.infoLabel['text'] = '棋盘上弹出一张纸条「pass。这又不是\n' \
                                                              '真的国际象棋，我选择PASS你又能怎样？\n' \
                                                              '你是无法将死我的。」'
                        self.mission.skip()
                        self.hide()
                    else:
                        self.pieces[self.dragging].obj.setPos(
                            SquarePos(self.dragging))
                        if self.dragging != self.hiSq:
                            self.player.EROSION +=10
                        self.player.erosionUpdateTemp()
                elif self.state ==2:
                    if self.dragging == 20 and self.hiSq == 36:
                        self.swapPieces(self.dragging,self.hiSq)
                        self.state = self.state+1
                        self.mission.manager.GoodsIta['exit_box'].state = 'unlockedOpen'
                        self.mission.menu.infoDialog.show()
                        self.mission.menu.infoLabel['text'] = '可恶 失策了……这里居然…还有一个城堡么…'
                        self.mission.skip()
                        if self.mission.hiddenState:
                            self.mission.end('hiddenEnd')
                        self.hide()
                    else:
                        self.pieces[self.dragging].obj.setPos(
                            SquarePos(self.dragging))
                        if self.dragging != self.hiSq:
                            self.player.EROSION += 10
                        self.player.erosionUpdateTemp()
                elif self.state ==3:
                    self.pieces[self.dragging].obj.setPos(
                        SquarePos(self.dragging))
        # We are no longer dragging anything
        self.dragging = False

    def setupLights(self):  # This function sets up some default lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.8, .8, .8, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 45, -45))
        directionalLight.setColor((0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))

    def initPos(self,state):
        if state ==0:
            self.pieces[40] = Queen(self, 40, WHITE)
            self.pieces[51] = Bishop(self, 51, PIECEBLACK)
            self.pieces[33] = Knight(self, 33, PIECEBLACK)
            self.pieces[9] = Rook(self, 9, PIECEBLACK)
            self.pieces[20] = Rook(self, 20, PIECEBLACK)
        elif state == 1:
            self.pieces[32] = Queen(self, 32, WHITE)
            self.pieces[58] = Bishop(self, 58, PIECEBLACK)
            self.pieces[33] = Knight(self, 33, PIECEBLACK)
            self.pieces[9] = Rook(self, 9, PIECEBLACK)
            self.pieces[20] = Rook(self, 20, PIECEBLACK)
        elif state == 2:
            self.pieces[32] = Queen(self, 32, WHITE)
            self.pieces[58] = Bishop(self, 58, PIECEBLACK)
            self.pieces[18] = Knight(self, 18, PIECEBLACK)
            self.pieces[9] = Rook(self, 9, PIECEBLACK)
            self.pieces[20] = Rook(self, 20, PIECEBLACK)
        elif state == 3:
            self.pieces[32] = Queen(self, 32, WHITE)
            self.pieces[58] = Bishop(self, 58, PIECEBLACK)
            self.pieces[18] = Knight(self, 18, PIECEBLACK)
            self.pieces[9] = Rook(self, 9, PIECEBLACK)
            self.pieces[36] = Rook(self, 36, PIECEBLACK)


# Class for a piece. This just handles loading the model and setting initial
# position and color
class Piece(object):
    def __init__(self, demo, square, color):
        self.obj = loader.loadModel(self.model)
        self.obj.reparentTo(demo.render2)
        self.obj.setColor(color)
        self.obj.setPos(SquarePos(square))


# Classes for each type of chess piece
# Obviously, we could have done this by just passing a string to Piece's init.
# But if you wanted to make rules for how the pieces move, a good place to start
# would be to make an isValidMove(toSquare) method for each piece type
# and then check if the destination square is acceptible during ReleasePiece
# class Pawn(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/pawn"
#
# class King(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/Scene3_king"
#
# class Queen(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/queen"
#
# class Bishop(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/Scene3_bishop"
#
# class Knight(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/Scene3_knight"
#
# class Rook(Piece):
#     model = "../res/models/Scene3/Scene3Cat/hall/rook"

class Pawn(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/pawn"

class King(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/Scene3_king"

class Queen(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/queen"

class Bishop(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/bishop.egg.pz"

class Knight(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/knight.egg.pz"

class Rook(Piece):
    model = "res/models/Scene3/Scene3Cat/hall/rook.egg.pz"

# Do the main initialization and start 3D rendering
# demo = ChessboardDemo()
# run()
