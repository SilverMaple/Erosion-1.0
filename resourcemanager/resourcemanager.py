import os

class ResourceManager:
    def __init__(self):
        self.resources = []
        self.path = os.getcwd() + "/"
        self.path = ''
        self.resource_folder = "res"
        self.model_folder = 'models'
        self.sound_folder = 'sounds'
        
    """
    def traverseResFolder(self):
        pass #codice che analizza la cartella res e per ogni elemento
             #aggiunge ['key',Resource()] a self.resources
    """
    
    def get_path(self):
        return self.path + self.resource_folder + "/"
    
    def getResource(self, key):
        object_path = self.path + self.resource_folder + "/" + key
        return object_path               #"full resource absoulute path (value)"

    def getModelResource(self, key):
        model_path = self.path + self.resource_folder + "/" + self.model_folder + "/" + key
        return model_path

    def getSoundResource(self, key):
        sound_path = self.path + self.resource_folder + "/" + self.sound_folder + "/" + key
        return sound_path
