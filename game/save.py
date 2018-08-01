# -*- coding:utf-8 -*-
from bag import Goods
from password import Password, Epassword, Boxpassword


class Save:
    def __init__(self, game):
        self.game = game
        self.player = game.node
        self.bag = self.player.bag
        self.gm = self.player.goodmanager

    def loadFile(self, file=None):
        if file is None:
            f = open('gameinfo.save', 'rb')
        else:
            f = open(file, 'rb')
        data = f.read()
        d = eval(data)
        self.loadSaveDict(d)
        f.close()

    def saveFile(self):
        f = open('gameinfo.save', 'wb')
        # f.write(str(self.getSaveDict()).replace(', ', ',\n\t').replace(': {', ': \n\t{'))
        f.write(str(self.getSaveDict()))
        f.close()

    def loadSaveDict(self, allDict):
        # print allDict
        # restore bag state
        self.bag.removeAllItem()
        self.bag.item_num = 0
        # print 'item_num', self.bag.item_num
        # self.bag.item_num = allDict['bagDict']['item_num']
        self.bag.injectTimes = allDict['bagDict']['injectTimes']
        self.bag.enemyInteractTimes = allDict['bagDict']['enemyInteractTimes']
        for i in allDict['bagDict']['items']:
            picture = allDict['bagDict']['items'][i]
            info = self.getInfo(picture)
            self.bag.addItem(Goods(picture, info[0], info[1]))

        # itemDict = {}
        # for i in self.bag.items:
        #     itemDict[i.id] = i.goods.picture
        # bagDict['items'] = itemDict

        # restore goods state
        if self.game.levelName == 'tutorial':
            doorState = self.gm.GoodsIta['toilet_door'].state
            wordState = self.gm.GoodsIta['Scene1_wallword_1'].state
            self.gm.GoodsIta['box'].state = allDict['goodStateDict']['box']
            self.gm.GoodsIta['enemy'].state = allDict['goodStateDict']['enemy']
            self.gm.GoodsIta['bed_box'].state = allDict['goodStateDict']['bed_box']
            self.gm.GoodsIta['yaoshui'].state = allDict['goodStateDict']['yaoshui']
            self.gm.GoodsIta['MusicBox'].state = allDict['goodStateDict']['MusicBox']
            self.gm.GoodsIta['xishoupen'].state = allDict['goodStateDict']['xishoupen']
            self.gm.GoodsIta['toilet_door'].state = allDict['goodStateDict']['toilet_door']
            self.gm.GoodsIta['Scene1_Exit'].state = allDict['goodStateDict']['Scene1_Exit']
            self.gm.GoodsIta['matong_box3'].state = allDict['goodStateDict']['matong_box3']
            self.gm.GoodsIta['bookshelf_box'].state = allDict['goodStateDict']['bookshelf_box']
            self.gm.GoodsIta['Scene1_wallword_1'].state = allDict['goodStateDict']['Scene1_wallword_1']

            if self.gm.GoodsIta['toilet_door'].state is not "":
                if self.player.mission.password == None:
                    self.player.mission.password = Password()
                self.player.mission.password.passState = True
            if self.gm.GoodsIta['toilet_door'].state == "unlockedOpen" and doorState is not "unlockedOpen" or\
                                    self.gm.GoodsIta['toilet_door'].state == "unlockedClose" and doorState is not "unlockedClose":
                self.player.mission.password.passwordFrame.hide()
                self.player.mission.password.unloadLeap()
                self.player.goodmanager.GoodsIta['toilet_door'].OnClick()

            if self.gm.GoodsIta['Scene1_wallword_1'].state == "changed":
                self.player.goodmanager.GoodsIta["Scene1_wallword_1"].CloseHighLight()
                self.player.goodmanager.GoodsIta["Scene1_wallword_1"].Node.hide()
                self.player.goodmanager.GoodsIta["Scene1_wallword_2"].Node.show()
                self.player.mission.resume()
                self.player.initTask()
            elif self.gm.GoodsIta['Scene1_wallword_1'].state is not "changed" and wordState == "changed":
                self.player.goodmanager.GoodsIta["Scene1_wallword_2"].CloseHighLight()
                self.player.goodmanager.GoodsIta["Scene1_wallword_2"].Node.hide()
                self.player.goodmanager.GoodsIta["Scene1_wallword_1"].Node.show()
                self.player.mission.resume()
                self.player.initTask()

        elif self.game.levelName == 'levelTwo':
            frontDoorState = self.gm.GoodsIta['Frontdoor'].state
            backDoorState = self.gm.GoodsIta['Backdoor'].state
            outDoorState = self.gm.GoodsIta['outdoor_box'].state
            hammerState = self.gm.GoodsIta['hammer_box'].state
            mirrorState = self.gm.GoodsIta['mirror_box'].state
            vState = self.gm.GoodsIta['vaccine_box'].state
            hallvState = self.gm.GoodsIta['hallvaccine_box'].state
            kState = self.gm.GoodsIta['knife_box'].state
            inkState = self.gm.GoodsIta['inknife_box'].state
            checkState = self.player.mission.checkState
            self.gm.GoodsIta['dianti_box'].state = allDict['goodStateDict']['dianti_box']
            self.gm.GoodsIta['broken_dianti_box'].state = allDict['goodStateDict']['broken_dianti_box']
            self.gm.GoodsIta['ElectricBox'].state = allDict['goodStateDict']['ElectricBox']
            self.gm.GoodsIta['diary_box'].state = allDict['goodStateDict']['diary_box']
            self.gm.GoodsIta['Frontdoor'].state = allDict['goodStateDict']['Frontdoor']
            self.gm.GoodsIta['Backdoor'].state = allDict['goodStateDict']['Backdoor']
            self.gm.GoodsIta['outdoor_box'].state = allDict['goodStateDict']['outdoor_box']
            self.gm.GoodsIta['safe_box'].state = allDict['goodStateDict']['safe_box']
            self.gm.GoodsIta['window_box'].state = allDict['goodStateDict']['window_box']
            self.gm.GoodsIta['window_broken_box'].state = allDict['goodStateDict']['window_broken_box']
            self.gm.GoodsIta['vaccine_box'].state = allDict['goodStateDict']['vaccine_box']
            self.gm.GoodsIta['hallvaccine_box'].state = allDict['goodStateDict']['hallvaccine_box']
            self.gm.GoodsIta['knife_box'].state = allDict['goodStateDict']['knife_box']
            self.gm.GoodsIta['inknife_box'].state = allDict['goodStateDict']['inknife_box']
            self.gm.GoodsIta['furnace_box'].state = allDict['goodStateDict']['furnace_box']
            self.gm.GoodsIta['infurnace_box'].state = allDict['goodStateDict']['infurnace_box']
            self.gm.GoodsIta['mirror_box'].state = allDict['goodStateDict']['mirror_box']
            self.gm.GoodsIta['bookshelf_box'].state = allDict['goodStateDict']['bookshelf_box']
            self.gm.GoodsIta['inbookshelf_box'].state = allDict['goodStateDict']['inbookshelf_box']
            self.gm.GoodsIta['hammer_box'].state = allDict['goodStateDict']['hammer_box']
            self.gm.GoodsIta['painting_8'].state = allDict['goodStateDict']['painting_8']
            self.player.mission.inFlowerNum = allDict['goodStateDict']['inFlowerNum']
            self.player.mission.outFlowerNum = allDict['goodStateDict']['outFlowerNum']
            self.player.mission.checkState = allDict['goodStateDict']['checkState']
            self.game.enemyState = allDict['goodStateDict']['enemyState']

            if self.gm.GoodsIta['safe_box'] is not 'unlocked':
                if self.player.mission.boxPassword == None:
                    self.player.mission.boxPassword = Boxpassword()
                    self.player.mission.boxPassword.passwordFrame.hide()
                self.player.mission.boxPassword.passState = False

            if self.gm.GoodsIta['Frontdoor'].state is not "" or self.gm.GoodsIta['Backdoor'].state is not "":
                if self.player.mission.hallPassword == None:
                    self.player.mission.hallPassword = Epassword()
                    self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.passState = True

            if self.gm.GoodsIta['Frontdoor'].state == "unlockedOpen" and frontDoorState is not "unlockedOpen":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['Frontdoor'].OpenDoor()
            elif self.gm.GoodsIta['Frontdoor'].state == "unlockedClose" and frontDoorState is not "unlockedClose":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['Frontdoor'].CloseDoor()

            if self.gm.GoodsIta['Backdoor'].state == "unlockedOpen" and backDoorState is not "unlockedOpen":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['Backdoor'].OpenDoor()
            elif self.gm.GoodsIta['Backdoor'].state == "unlockedClose" and backDoorState is not "unlockedClose":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['Backdoor'].CloseDoor()

            if self.gm.GoodsIta['outdoor_box'].state == "unlockedOpen" and outDoorState is not "unlockedOpen":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['outdoor_box'].OpenDoor()
            elif self.gm.GoodsIta['outdoor_box'].state == "unlockedClose" and outDoorState is not "unlockedClose":
                self.player.mission.hallPassword.passwordFrame.hide()
                self.player.mission.hallPassword.unloadLeap()
                self.player.goodmanager.GoodsIta['outdoor_box'].CloseDoor()

            if self.gm.GoodsIta['hammer_box'].state == "picked" and hammerState is not "picked":
                self.player.goodmanager.GoodsIta['hammer_box'].Node.hide()
                self.player.goodmanager.UnLoad('hammer_box')
            elif self.gm.GoodsIta['hammer_box'].state is not "picked" and hammerState == "picked":
                self.player.goodmanager.Load('hammer_box')
                self.player.goodmanager.GoodsIta['hammer_box'].Node.show()
            if self.gm.GoodsIta['vaccine_box'].state == "picked" and vState is not "picked":
                self.player.goodmanager.GoodsIta['vaccine_box'].Node.hide()
                self.player.goodmanager.UnLoad('vaccine_box')
            elif self.gm.GoodsIta['vaccine_box'].state is not "picked" and vState == "picked":
                self.player.goodmanager.Load('vaccine_box')
                self.player.goodmanager.GoodsIta['vaccine_box'].Node.show()
            if self.gm.GoodsIta['hallvaccine_box'].state == "picked" and hallvState is not "picked":
                self.player.goodmanager.GoodsIta['hallvaccine_box'].Node.hide()
                self.player.goodmanager.UnLoad('hallvaccine_box')
            elif self.gm.GoodsIta['hallvaccine_box'].state is not "picked" and hallvState == "picked":
                self.player.goodmanager.Load('hallvaccine_box')
                self.player.goodmanager.GoodsIta['hallvaccine_box'].Node.show()
            if self.gm.GoodsIta['knife_box'].state == "picked" and kState is not "picked":
                self.player.goodmanager.GoodsIta['knife_box'].Node.hide()
                self.player.goodmanager.UnLoad('knife_box')
            elif self.gm.GoodsIta['knife_box'].state is not "picked" and kState == "picked":
                self.player.goodmanager.Load('knife_box')
                self.player.goodmanager.GoodsIta['knife_box'].Node.show()
            if self.gm.GoodsIta['inknife_box'].state == "picked" and inkState is not "picked":
                self.player.goodmanager.GoodsIta['inknife_box'].Node.hide()
                self.player.goodmanager.UnLoad('inknife_box')
            elif self.gm.GoodsIta['inknife_box'].state is not "picked" and inkState == "picked":
                self.player.goodmanager.Load('inknife_box')
                self.player.goodmanager.GoodsIta['inknife_box'].Node.show()
            if self.gm.GoodsIta['mirror_box'].state == "smashed" and mirrorState is not "smashed":
                self.player.goodmanager.GoodsIta['mirror_box'].Node.hide()
                self.player.game.UnLoadmirror()
                self.player.goodmanager.UnLoad('mirror_box')
            elif self.gm.GoodsIta['mirror_box'].state is not "smashed" and mirrorState == "smashed":
                self.player.goodmanager.Load('mirror_box')
                self.player.goodmanager.GoodsIta['mirror_box'].Node.show()

            if self.gm.GoodsIta['painting_8'].state == 'done':
                self.player.goodmanager.GoodsIta['painting_8'].Node.hide()
                self.player.goodmanager.UnLoad('painting_8')
                self.player.goodmanager.Load('painting_cut')
                self.player.goodmanager.GoodsIta['painting_cut'].Node.show()
            else:
                self.player.goodmanager.GoodsIta['painting_cut'].Node.hide()
                self.player.goodmanager.Load('painting_8')
                self.player.goodmanager.GoodsIta['painting_8'].Node.show()

            self.player.mission.initFlowers()
            if self.player.mission.checkState == True and checkState == False:
                taskMgr.remove('checkFlowerNum')
            elif self.player.mission.checkState == False and checkState == True:
                taskMgr.add(self.player.mission.checkFlowerNum, "checkFlowerNum")

            self.game.enemy.initState(self.game.enemyState)

        elif self.game.levelName == 'levelThree':
            chessdoorState = self.gm.GoodsIta['chessdoor_box'].state
            labdoorState = self.gm.GoodsIta['labdoor_box'].state
            studydoorState = self.gm.GoodsIta['studydoor_box'].state
            bottleState = self.gm.GoodsIta['emptybottle_box'].state
            v1State = self.gm.GoodsIta['vaccine1_box'].state
            v2State = self.gm.GoodsIta['vaccine2_box'].state
            v3State = self.gm.GoodsIta['vaccine_studyroom_box'].state
            self.gm.GoodsIta['elebutton_box'].state = allDict['goodStateDict']['elebutton_box']
            self.gm.GoodsIta['labdoor_box'].state = allDict['goodStateDict']['labdoor_box']
            self.gm.GoodsIta['studydoor_box'].state = allDict['goodStateDict']['studydoor_box']
            self.gm.GoodsIta['chessdoor_box'].state = allDict['goodStateDict']['chessdoor_box']
            self.gm.GoodsIta['exit_box'].state = allDict['goodStateDict']['exit_box']
            self.gm.GoodsIta['emptybottle_box'].state = allDict['goodStateDict']['emptybottle_box']
            self.gm.GoodsIta['bookshelf_box'].state = allDict['goodStateDict']['bookshelf_box']
            self.gm.GoodsIta['vaccine1_box'].state = allDict['goodStateDict']['vaccine1_box']
            self.gm.GoodsIta['vaccine2_box'].state = allDict['goodStateDict']['vaccine2_box']
            self.gm.GoodsIta['vaccine_studyroom_box'].state = allDict['goodStateDict']['vaccine_studyroom_box']
            self.player.mission.chessBoard.state = allDict['goodStateDict']['chessState']

            self.player.mission.chessBoard.initPos(self.player.mission.chessBoard.state)
            if self.gm.GoodsIta['chessdoor_box'].state == "unlockedOpen" and chessdoorState is not "unlockedOpen":
                self.player.goodmanager.GoodsIta['chessdoor_box'].OpenDoor()
            elif self.gm.GoodsIta['chessdoor_box'].state == "unlockedClose" and chessdoorState is not "unlockedClose":
                self.player.goodmanager.GoodsIta['chessdoor_box'].CloseDoor()

            if self.gm.GoodsIta['labdoor_box'].state == "unlockedOpen" and labdoorState is not "unlockedOpen":
                self.player.goodmanager.GoodsIta['labdoor_box'].OpenDoor()
            elif self.gm.GoodsIta['labdoor_box'].state == "unlockedClose" and labdoorState is not "unlockedClose":
                self.player.goodmanager.GoodsIta['labdoor_box'].CloseDoor()

            if self.gm.GoodsIta['studydoor_box'].state == "unlockedOpen" and studydoorState is not "unlockedOpen":
                self.player.goodmanager.GoodsIta['studydoor_box'].OpenDoor()
            elif self.gm.GoodsIta['studydoor_box'].state == "unlockedClose" and studydoorState is not "unlockedClose":
                self.player.goodmanager.GoodsIta['studydoor_box'].CloseDoor()

            if self.gm.GoodsIta['emptybottle_box'].state == "picked" and bottleState is not "picked":
                self.player.goodmanager.GoodsIta['emptybottle_box'].Node.hide()
                self.player.goodmanager.UnLoad('emptybottle_box')
            elif self.gm.GoodsIta['emptybottle_box'].state is not "picked" and bottleState == "picked":
                self.player.goodmanager.Load('emptybottle_box')
                self.player.goodmanager.GoodsIta['emptybottle_box'].Node.show()
            if self.gm.GoodsIta['vaccine1_box'].state == "picked" and v1State is not "picked":
                self.player.goodmanager.GoodsIta['vaccine1_box'].Node.hide()
                self.player.goodmanager.UnLoad('vaccine1_box')
            elif self.gm.GoodsIta['vaccine1_box'].state is not "picked" and v1State == "picked":
                self.player.goodmanager.Load('emptybottle_box')
                self.player.goodmanager.GoodsIta['emptybottle_box'].Node.show()
            if self.gm.GoodsIta['vaccine2_box'].state == "picked" and v2State is not "picked":
                self.player.goodmanager.GoodsIta['vaccine2_box'].Node.hide()
                self.player.goodmanager.UnLoad('vaccine2_box')
            elif self.gm.GoodsIta['vaccine2_box'].state is not "picked" and v2State == "picked":
                self.player.goodmanager.Load('vaccine2_box')
                self.player.goodmanager.GoodsIta['vaccine2_box'].Node.show()
            if self.gm.GoodsIta['vaccine_studyroom_box'].state == "picked" and v3State is not "picked":
                self.player.goodmanager.GoodsIta['vaccine_studyroom_box'].Node.hide()
                self.player.goodmanager.UnLoad('vaccine_studyroom_box')
            elif self.gm.GoodsIta['vaccine_studyroom_box'].state is not "picked" and v3State == "picked":
                self.player.goodmanager.Load('vaccine_studyroom_box')
                self.player.goodmanager.GoodsIta['vaccine_studyroom_box'].Node.show()

        self.player.isInteractive = allDict['playerDict']['isInteractive']
        self.player.SLOW = allDict['playerDict']['isInteractive']
        self.player.EROSION = allDict['playerDict']['erosion']
        self.player.mission.memoryNum = allDict['playerDict']['memoryNum']
        self.player.node.setPos(allDict['playerDict']['pos'])
        self.player.node.setHpr(allDict['playerDict']['hpr'])
        self.player.cameraState = allDict['playerDict']['cameraState']
        self.player.visionState = allDict['playerDict']['visionState']
        base.accept("mouse1", self.player.__setattr__, ["LeftButton", 1])
        base.accept("mouse1-up", self.player.__setattr__, ["LeftButton", 0])

    def getSaveDict(self):
        bagDict = {
            'item_num': self.bag.item_num,
            'items': self.bag.items,
            'injectTimes': self.bag.injectTimes,
            'enemyInteractTimes': self.bag.enemyInteractTimes
        }
        itemDict = {}
        for i in self.bag.items:
            itemDict[i.id] = i.goods.picture
        bagDict['items'] = itemDict

        goodStateDict = {}
        if self.game.levelName == 'tutorial':
            goodStateDict = {
                'box': self.gm.GoodsIta['box'].state,
                'enemy': self.gm.GoodsIta['enemy'].state,
                'bed_box': self.gm.GoodsIta['bed_box'].state,
                'yaoshui': self.gm.GoodsIta['yaoshui'].state,
                'MusicBox': self.gm.GoodsIta['MusicBox'].state,
                'xishoupen': self.gm.GoodsIta['xishoupen'].state,
                'toilet_door': self.gm.GoodsIta['toilet_door'].state,
                'Scene1_Exit': self.gm.GoodsIta['Scene1_Exit'].state,
                'matong_box3': self.gm.GoodsIta['matong_box3'].state,
                'bookshelf_box': self.gm.GoodsIta['bookshelf_box'].state,
                'Scene1_wallword_1': self.gm.GoodsIta['Scene1_wallword_1'].state
            }
        elif self.game.levelName == 'levelTwo':
            goodStateDict = {
                'dianti_box': self.gm.GoodsIta['dianti_box'].state,
                'broken_dianti_box': self.gm.GoodsIta['broken_dianti_box'].state,
                'ElectricBox': self.gm.GoodsIta['ElectricBox'].state,
                'diary_box': self.gm.GoodsIta['diary_box'].state,
                'Frontdoor': self.gm.GoodsIta['Frontdoor'].state,
                'Backdoor': self.gm.GoodsIta['Backdoor'].state,
                'outdoor_box': self.gm.GoodsIta['outdoor_box'].state,
                'safe_box': self.gm.GoodsIta['safe_box'].state,
                'window_box': self.gm.GoodsIta['window_box'].state,
                'window_broken_box': self.gm.GoodsIta['window_broken_box'].state,
                'vaccine_box': self.gm.GoodsIta['vaccine_box'].state,
                'hallvaccine_box': self.gm.GoodsIta['hallvaccine_box'].state,
                'knife_box': self.gm.GoodsIta['knife_box'].state,
                'inknife_box': self.gm.GoodsIta['inknife_box'].state,
                'furnace_box': self.gm.GoodsIta['furnace_box'].state,
                'infurnace_box': self.gm.GoodsIta['infurnace_box'].state,
                'mirror_box': self.gm.GoodsIta['mirror_box'].state,
                'bookshelf_box': self.gm.GoodsIta['bookshelf_box'].state,
                'inbookshelf_box': self.gm.GoodsIta['inbookshelf_box'].state,
                'hammer_box': self.gm.GoodsIta['hammer_box'].state,
                'painting_8': self.gm.GoodsIta['painting_8'].state,
                'inFlowerNum': self.player.mission.inFlowerNum,
                'outFlowerNum': self.player.mission.outFlowerNum,
                'checkState': self.player.mission.checkState,
                'enemyState': self.game.enemy.state
            }
        elif self.game.levelName == 'levelThree':
            goodStateDict = {
                'elebutton_box': self.gm.GoodsIta['elebutton_box'].state,
                'labdoor_box': self.gm.GoodsIta['labdoor_box'].state,
                'studydoor_box': self.gm.GoodsIta['studydoor_box'].state,
                'chessdoor_box': self.gm.GoodsIta['chessdoor_box'].state,
                'exit_box': self.gm.GoodsIta['exit_box'].state,
                'emptybottle_box': self.gm.GoodsIta['emptybottle_box'].state,
                'bookshelf_box': self.gm.GoodsIta['bookshelf_box'].state,
                'vaccine1_box': self.gm.GoodsIta['vaccine1_box'].state,
                'vaccine2_box': self.gm.GoodsIta['vaccine2_box'].state,
                'vaccine_studyroom_box': self.gm.GoodsIta['vaccine_studyroom_box'].state,
                'key_box': self.gm.GoodsIta['key_box'].state,
                'chessState': self.player.mission.chessBoard.state
            }

        playerDict = {
            'isInteractive': False,
            'SLOW': self.player.SLOW,
            'erosion': self.player.EROSION,
            'memoryNum': self.player.mission.memoryNum,
            'pos': tuple(self.player.node.getPos()),
            'hpr': tuple(self.player.node.getHpr()),
            'cameraState': self.player.cameraState,
            'visionState': self.player.visionState,
        }
        allDict = {
            'bagDict': bagDict,
            'playerDict': playerDict,
            'goodStateDict': goodStateDict
        }
        return allDict

    def getInfo(self, pic):
        # prefix = 'res/models/items/'
        info = [None]
        pic = pic[17: -4]
        if pic == 'torch':
            info = [self.bag.torch, '一个手电筒']
        elif pic == 'photo':
            info = [self.bag.photo, '一张合影']
        elif pic == 'paper':
            info = [self.bag.paper, '一张纸条']
        elif pic == 'spring':
            info = [self.bag.spring, '发条']
        elif pic == 'injection':
            info = [self.bag.injection, '抑制剂']

        if self.game.levelName == 'tutorial':
            return info

        if pic == 'cake':
            info = [self.bag.cake, '一块大蛋糕']
        elif pic == 'knife':
            info = [self.bag.knife, '一把裁纸刀']
        elif pic == 'hammer':
            info = [self.bag.hammer, '一只锤子']
        elif pic == 'flower':
            info = [self.bag.flower, '一朵纸花']
        elif pic == 'carrot':
            info = [self.bag.carrot, '一根胡萝卜']
        elif pic == 'inknife':
            info = [self.bag.inknife, '一把裁纸刀']
        elif pic == 'funBook':
            info = [self.bag.funBook, '《莎士比亚喜剧集》']
        elif pic == 'sadBook':
            info = [self.bag.sadBook, '《莎士比亚悲剧集》']
        elif pic == 'goldenKey':
            info = [self.bag.goldenKey, '一把金色钥匙']
        elif pic == 'gaoshuBook':
            info = [self.bag.gaoshuBook, '《高等数学分析》']
        elif pic == 'rabbit_dead':
            info = [self.bag.deadRabbit, '一只死兔']
        elif pic == 'rabbit_alive':
            info = [self.bag.rabbit, '一只实验兔']
        elif pic == 'copperplate_clean':
            info = [self.bag.copperplate_clean, '干净的铜板']
        elif pic == 'copperplate_rusted':
            info = [self.bag.copperplate_rusted, '锈迹斑斑的铜板']

        if self.game.levelName is 'levelTwo':
            return info

        if pic == 'bottle':
            info = [self.bag.bottle, '一个装满水的瓶子']
        elif pic == 'bottle_empty':
            info = [self.bag.emptyBottle, '一个空瓶子']
        elif pic == 'roomKey':
            info = [self.bag.roomKey, '一把钥匙']

        return info
