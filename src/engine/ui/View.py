
# Interface for the View
class View:

    def __init__(self):
        raise NotImplementedError

    def tick(self, deltaTime):
        raise NotImplementedError