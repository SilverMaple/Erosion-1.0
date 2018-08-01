from direct.showbase.DirectObject import DirectObject
from direct.interval.LerpInterval import LerpFunc
from resourcemanager.resourcemanager import ResourceManager

class AudioManager(DirectObject):

    def __init__ (self):
        #for bgmusic
        self.isPlaying = False
        self.mySound = False
        #for long effects
        self.effects = {}
        
    #apicall
    def playMusic(self, bgmusic):
        if(self.isPlaying):
            self.mySound.stop()
        path = ResourceManager().getSoundResource(bgmusic)
        self.mySound = base.loader.loadSfx(path)
        self.mySound.setVolume(1)
        self.mySound.setLoop(True)
        self.mySound.play()
        self.isPlaying = True
    
    '''stop music fading in given time'''
    def stopMusic(self, time):
        if(self.isPlaying):
            i = LerpFunc(self.stopMusicLerp,
             fromData=1,
             toData=0,
             duration=time,
             blendType='noBlend',
             extraArgs=[],
             name=None).start()
    
    def stopMusicLerp(self, t):
        self.mySound.setVolume(t)
        if t==0:
            self.mySound.stop()

    def setMusicVolume(self, t):
        self.mySound.setVolume(t)
    
    #apicall
    def playEffect(self, effect):
        path = resourceManager.getResource(effect)
        effect = base.loader.loadSfx(path)
        effect.setVolume(1)
        effect.play()
        
    #apicall
    def playLongEffect(self, name, effect, time=2):
        if self.effects.has_key(name) == False:
            path = resourceManager.getResource(effect)
            effect = base.loader.loadSfx(path)
            effect.setVolume(0.01)
            effect.setLoop(True)
            self.effects[name] = effect
            effect.play()
            
            i = LerpFunc(self.playLongEffectLerp,
             fromData=0,
             toData=1,
             duration=time,
             blendType='noBlend',
             extraArgs=[effect],
             name=None).start()
            
        else:
            print "AUDIOMANAGER: you have to stop", name, " long effect before spawning a new one!"
    
    def playLongEffectLerp(self, t, effect):
        effect.setVolume(t)
        
        
    
    #apicall
    def stopLongEffect(self, name):
        if self.effects.has_key(name):
            self.effects[name].stop()
            del self.effects[name]
    
    #apicall
    def clearAllEffects(self):
        for e in self.effects[:]:
            e.stop()
            self.effects.remove(e)
    
