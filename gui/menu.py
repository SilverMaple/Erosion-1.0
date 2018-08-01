# -*- coding: utf-8 -*-
import random
import sys, os, gc

from direct.stdpy import threading
from direct.stdpy import thread
from pandac.PandaModules import Thread
from direct.gui.DirectDialog import DirectDialog
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectLabel import DirectLabel
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.OnscreenImage import OnscreenImage, LVecBase4f
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.showbase.ShowBase import ShowBase, WindowProperties
from panda3d.core import TransparencyAttrib

from game.game import Game
from game.save import Save
from game.leveltwo import LevelTwo
from game.levelthree import LevelThree
from role.player import Player
from audio.audioManager import AudioManager

from panda3d.core import loadPrcFileData, MovieTexture, CardMaker, NodePath, AudioSound
# Tell Panda3D to use OpenAL, not FMOD
loadPrcFileData("", "audio-library-name p3openal_audio")

SPEED = 0.5


class Menu(DirectObject):

    def ranColor(self, task):
        self.it += 1
        if self.it % 5 == 0:
            self.r = random.uniform(0, 1)
            self.g = random.uniform(0, 1)
            self.b = random.uniform(0, 1)
            self.background.setColorScale(LVecBase4f(self.r, self.g, self.b, .5))
            self.background.reparentTo(self.mainFrame)
        return task.cont

    def initSound(self):
        self.soundMgr = AudioManager()
        self.soundMgr.playMusic('bgm1.mp3')
        self.soundMgr.mySound.stop()
        self.musicVolume = 50
        self.soundMgr.setMusicVolume(self.musicVolume / 100.0)
        # self.soundMgr.mySound.setVolume(self.musicVolume / 100)

    def initVideo(self):
        media_file = "res/videos/fgh_2k_Mux2.avi"
        self.tex = MovieTexture("name")
        success = self.tex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("My Fullscreen Card")
        # cm.setFrameFullscreenQuad()
        cm.setFrame(-1.3, 1.3, -1, 1)

        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.tex)
        self.card = NodePath(cm.generate())
        self.card.reparentTo(base.render2d)
        self.card.setTexture(self.tex)
        self.videoSound = loader.loadSfx(media_file)
        self.tex.synchronizeTo(self.videoSound)
        self.videoSound.play()

        taskMgr.add(self.playVideo, 'playVideo')
        self.creditVideo()

    def playVideo(self, task):
        if self.videoSound.status() != AudioSound.PLAYING:
            self.videoSound.stop()
            self.card.hide()
            self.mainFrame.show()
            self.soundMgr.playMusic('bgm1.mp3')
            return 0
        return task.cont

    def loadVideo(self):
        media_file = "res/videos/loading.avi"
        self.loadTex = MovieTexture("loadingTexture")
        success = self.loadTex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("loading card")
        cm.setFrame(-1, 1, -1, 1)
        cm.setUvRange(self.loadTex)
        self.loadCard = NodePath(cm.generate())
        self.loadCard.reparentTo(base.render2d)
        self.loadCard.setTexture(self.loadTex)
        # self.card.show()
        self.loadSound = loader.loadSfx("res/sounds/bgm.mp3")
        self.loadSound.setVolume(0)
        self.loadSound.setLoop(True)
        self.loadTex.synchronizeTo(self.loadSound)

        # self.loadFrame.hide()
        self.loadSound.play()
        self.loadState = False
        taskMgr.add(self.gameReady, 'gameReady')
        print 'load video'

    def gameReady(self, task):
        if self.loadState:
            self.loadSound.stop()
            self.loadCard.hide()
            self.game.node.setUpCamera()
            return 0
        return task.cont

    def creditVideo(self):
        media_file = "res/videos/credits.avi"
        self.creditTex = MovieTexture("loadingTexture")
        success = self.creditTex.read(media_file)
        assert success, "Failed to load video!"

        cm = CardMaker("credit card")
        cm.setFrame(-1, 1, -1, 1)
        cm.setUvRange(self.creditTex)
        self.creditCard = NodePath(cm.generate())
        self.creditCard.reparentTo(base.render2d)
        self.creditCard.setTexture(self.creditTex)
        # self.card.show()
        self.creditSound = loader.loadSfx("res/videos/credits.avi")
        self.creditSound.setVolume(0)
        self.creditSound.setLoop(True)
        self.creditTex.synchronizeTo(self.creditSound)

        print 'credit video'

    def __init__(self):
        DirectObject.__init__(self)

        wp = WindowProperties()
        wp.setTitle('EROSION')
        wp.setSize(1024, 768)
        wp.set_origin(200, 30)
        # wp.setFullscreen(True)
        base.win.requestProperties(wp)

        self.initVideo()
        self.initSound()
        self.game = 0
        self.tempPlayer = None
        # threading.currentThread().setName('mainThread')

        '''
        mainFrame initialize
        '''
        self.xCoor = -0.8
        self.yCoor = 0.0
        self.zCoor = -0.4
        self.hCoor = 0.2
        self.mainFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        # print os.getcwd()
        self.background = OnscreenImage('res/back.png', pos=(0, 0, 0), scale=(1.5, 1, 1))
        self.r = 1
        self.g = 0
        self.b = 0
        self.it = 0
        # taskMgr.add(self.ranColor, 'ranColor')
        self.background.reparentTo(self.mainFrame)
        self.clickSound = loader.loadSfx('res/sounds/click.mp3')
        self.hoverSound = loader.loadSfx('res/sounds/click.mp3')
        self.clickSound.setVolume(1)
        # print self.clickSound

        self.buttonMaps = loader.loadModel('res/button_maps')
        self.newGameButtonMaps = loader.loadModel('res/button_new_game')
        self.continueButtonMaps = loader.loadModel('res/button_continue')
        self.optionsButtonMaps = loader.loadModel('res/button_options')
        self.creditsButtonMaps = loader.loadModel('res/button_credits')
        self.exitButtonMaps = loader.loadModel('res/button_exit')
        self.yesButtonMaps = loader.loadModel('res/button_yes')
        self.noButtonMaps = loader.loadModel('res/button_no')
        self.returnButtonMaps = loader.loadModel('res/button_return')
        self.loadLevelMaps = loader.loadModel('res/button_load_level')
        self.loadButtonMaps = loader.loadModel('res/button_load')
        self.sliderMaps = loader.loadModel('res/slider')
        self.saveSlotMaps = loader.loadModel('res/save_slot')
        self.deleteSlotMaps = loader.loadModel('res/delete_slot')
        self.pauseResumeMaps = loader.loadModel('res/pause_resume')
        self.pauseLoadMaps = loader.loadModel('res/pause_load')
        self.pauseSaveMaps = loader.loadModel('res/pause_save')
        self.pauseExitMaps = loader.loadModel('res/pause_exit')
        self.selectButtonMaps = loader.loadModel('res/btn_option')
        self.selectMaps = loader.loadModel('res/select')

        self.startButton = DirectButton(relief=None, scale=(0.4, 1, 0.07), clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.newGameButtonMaps.find("**/button_new_game_ready"),
                                              self.newGameButtonMaps.find("**/button_new_game_click"),
                                              self.newGameButtonMaps.find("**/button_new_game_rollover"),
                                              self.newGameButtonMaps.find("**/button_new_game_disabled")), command=self.startGame,
                                        pos=(self.xCoor, self.yCoor, self.zCoor+2*self.hCoor))
        self.continueButton = DirectButton(relief=None, scale=(0.4, 1, 0.07), clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.continueButtonMaps.find("**/button_continue_ready"),
                                              self.continueButtonMaps.find("**/button_continue_click"),
                                              self.continueButtonMaps.find("**/button_continue_rollover"),
                                              self.continueButtonMaps.find("**/button_continue_disabled")), command=self.continueGame,
                                        pos=(self.xCoor, self.yCoor, self.zCoor+1*self.hCoor))
        self.settingButton = DirectButton(relief=None, scale=(0.4, 1, 0.07), clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.optionsButtonMaps.find("**/button_options_ready"),
                                              self.optionsButtonMaps.find("**/button_options_click"),
                                              self.optionsButtonMaps.find("**/button_options_rollover"),
                                              self.optionsButtonMaps.find("**/button_options_disabled")), command=self.settingGame,
                                        pos=(self.xCoor, self.yCoor, self.zCoor))
        self.aboutButton = DirectButton(relief=None, scale=(0.4, 1, 0.07), clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.creditsButtonMaps.find("**/button_credits_ready"),
                                              self.creditsButtonMaps.find("**/button_credits_click"),
                                              self.creditsButtonMaps.find("**/button_credits_rollover"),
                                              self.creditsButtonMaps.find("**/button_credits_disabled")), command=self.aboutGame,
                                        pos=(self.xCoor, self.yCoor, self.zCoor-1*self.hCoor))
        self.exitButton = DirectButton(relief=None, scale=(0.4, 1, 0.07), clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.exitButtonMaps.find("**/button_exit_ready"),
                                              self.exitButtonMaps.find("**/button_exit_click"),
                                              self.exitButtonMaps.find("**/button_exit_rollover"),
                                              self.exitButtonMaps.find("**/button_exit_disabled")), command=self.exitGame,
                                       pos=(self.xCoor, self.yCoor, self.zCoor-2*self.hCoor))
        self.startButton.reparentTo(self.mainFrame)
        self.continueButton.reparentTo(self.mainFrame)
        self.settingButton.reparentTo(self.mainFrame)
        self.aboutButton.reparentTo(self.mainFrame)
        self.exitButton.reparentTo(self.mainFrame)
        self.mainFrame.hide()

        '''
        levelFrame initialize
        '''
        self.xSave = -0.8
        self.ySave = 0.0
        self.zSave = 0
        self.levelFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage('res/background.png', pos=(0, 0, 0), scale=(1.5, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.levelFrame)
        self.selectedLevel = 1
        self.level1Button = DirectButton(text="教学关", text_scale=(.08, .27), text_pos=(0, -.1, 0), scale=(1, 1, 0.3), relief=None,
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound, text_fg=(1, 1, 1, 1),
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectLevel,
                                        extraArgs=[1],
                                        pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave + 2 * self.hCoor))
        self.level2Button = DirectButton(text="第二关", text_scale=(.08, .27), text_pos=(0, -.1, 0), scale=(1, 1, 0.3), relief=None,
                                        text_fg=(1, 1, 1, 1),
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectLevel,
                                        extraArgs=[2],
                                        pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave + 0 * self.hCoor))
        self.level3Button = DirectButton(text="第三关", text_scale=(.08, .27), text_pos=(0, -.1, 0), scale=(1, 1, 0.3), relief=None,
                                        text_fg=(1, 1, 1, 1),
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectLevel,
                                        extraArgs=[3],
                                        pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave - 2 * self.hCoor))
        self.loadLevelButton = DirectButton(text="", text_scale=(0.07, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                           clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                           geom=(self.loadLevelMaps.find("**/button_load_level_ready"),
                                                 self.loadLevelMaps.find("**/button_load_level_click"),
                                                 self.loadLevelMaps.find("**/button_load_level_rollover"),
                                                 self.loadLevelMaps.find("**/button_load_level_disabled")),
                                           command=self.loadLevel,
                                           pos=(self.xSave + 8 * self.hCoor, self.yCoor, self.zCoor + 2 * self.hCoor))
        self.returnButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                         geom=(self.returnButtonMaps.find("**/button_return_ready"),
                                               self.returnButtonMaps.find("**/button_return_click"),
                                               self.returnButtonMaps.find("**/button_return_rollover"),
                                               self.returnButtonMaps.find("**/button_return_disabled")),
                                         command=self.levelToMain,
                                         pos=(self.xSave - 0.8 * self.hCoor, self.yCoor, self.zCoor - 2 * self.hCoor))
        self.level1Button.reparentTo(self.levelFrame)
        self.level2Button.reparentTo(self.levelFrame)
        self.level3Button.reparentTo(self.levelFrame)
        self.loadLevelButton.reparentTo(self.levelFrame)
        self.returnButton.reparentTo(self.levelFrame)
        self.levelFrame.hide()

        '''
        saveFrame initialize
        '''
        self.skipUseless = False
        self.xSave = -0.8
        self.ySave = 0.0
        self.zSave = 0
        self.saveFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage('res/background.png', pos=(0, 0, 0), scale=(1.5, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.saveFrame)
        self.selectedSave = 1
        self.slot1Button = DirectButton(text="20170703 12:00", text_scale=(.08, .27), text_pos=(.15, -.1, 0), scale=(1, 1, 0.3), relief=None,
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound, text_fg=(1, 1, 1, 1),
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectSlot,
                                        extraArgs=[1], pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave + 2 * self.hCoor))
        self.slot2Button = DirectButton(text="20170702 19:00", text_scale=(.08, .27), text_pos=(.15, -.1, 0), scale=(1, 1, 0.3), relief=None, text_fg=(1, 1, 1, 1),
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectSlot,
                                        extraArgs=[2], pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave + 0 * self.hCoor))
        self.slot3Button = DirectButton(text="20170701 11:00", text_scale=(.08, .27), text_pos=(.15, -.1, 0), scale=(1, 1, 0.3), relief=None, text_fg=(1, 1, 1, 1),
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.saveSlotMaps.find("**/save_slot_ready"),
                                              self.saveSlotMaps.find("**/save_slot_click"),
                                              self.saveSlotMaps.find("**/save_slot_rollover"),
                                              self.saveSlotMaps.find("**/save_slot_disabled")), command=self.selectSlot,
                                        extraArgs=[3], pos=(self.xSave + 1 * self.hCoor, self.ySave, self.zSave - 2 * self.hCoor))
        self.loadSaveButton = DirectButton(text="", text_scale=(0.07, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                        clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                       geom=(self.loadButtonMaps.find("**/button_load_ready"),
                                             self.loadButtonMaps.find("**/button_load_click"),
                                             self.loadButtonMaps.find("**/button_load_rollover"),
                                             self.loadButtonMaps.find("**/button_load_disabled")),
                                       command=self.loadExistSave,
                                       pos=(self.xSave + 8 * self.hCoor, self.yCoor, self.zCoor + 2 * self.hCoor))
        self.deleteSaveButton = DirectButton(text="", text_scale=(0.07, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                             clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                         geom=(self.deleteSlotMaps.find("**/delete_slot_ready"),
                                               self.deleteSlotMaps.find("**/delete_slot_click"),
                                               self.deleteSlotMaps.find("**/delete_slot_rollover"),
                                               self.deleteSlotMaps.find("**/delete_slot_disabled")),
                                         command=self.deleteSave,
                                         pos=(self.xSave + 8 * self.hCoor, self.yCoor, self.zCoor - 0 * self.hCoor))
        self.returnButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.returnButtonMaps.find("**/button_return_ready"),
                                              self.returnButtonMaps.find("**/button_return_click"),
                                              self.returnButtonMaps.find("**/button_return_rollover"),
                                              self.returnButtonMaps.find("**/button_return_disabled")), command=self.saveToMain,
                                        pos=(self.xSave - 0.8 * self.hCoor, self.yCoor, self.zCoor - 2 * self.hCoor))
        self.slot1Button.reparentTo(self.saveFrame)
        self.slot2Button.reparentTo(self.saveFrame)
        self.slot3Button.reparentTo(self.saveFrame)
        self.loadSaveButton.reparentTo(self.saveFrame)
        self.deleteSaveButton.reparentTo(self.saveFrame)
        self.returnButton.reparentTo(self.saveFrame)
        self.saveFrame.hide()

        '''
        pauseFrame initialize
        '''
        self.pauseFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage('res/background-pause.png', pos=(0, 0, 0), scale=(1.4, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.continueButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.6, 1, 0.1),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.pauseResumeMaps.find("**/pause_resume_ready"),
                                              self.pauseResumeMaps.find("**/pause_resume_click"),
                                              self.pauseResumeMaps.find("**/pause_resume_rollover"),
                                              self.pauseResumeMaps.find("**/pause_resume_disabled")), command=self.backToGame,
                                         pos=(self.xCoor, self.yCoor, self.zCoor + 3.5 * self.hCoor))
        self.pauseSaveButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.6, 1, 0.1),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                         geom=(self.pauseSaveMaps.find("**/pause_save_ready"),
                                               self.pauseSaveMaps.find("**/pause_save_click"),
                                               self.pauseSaveMaps.find("**/pause_save_rollover"),
                                               self.pauseSaveMaps.find("**/pause_save_disabled")),
                                         command=self.saveCurrentGame,
                                         pos=(self.xCoor, self.yCoor, self.zCoor + 2.5 * self.hCoor))
        self.pauseLoadButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.6, 1, 0.1),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                         geom=(self.pauseLoadMaps.find("**/pause_load_ready"),
                                               self.pauseLoadMaps.find("**/pause_load_click"),
                                               self.pauseLoadMaps.find("**/pause_load_rollover"),
                                               self.pauseLoadMaps.find("**/pause_load_disabled")),
                                         command=self.loadLastGame,
                                         pos=(self.xCoor, self.yCoor, self.zCoor + 1.5 * self.hCoor))
        self.returnButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.6, 1, 0.1),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.pauseExitMaps.find("**/pause_exit_ready"),
                                              self.pauseExitMaps.find("**/pause_exit_click"),
                                              self.pauseExitMaps.find("**/pause_exit_rollover"),
                                              self.pauseExitMaps.find("**/pause_exit_disabled")), command=self.backToMenu,
                                         pos=(self.xCoor, self.yCoor, self.zCoor + 0.5 * self.hCoor))
        self.background.reparentTo(self.pauseFrame)
        self.continueButton.reparentTo(self.pauseFrame)
        self.pauseSaveButton.reparentTo(self.pauseFrame)
        self.pauseLoadButton.reparentTo(self.pauseFrame)
        self.returnButton.reparentTo(self.pauseFrame)
        self.pauseFrame.hide()

        '''
        settingFrame initialize
        '''
        self.xLabel = -0.9
        self.zLabel = 0.4
        self.musicVolume = 50
        self.voiceVolume = 50
        self.settingFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.background = OnscreenImage('res/optionBackground.png', pos=(0, 0, 0), scale=(1.4, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        # self.musicLabel = OnscreenText(text='Music Volume', style=1, fg=(0, 0, 0, 1),
        #                                 pos=(self.xLabel, self.zLabel), align=TextNode.ALeft, scale=.07)
        #
        # self.voiceLabel = OnscreenText(text='Voice Volume', style=1, fg=(0, 0, 0, 1),
        #                             pos=(self.xLabel, self.zLabel - 1 * self.hCoor), align=TextNode.ALeft,
        #                             scale=.07)
        self.musicSlider = DirectSlider(range=(0,100), value=50, pageSize=1, relief=None,
                                        command=self.setMusicVolume, scale=(0.6, 1, 0.1),
                                        geom=(self.sliderMaps.find("**/slider_bar"),
                                              self.sliderMaps.find("**/slider_value")),
                                        image=(self.sliderMaps.find("**/slider_value")),
                                        pos=(self.xSave + 5 * self.hCoor, self.ySave, self.zSave + 1.8 * self.hCoor))
        self.voiceSlider = DirectSlider(range=(0,100), value=50, pageSize=1, relief=None,
                                        command=self.setVoiceVolume, scale=(0.6, 1, 0.1),
                                        geom=(self.sliderMaps.find("**/slider_bar"),
                                              self.sliderMaps.find("**/slider_value")),
                                        image=(self.sliderMaps.find("**/slider_value")),
                                        pos=(self.xSave + 5 * self.hCoor, self.ySave, self.zSave + .35 * self.hCoor))
        self.textSlider = DirectSlider(range=(0, 100), value=50, pageSize=1, relief=None,
                                        command=self.setVoiceVolume, scale=(0.6, 1, 0.1),
                                        geom=(self.sliderMaps.find("**/slider_bar"),
                                              self.sliderMaps.find("**/slider_value")),
                                        image=(self.sliderMaps.find("**/slider_value")),
                                        pos=(self.xSave + 5 * self.hCoor, self.ySave, self.zSave - 1.1 * self.hCoor))
        self.returnButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.returnButtonMaps.find("**/button_return_ready"),
                                              self.returnButtonMaps.find("**/button_return_click"),
                                              self.returnButtonMaps.find("**/button_return_rollover"),
                                              self.returnButtonMaps.find("**/button_return_disabled")), command=self.settingToMain,
                                         pos=(self.xSave - 0.8 * self.hCoor, self.yCoor, self.zCoor - 2 * self.hCoor))
        self.background.reparentTo(self.settingFrame)
        # self.musicLabel.reparentTo(self.settingFrame)
        # self.voiceLabel.reparentTo(self.settingFrame)
        self.musicSlider.reparentTo(self.settingFrame)
        self.voiceSlider.reparentTo(self.settingFrame)
        self.textSlider.reparentTo(self.settingFrame)
        self.returnButton.reparentTo(self.settingFrame)
        self.settingFrame.hide()

        '''
        aboutFrame initialize
        '''
        self.xLabel = -0.8
        self.zLabel = 0.4
        self.aboutFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        # self.background = OnscreenImage('res/silence.jpg', pos=(0, 0, 0), scale=(1.5, 1, 1))
        # self.background.setTransparency(TransparencyAttrib.MAlpha)
        # self.background.reparentTo(self.aboutFrame)
        # self.logoImage = OnscreenImage(image='res/fgh_color.png', pos=(0, 0, 0), scale=(.5, 1, .4))
        # self.logoImage.setTransparency(TransparencyAttrib.MAlpha)
        # self.staff1Label = OnscreenText(text='Game studio: ', style=1, fg=(0,0,0,1),
        #                 pos=(self.xLabel, self.zLabel), align=TextNode.ALeft, scale = .1)
        # self.staff2Label = OnscreenText(text='FGH', style=1, fg=(0,0,0,1),
        #                 pos=(self.xLabel + self.hCoor, self.zLabel - 1 * self.hCoor), align=TextNode.ALeft, scale = .07)
        # self.staff3Label = OnscreenText(text='Members:', style=1, fg=(0,0,0,1),
        #                 pos=(self.xLabel, self.zLabel - 2 * self.hCoor), align=TextNode.ALeft, scale = .07)
        # self.staff4Label = OnscreenText(text='UBeach Nine', style=1, fg=(0,0,0,1),
        #                 pos=(self.xLabel + self.hCoor, self.zLabel - 3 * self.hCoor), align=TextNode.ALeft, scale = .07)
        self.returnButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(0.5, 1, 0.09),
                                         clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                        geom=(self.returnButtonMaps.find("**/button_return_ready"),
                                              self.returnButtonMaps.find("**/button_return_click"),
                                              self.returnButtonMaps.find("**/button_return_rollover"),
                                              self.returnButtonMaps.find("**/button_return_disabled")), command=self.aboutToMain,
                                         pos=(self.xSave - 0.8 * self.hCoor, self.yCoor, self.zCoor - 2 * self.hCoor))
        # self.logoImage.reparentTo(self.aboutFrame)
        # self.staff1Label.reparentTo(self.aboutFrame)
        # self.staff2Label.reparentTo(self.aboutFrame)
        # self.staff3Label.reparentTo(self.aboutFrame)
        # self.staff4Label.reparentTo(self.aboutFrame)
        self.creditCard.reparentTo(self.aboutFrame)
        self.creditCard.setScale(1.5, 1, 1)
        self.returnButton.reparentTo(self.aboutFrame)
        self.aboutFrame.hide()

        '''
        selectDialog initialize
        '''
        self.selectDialog = DirectDialog(dialogName='selectDialog', relief=None,
                                    image='res/window.png', scale=(7, 1, .6), text_fg=(0, 0, 0, 1))
        self.selectDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.textLabel = DirectLabel(text='test', text_scale=(.09, .09, .8), text_fg=(1, 1, 1, 1), text_pos=(0, .1),
                                      relief=None, scale=(.1, 1, 1.2), pos=(0, 0, 0))
        self.aButton = DirectButton(text="Option A", text_scale=(.07, .36), text_pos=(.1, 0, 0), text_fg=(1, 1, 1, 1), relief=None, scale=(.1, 1, .25),
                                      clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                      geom=(self.selectMaps.find("**/select_ready"),
                                            self.selectMaps.find("**/select_click"),
                                            self.selectMaps.find("**/select_rollover"),
                                            self.selectMaps.find("**/select_disabled")),
                                      pos=(.12, 0, 0.8))
        self.bButton = DirectButton(text="Option B", text_scale=(.07, .36), text_pos=(.1, 0, 0), text_fg=(1, 1, 1, 1), relief=None, scale=(.1, 1, .25),
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.selectMaps.find("**/select_ready"),
                                          self.selectMaps.find("**/select_click"),
                                          self.selectMaps.find("**/select_rollover"),
                                          self.selectMaps.find("**/select_disabled")),
                                    pos=(.12, 0, 0.5))
        self.cButton = DirectButton(text="Option C", text_scale=(.07, .36), text_pos=(.1, 0, 0), text_fg=(1, 1, 1, 1),
                                    relief=None, scale=(.1, 1, .25),
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.selectMaps.find("**/select_ready"),
                                          self.selectMaps.find("**/select_click"),
                                          self.selectMaps.find("**/select_rollover"),
                                          self.selectMaps.find("**/select_disabled")),
                                    pos=(.12, 0, 1.1))
        self.cButton.hide()
        # self.selectDialog = DirectDialog(dialogName='selectDialog', relief=None,
        #                                  image='res/dialog.png', scale=(8, 1, .4), text_fg=(1, 1, 1, 1))
        # self.textLabel = DirectLabel(text='test', text_scale=(.07, .1, .8), text_fg=(1, 1, 1, 1), text_pos=(0, .1),
        #                              relief=None, scale=(.1, 1, 1.2), pos=(-.05, 0, 0))
        # self.aButton = DirectButton(text="Option A", text_scale=(.07, .36), text_fg=(1, 1, 1, 1), relief=None,
        #                             scale=(.08, 1, .3),
        #                             clickSound=self.clickSound, rolloverSound=self.hoverSound,
        #                             geom=(self.selectButtonMaps.find("**/btn_option_ready"),
        #                                   self.selectButtonMaps.find("**/btn_option_cllick"),
        #                                   self.selectButtonMaps.find("**/btn_option_rollover"),
        #                                   self.selectButtonMaps.find("**/btn_option_disabled")),
        #                             pos=(.14, 0, .12))
        # self.bButton = DirectButton(text="Option B", text_scale=(.07, .36), text_fg=(1, 1, 1, 1), relief=None,
        #                             scale=(.08, 1, .3),
        #                             clickSound=self.clickSound, rolloverSound=self.hoverSound,
        #                             geom=(self.selectButtonMaps.find("**/btn_option_ready"),
        #                                   self.selectButtonMaps.find("**/btn_option_cllick"),
        #                                   self.selectButtonMaps.find("**/btn_option_rollover"),
        #                                   self.selectButtonMaps.find("**/btn_option_disabled")),
        #                             pos=(.14, 0, -0.2))
        self.aButton.reparentTo(self.selectDialog)
        self.bButton.reparentTo(self.selectDialog)
        self.cButton.reparentTo(self.selectDialog)
        self.textLabel.reparentTo(self.selectDialog)
        self.selectDialog.setPos(0, 0, -.7)
        self.selectDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.selectDialog.hide()

        '''
        tutorialDialog
        '''
        self.tutorialDialog = DirectDialog(dialogName='tutorialDialog', relief=None,
                                         image='res/dialog.png', scale=(8, 1, .4), text_fg=(1, 1, 1, 1))
        self.nextButton = DirectButton(text="Option A", text_scale=(.016, .2), text_fg=(1, 1, 1, 1), relief=None,
                                    scale=(.4, 1, .75), text_pos=(0, .1),
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.selectButtonMaps.find("**/btn_option_ready"),
                                         self.selectButtonMaps.find("**/btn_option_cllick"),
                                         self.selectButtonMaps.find("**/btn_option_rollover"),
                                         self.selectButtonMaps.find("**/btn_option_disabled")),
                                    pos=(0, 0, -.03))
        self.headLabel = DirectLabel(image="res/headPhoto/kura.png", relief=None, scale=(.1, 1, 2.5), pos=(-.13, 0, 1))
        self.headLabel.setTransparency(TransparencyAttrib.MAlpha)
        self.headLabel.reparentTo(self.tutorialDialog)
        self.nextButton.reparentTo(self.tutorialDialog)
        self.tutorialDialog.setPos(0, 0, -.7)
        self.tutorialDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.tutorialDialog.hide()

        '''
        ocanioDialog
        '''
        self.ocanioDialog = DirectDialog(dialogName='ocanioDialog', relief=None,
                                         image='res/dialog.png', scale=(8, 1, .4), text_fg=(1, 1, 1, 1))
        self.headLabel = DirectLabel(relief=None, scale=(.12, 1, 2.5), pos=(-.13, 0, 1))
        self.ocanioButton = DirectButton(text="Option A", text_scale=(.015, .2), text_fg=(1, 1, 1, 1), relief=None,
                                    scale=(.4, 1, .75),
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.selectButtonMaps.find("**/btn_option_ready"),
                                          self.selectButtonMaps.find("**/btn_option_cllick"),
                                          self.selectButtonMaps.find("**/btn_option_rollover"),
                                          self.selectButtonMaps.find("**/btn_option_disabled")),
                                    pos=(0, 0, -.03))
        self.ocanioButton.reparentTo(self.ocanioDialog)
        self.headLabel.reparentTo(self.ocanioDialog)
        self.ocanioDialog.setPos(0, 0, -.7)
        self.ocanioDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.ocanioDialog.hide()

        '''
        infoDialog initialize
        '''
        self.infoDialog = DirectDialog(dialogName='infoDialog', text='', text_scale=(.12),
                                         relief=None, image='res/information.png', scale=(4, 1, .6), text_fg=(1, 1, 1, 1))
        self.infoLabel = DirectLabel(text='test', text_scale=(.18, .1, .8), text_fg=(1, 1, 1, 1), text_pos=(0, 0),
                                     relief=None, scale=(.1, 1, 1.2), pos=(0, 0, 0))
        self.infoDialog.setPos(0, 0, 0)
        self.infoLabel.reparentTo(self.infoDialog)
        self.infoDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.infoDialog.hide()

        '''
        tipDialog initialize
        '''
        self.tipDialog = DirectDialog(dialogName='tipDialog', text='', text_scale=(.12),
                                       relief=None, image='res/information.png', scale=(4, 1, .6), text_fg=(1, 1, 1, 1))
        self.tipLabel = DirectLabel(text='test', text_scale=(.18, .1, .8), text_fg=(1, 1, 1, 1), text_pos=(0, 0),
                                     relief=None, scale=(.1, 1, 1.2), pos=(0, 0, 0))
        self.tipDialog.setPos(0, 0, 0)
        self.tipLabel.reparentTo(self.tipDialog)
        self.tipDialog.setTransparency(TransparencyAttrib.MAlpha)
        self.tipDialog.hide()

        '''
        deleteDialog initialize
        '''
        self.deleteDialog = DirectDialog(dialogName='deleteDialog', text='',
                                         relief=None, image='res/exit.png', scale=(2.5, 1, .7))

        self.yesButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(.2), command=self.doDelete,
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.yesButtonMaps.find("**/button_yes_ready"),
                                          self.yesButtonMaps.find("**/button_yes_click"),
                                          self.yesButtonMaps.find("**/button_yes_rollover"),
                                          self.yesButtonMaps.find("**/button_yes_disabled")),
                                    pos=(-0.1, 0, -0.2))
        self.noButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(.2), command=self.cancelDelete,
                                    clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                    geom=(self.noButtonMaps.find("**/button_no_ready"),
                                          self.noButtonMaps.find("**/button_no_click"),
                                          self.noButtonMaps.find("**/button_no_rollover"),
                                          self.noButtonMaps.find("**/button_no_disabled")),
                                    pos=(0.1, 0, -0.2))
        self.yesButton.reparentTo(self.deleteDialog)
        self.noButton.reparentTo(self.deleteDialog)
        self.deleteDialog.hide()

        '''
        exitDialog initialize
        '''
        self.dialog = DirectDialog(dialogName='', text='', command=self.isExit,
                                  relief=None, image='res/exit.png', scale=(2.5, 1, .7))
        self.yesButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(.2),
                                      clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                     geom=(self.yesButtonMaps.find("**/button_yes_ready"),
                                           self.yesButtonMaps.find("**/button_yes_click"),
                                           self.yesButtonMaps.find("**/button_yes_rollover"),
                                           self.yesButtonMaps.find("**/button_yes_disabled")), command=sys.exit,
                                      pos=(-0.1, 0, -0.2))
        self.noButton = DirectButton(text="", text_scale=(0.14, 0.07), relief=None, scale=(.2),
                                     clickSound=self.clickSound, rolloverSound=self.hoverSound,
                                      geom=(self.noButtonMaps.find("**/button_no_ready"),
                                            self.noButtonMaps.find("**/button_no_click"),
                                            self.noButtonMaps.find("**/button_no_rollover"),
                                            self.noButtonMaps.find("**/button_no_disabled")), command=self.cancelExit,
                                     pos=(0.1, 0, -0.2))
        self.yesButton.reparentTo(self.dialog)
        self.noButton.reparentTo(self.dialog)
        self.dialog.hide()
        # self.mainFrame.show()
        self.passFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.passFrame.hide()

        self.endPictureFrame = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 2, -2, 2), pos=(0, 0, 0))
        self.endBackground = OnscreenImage('res/end/trueend.png', pos=(0, 0, 0), scale=(1.4, 1, 1))
        self.endBackground.reparentTo(self.endPictureFrame)
        self.endPictureFrame.hide()

    #     messenger.send('shift')
    #     self.flag = True
    #     base.accept('shift', self.undoShift)
    #
    # def undoShift(self):
    #     if self.flag:
    #         self.flag = False
    #         messenger.send('shift')
    #     else:
    #         self.flag = True

    '''
    event in levelFrame
    '''
    def selectLevel(self, arg):
        self.selectedLevel = arg
        self.level1Button['image'] = None
        self.level2Button['image'] = None
        self.level3Button['image'] = None

        if arg == 1:
            self.level1Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')
        elif arg == 2:
            self.level2Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')
        else:
            self.level3Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')

    def loadLevel(self):
        print 'load level'
        self.mainFrame.hide()
        self.levelFrame.hide()
        self.loadVideo()
        thread.start_new_thread(self.loadLevelGame, {})

    def loadLevelGame(self):
        self.skipUseless = False
        if self.selectedLevel == 1:
            self.game = Game(self)
            print "load teaching level"
        elif self.selectedLevel == 2:
            self.game = LevelTwo(self)
            print "load level two"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        else:
            self.game = LevelThree(self)
            print "load level three"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        # self.soundMgr.setMusicVolume(0)
        # self.musicVolume = 0
        self.mainFrame.hide()
        self.save = Save(self.game)

    def levelToMain(self):
        self.levelFrame.hide()
        self.mainFrame.show()

    '''
    event in saveFrame
    '''
    def selectSlot(self, arg):
        self.selectedSave = arg
        self.slot1Button['image'] = None
        self.slot2Button['image'] = None
        self.slot3Button['image'] = None

        if arg == 1:
            self.slot1Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')
        elif arg == 2:
            self.slot2Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')
        else:
            self.slot3Button['image'] = self.saveSlotMaps.find('**/save_slot_selected')

    def loadExistSave(self):
        print 'load exist save'
        self.mainFrame.hide()
        self.saveFrame.hide()
        self.loadVideo()
        thread.start_new_thread(self.loadExistGame, {})

    def loadExistGame(self):
        self.skipUseless = True
        if self.selectedSave == 1:
            self.game = Game(self)
            print "load teaching level save"
        elif self.selectedSave == 2:
            self.game = LevelTwo(self)
            print "load level two save"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        else:
            self.game = LevelTwo(self)
            print "load level three save"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        # self.soundMgr.setMusicVolume(0)
        # self.musicVolume = 0
        self.mainFrame.hide()
        # self.save = Save(self.game)

    def loadSave(self):
        print 'load save'
        self.mainFrame.hide()
        self.saveFrame.hide()
        self.loadVideo()
        thread.start_new_thread(self.loadGame, {})

    def loadGame(self):
        self.skipUseless = False
        if self.selectedSave == 1:
            self.game = Game(self)
            print "load teaching level"
        elif self.selectedSave == 2:
            self.game = LevelTwo(self)
            print "load level two"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        else:
            self.game = LevelThree(self)
            print "load level three"
            self.soundMgr.setMusicVolume(0)
            self.musicVolume = 0
        # self.soundMgr.setMusicVolume(0)
        # self.musicVolume = 0
        self.mainFrame.hide()
        self.save = Save(self.game)

    def deleteSave(self):
        print 'delete save'
        self.deleteDialog.show()

    def cancelDelete(self):
        self.deleteDialog.hide()

    def doDelete(self):
        print 'delete '
        # print self.selectedSave
        self.deleteDialog.hide()

    def saveToMain(self):
        self.saveFrame.hide()
        self.mainFrame.show()

    '''
    event in pauseFrame
    '''
    def backToGame(self):
        self.pauseFrame.hide()
        self.saveFrame.hide()
        self.game.gameState = ''
        self.game.node.state = ''
        self.game.node.initTask()
        # threading.currentThread().join('gameThread')
        base.accept('escape', self.game.pauseGame)
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        self.game.node.erosionFrame.show()
        self.game.node.currentItemFrame.show()

    def backToMenu(self):
        self.pauseFrame.hide()
        base.accept('escape', self.nothing)
        self.soundMgr.setMusicVolume(1)
        self.musicVolume = 100
        # remove game
        # self.gameThread.exit()
        # del self.game
        wp = WindowProperties()
        wp.setCursorHidden(False)
        self.mainFrame.show()
        self.game.node.mission.removeGame()
        self.tempPlayer = self.game.node
        self.removePlayer()

    def removePlayer(self):
        if self.game.node.node.is_empty():
            return
        self.game.node.node.hide()
        # texList = self.game.node.node.findAllTextures()
        # num = texList.getNumTextures()
        # for i in range(num):
        #     texList[i].releaseAll()
        #     loader.unloadTexture(texList[i])
        # self.game.node.node.removeNode()
        # # self.game.node.hide()
        # gc.collect()

    def backToSave(self):
        self.pauseFrame.hide()
        self.saveFrame.show()

    def saveCurrentGame(self):
        self.save.saveFile()

    def loadLastGame(self):
        self.save.loadFile()
        self.backToGame()
        self.infoDialog.show()
        self.infoLabel['text'] = '载入游戏成功'
        self.game.node.mission.resume()
        base.accept('b', self.game.openBag)
        if self.game.node.bag.model is not None:
            self.game.node.bag.model.detachNode()
            self.game.node.bag.textObject.setText('')

    def nothing(self):
        pass

    '''
    event in settingFrame
    '''
    def setMusicVolume(self):
        self.musicVolume = self.musicSlider['value']
        self.musicSlider['image_scale'] = (self.musicVolume / 100, 1, 1)
        self.musicSlider['image_pos'] = ((self.xSave + 4.1 * self.hCoor) - (1 - self.musicVolume / 100) * .9, self.ySave, self.zSave)
        self.soundMgr.setMusicVolume(self.musicVolume / 100.0)
        # print self.musicVolume

    def setVoiceVolume(self):
        self.voiceVolume = self.voiceSlider['value']
        self.voiceSlider['image_scale'] = (self.voiceVolume / 100, 1, 1)
        self.voiceSlider['image_pos'] = ((self.xSave + 4.1 * self.hCoor) - (1 - self.voiceVolume / 100) * .9, self.ySave, self.zSave)

    def settingToMain(self):
        self.settingFrame.hide()
        self.mainFrame.show()

    '''
    event in aboutFrame
    '''
    def aboutToMain(self):
        self.creditSound.stop()
        self.soundMgr.mySound.play()
        self.aboutFrame.hide()
        self.mainFrame.show()

    '''
    event in exitDialog
    '''
    def cancelExit(self):
        # print 'cancel'
        self.dialog.hide()
        self.mainFrame.show()

    '''
    event in mainFrame
    '''
    def startGame(self):
        print 'start game'
        # self.saveFrame.show()
        self.levelFrame.show()

    def continueGame(self):
        print 'continue game'
        self.saveFrame.show()

    def settingGame(self):
        print 'setting game'
        self.settingFrame.show()

    def aboutGame(self):
        print 'about game'
        self.aboutFrame.show()
        self.mainFrame.hide()
        self.creditSound.setVolume(1)
        self.soundMgr.mySound.stop()
        self.creditSound.play()

    def exitGame(self):
        print 'exit game'
        self.dialog.show()

    def isExit(self, arg):
        if arg:
            sys.exit()
        else:
            self.dialog.hide()

    def show(self):
        self.mainFrame.show()

    def hide(self):
        self.mainFrame.hide()
