class Pause(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        # default no time limit
        self.pauseTime = None
        # function executed after pause
        self.func = None
        
    # for timed pauses
    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func
        return None

    # general pause
    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    # change state pause
    def flip(self):
        self.paused = not self.paused
