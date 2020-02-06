
# Interface for the Controller
class Controller:

    def __init__(self):
        raise NotImplementedError

    def tick(self, deltaTime):
        raise NotImplementedError