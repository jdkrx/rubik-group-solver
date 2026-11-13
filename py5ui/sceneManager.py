import py5

class SceneManager:
    def __init__(self):
        self.scenes = []
        self.actualscene = 0
    def addScene(self, scene):
        self.scenes.append(scene)
        return len(self.scenes) - 1 # Devuelve el ID de la escena
    def display(self):
        self.scenes[self.actualscene]()
    def sceneGoTo(self, n):
        self.actualscene = n
    def getScene(self):
        return self.actualscene