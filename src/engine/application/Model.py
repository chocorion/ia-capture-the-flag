
# Interface for the Model
class Model:

    def __init__(self):
        raise NotImplementedError

    def tick(self, deltaTime):
        raise NotImplementedError

    def register(self, player):
        raise NotImplementedError