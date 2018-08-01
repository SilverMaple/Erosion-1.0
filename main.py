from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData('', 'text-encoding utf8')
loadPrcFileData('', 'textures-power-2 none')

class ErosionApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        from gui.menu import Menu
        self.m = Menu()

app = ErosionApp()
app.run()
