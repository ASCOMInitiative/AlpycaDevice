# =================================================================
# ROTATORDEVICE.PY - Poor-man's simulaton of a Rotator
# =================================================================
# This is only for demo purposes. It's extremely fragile, and should
# not be used as an example of a real device. Settings not remembered.
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#
from threading import Timer
from threading import Lock

class RotatorDevice(object):
    """Implements a rotator device that runs in a separate thread"""
    #
    # Only override __init_()  and run() (pydoc 17.1.2)
    #
    def __init__(self):
        self._lock = Lock()
        self.name = 'device'
        #
        # Rotator device constants
        #
        self._can_reverse = True
        self._step_size = 1.0
        self._steps_per_sec = 6
        #
        # Rotator device state variables
        #
        self._reverse = False
        self._position = 0.0
        self._target_position = 0.0
        self._is_moving = False
        self._connected = False
        #
        # Rotator engine
        #
        self._timer = None
        self._interval = 1.0 / self._steps_per_sec
        self._stopped = True

    def start(self, from_run=False):
        #print('[start] try to lock')
        self._lock.acquire()
        #print('[start] got lock')
        if from_run or self._stopped:
            self._stopped = False
            #print('[start] new timer')
            self._timer = Timer(self._interval, self._run)
            #print('[start] now start the timer')
            self._timer.start()
            #print('[start] timer started')
            self._lock.release()
            #print('[start] lock released')
        else:
            self._lock.release()
            #print('[start] lock released')


    def _run(self):
        #print('[_run] (tmr expired) get lock')
        self._lock.acquire()
        #print('[_run] got lock : tgtpos=' + str(self._target_position) + ' pos=' + str(self._position))
        delta = self._target_position - self._position
        #if delta >= 360.0:
        #    delta -= 360.0
        #if delta < 0.0:
        #    delta += 360.0
        #    print('[_run] final delta = ' + str(delta))
        if abs(delta) > (self._step_size / 2.0):
            self._is_moving = True
            if delta > 0:
                #print('[_run] delta > 0 go positive')
                self._position += self._step_size
                if self._position >= 360.0:
                    self._position -= 360.0
            else:
                #print('[_run] delta < 0 go negative')
                self._position -= self._step_size
                if self._position < 0.0:
                    self._position += 360.0
            print('[_run] new pos = ' + str(self._position))
        else:
            self._is_moving = False
            self._stopped = True
        self._lock.release()
        #print('[_run] lock released')
        if self._is_moving:
            #print('[_run] more motion needed, start another timer interval')
            self.start(from_run = True)

    def stop(self):
        self._lock.acquire()
        print('[stop] Stopping...')
        self._stopped = True
        self._is_moving = False
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None
        self._lock.release()

    #
    # Guarded properties
    # **TODO** Catch lock failures and raise error.
    #
    @property
    def can_reverse(self):
        self._lock.acquire()
        res =  self._can_reverse
        self._lock.release()
        return res

    @property
    def reverse(self):
        self._lock.acquire()
        res =  self._reverse
        self._lock.release()
        return res
    @reverse.setter
    def reverse (self, reverse):
        self._lock.acquire()
        self._reverse = reverse
        self._lock.release()

    @property
    def step_size(self):
        self._lock.acquire()
        res =  self._step_size
        self._lock.release()
        return res
    @step_size.setter
    def step_size (self, step_size):
        self._lock.acquire()
        self._step_size = step_size
        self._lock.release()

    @property
    def steps_per_sec(self):
        self._lock.acquire()
        res =  self._steps_per_sec
        self._lock.release()
        return res
    @steps_per_sec.setter
    def steps_per_sec (self, steps_per_sec):
        self._lock.acquire()
        self._steps_per_sec = steps_per_sec
        self._lock.release()

    @property
    def position(self):
        self._lock.acquire()
        res = self._position
        print('[position] ' + str(res))
        self._lock.release()
        return res

    @property
    def target_position(self):
        self._lock.acquire()
        res =  self._target_position
        print('[target_position] ' + str(res))
        self._lock.release()
        return res

    @property
    def is_moving(self):
        self._lock.acquire()
        res =  self._is_moving
        print('[is_moving] ' + str(res))
        self._lock.release()
        return res

    @property
    def connected(self):
        self._lock.acquire()
        res =  self._connected
        self._lock.release()
        return res
    @connected.setter
    def connected (self, connected: bool):
        self._lock.acquire()
        self._connected = connected
        if connected:
            print('[connected]')
        else:
            print('[disconnected]')
        self._lock.release()

    #
    # Methods
    #
    def Move(self, pos):
        self._lock.acquire()
        print('[Move] pos=' + str(pos) + ' cur=' + str(self._position))
        self._is_moving = True
        self._target_position = self._position + pos
        if self._target_position >= 360.0:              # Caller should protecxt against this (typ.)
            self._target_position -= 360.0
        if self._target_position < 0.0:
            self._target_position += 360.0
        print('       targetpos=' + str(self._target_position))
        self._lock.release()
        self.start()

    def MoveAbsolute(self, pos):
        self._lock.acquire()
        print('[MoveAbs] pos=' + str(pos) + ' cur=' + str(self._position))
        self._is_moving = True
        self._target_position = pos
        if self._target_position >= 360.0:
            self._target_position -= 360.0
        if self._target_position < 0.0:
            self._target_position += 360.0
        self._lock.release()
        self.start()

    def Halt(self):
        print('[Halt]')
        self.stop()
