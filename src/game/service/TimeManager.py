import time

from service.Config import Config

class TimeManager:
    """
    Various methods to help with Time.

    Can be used as a Stopwatch and/or Frame Counter.

    Attributes:
        current (int): The time in milliseconds at which the stopwatch started.
        last (int): The time in milliseconds at which the stopwatch was last marked.
        now (int): The time in milliseconds at which the stopwatch was last peeked.
    """

    def StartTimer(self):
        """
        Starts to keep track of time. This also resets the timer.
        """
        self.StopTimer()
        self.current = self.GetTimeMs()
        self.last = self.current

    def StopTimer(self):
        """
        Resets the timer.
        """
        self.current = None
        self.last = None
        self.now = None

    def GetTimeMs(self):
        """
        Get the time in milliseconds, regardless of the timer's state.

        Returns:
            time (int) : Time in milliseconds.
        """
        return int(round(time.time() * 1000))

    def PeekDeltaTimeMs(self):
        """
        Get the time difference since last mark.

        Returns:
            deltaTime (int) : Time delta in milliseconds since last call to Mark() or StartTimer().
        """
        self.now = self.GetTimeMs()
        deltaTime = self.now - self.last
        return deltaTime

    def Mark(self):
        """
        Reset deltatime measure.
        """
        self.last = self.GetTimeMs()

    def DeltaTimeMs(self):
        """
        Get the time difference since last call to this function or Mark().
        
        Use only between a call for Start and a call for Stop.

        Returns:
            deltaTime (int) : Time delta in milliseconds since last call to Mark() or StartTimer().
        """
        deltaTime = self.PeekDeltaTimeMs()
        self.Mark()
        return deltaTime

    def NextFrame(self):
        """
        Wait for next frame depending on the Framerate found in Config.

        To use this method, you need to initialize Config at least once during runtime.

        Returns:
            deltaTime (int) : Time delta in milliseconds since last call to Mark() or StartTimer().
        """
        msWait = 1000 / Config.Framerate()

        deltaTime = self.PeekDeltaTimeMs()
        slept = 0
        if deltaTime < msWait: 
            slept = msWait - deltaTime
            time.sleep(slept/1000)
            deltaTime = msWait


        print("Tickrate: {} tick/s ({:2d}% time usage)".format(round(1000/deltaTime,2),round((msWait-slept)/msWait*100)), end='\r')
        
        return deltaTime