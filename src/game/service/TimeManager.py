import time

from service.Config import Config

class TimeManager:

    def __init__(self):
        self.current = None
        self.last = None

    def StartTimer(self):
        self.current = self.GetTimeMs()
        self.last = self.current

    def StopTimer(self):
        self.current = None
        self.last = None

    # Get time in milliseconds regardless of the timer state
    def GetTimeMs(self):
        return int(round(time.time() * 1000))

    # Check the time difference since last check
    def PeekDeltaTimeMs(self):
        self.now = self.GetTimeMs()
        deltaTime = self.now - self.last
        return deltaTime

    # Reset deltatime measure
    def Mark(self):
        self.last = self.GetTimeMs()

    # Use only between a call for Start and a call for Stop
    def DeltaTimeMs(self):
        deltaTime = self.PeekDeltaTimeMs()
        self.Mark()
        return deltaTime

    # Wait for next frame depending on framerate
    def NextFrame(self):
        msWait = 1000 / Config.Framerate()

        deltaTime = self.PeekDeltaTimeMs()
        if deltaTime < msWait: 
            time.sleep((msWait - deltaTime)/1000)
            deltaTime = msWait
        
        return deltaTime