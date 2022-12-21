# =================================================================
# ROTATORDEVICE.PY - Poor-man's simulaton of a Rotator
# =================================================================
# This is only for demo purposes. It's extremely fragile, and should
# not be used as an example of a real device. Settings not remembered.
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Type hints 
# 19-Dec-2022   rbd 0.1 Add logic for IRotatorV3 offsets
#
from threading import Timer
from threading import Lock

# TODO Move connected checks here and raise RuntimeExeption 
# TODO Change commented-out diagnostics to use f-strings

class RotatorDevice(object):
    """Implements a rotator device that runs in a separate thread"""
    #
    # Only override __init_()  and run() (pydoc 17.1.2)
    #
    def __init__(self):
        self._lock = Lock()
        self.name: str = 'device'
        #
        # Rotator device constants
        #
        self._can_reverse: bool = True
        self._step_size: float = 1.0
        self._steps_per_sec: int = 6
        #
        # Rotator device state variables
        #
        self._reverse = False
        self._mech_pos = 0.0
        self._tgt_mech_pos = 0.0
        self._pos_offset = 0.0      # TODO In real life this must be persisted
        self._is_moving = False
        self._connected = False
        #
        # Rotator engine
        #
        self._timer: Timer = None
        self._interval: float = 1.0 / self._steps_per_sec
        self._stopped: bool = True

    def _pos_to_mech(self, pos: float) -> float:
        mech = pos - self._pos_offset
        if mech >= 360.0:
            mech -= 360.0
        if mech < 0.0:
            mech += 360.0
        return mech
    
    def _mech_to_pos(self, mech: float) -> float:
        pos = mech + self._pos_offset
        if pos >= 360.0:
            pos -= 360.0
        if pos < 0.0:
            pos += 360.0
        return pos

    def start(self, from_run: bool = False) -> None:
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


    def _run(self) -> None:
        #print('[_run] (tmr expired) get lock')
        self._lock.acquire()
        #print(f'[_run] got lock : tgtmech={str(self._tgt_mech_pos)} mech={str(self._mech_pos)}')
        delta = self._tgt_mech_pos - self._mech_pos
        if delta < -180.0:
           delta += 360.0
        if delta >= 180.0:
           delta -= 360.0
        #print(f'[_run] final delta={str(delta)}')
        if abs(delta) > (self._step_size / 2.0):
            self._is_moving = True
            if delta > 0:
                #print('[_run] delta > 0 go positive')
                self._mech_pos += self._step_size
                if self._mech_pos >= 360.0:
                    self._mech_pos -= 360.0
            else:
                #print('[_run] delta < 0 go negative')
                self._mech_pos -= self._step_size
                if self._mech_pos < 0.0:
                    self._mech_pos += 360.0
            #print(f'[_run] new pos = {str(self._mech_to_pos(self._mech_pos))}')
        else:
            self._is_moving = False
            self._stopped = True
        self._lock.release()
        #print('[_run] lock released')
        if self._is_moving:
            #print('[_run] more motion needed, start another timer interval')
            self.start(from_run = True)

    def stop(self) -> None:
        self._lock.acquire()
        #print('[stop] Stopping...')
        self._stopped = True
        self._is_moving = False
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None
        self._lock.release()

    #
    # Guarded properties
    #
    @property
    def can_reverse(self) -> bool:
        self._lock.acquire()
        res =  self._can_reverse 
        self._lock.release()
        return res

    @property
    def reverse(self) -> bool:
        self._lock.acquire()
        res =  self._reverse
        self._lock.release()
        return res
    @reverse.setter
    def reverse (self, reverse: bool):
        self._lock.acquire()
        self._reverse = reverse
        self._lock.release()

    @property
    def step_size(self) -> float:
        self._lock.acquire()
        res =  self._step_size
        self._lock.release()
        return res
    @step_size.setter
    def step_size (self, step_size: float):
        self._lock.acquire()
        self._step_size = step_size
        self._lock.release()

    @property
    def steps_per_sec(self) -> int:
        self._lock.acquire()
        res =  self._steps_per_sec
        self._lock.release()
        return res
    @steps_per_sec.setter
    def steps_per_sec (self, steps_per_sec: int):
        self._lock.acquire()
        self._steps_per_sec = steps_per_sec
        self._lock.release()

    @property
    def position(self) -> float:
        self._lock.acquire()
        res = self._mech_to_pos(self._mech_pos)
        #print('[position] ' + str(res))
        self._lock.release()
        return res

    @property
    def mechanical_position(self) -> float:
        self._lock.acquire()
        res = self._mech_pos
        #print('[mech position] ' + str(res))
        self._lock.release()
        return res

    @property
    def target_position(self) -> float:
        self._lock.acquire()
        res =  self._mech_to_pos(self._tgt_mech_pos)
        #print('[target_position] ' + str(res))
        self._lock.release()
        return res

    @property
    def is_moving(self) -> bool:
        self._lock.acquire()
        res =  self._is_moving
        #print('[is_moving] ' + str(res))
        self._lock.release()
        return res

    @property
    def connected(self) -> bool:
        self._lock.acquire()
        res = self._connected
        self._lock.release()
        return res
    @connected.setter
    def connected (self, connected: bool):
        self._lock.acquire()
        if (not connected) and self._connected and self._is_moving:
            # Yes you could call Halt() but this is for illustration
            raise RuntimeError('Cannot disconnect while rotator is moving')
        self._connected = connected
        # if connected:
        #     print('[connected]')
        # else:
        #     print('[disconnected]')
        self._lock.release()

    #
    # Methods
    # TODO - This is supposed to throw if the final position is outside 0-360, but WHICH position? Mech or user????
    #
    def Move(self, delta_pos: float) -> None:
        self._lock.acquire()
        if self._is_moving:
            self._lock.release()
            raise RuntimeError('Cannot start a move while the rotator is moving')
        #print(f'[Move] pos={str(delta_pos)}')
        self._is_moving = True
        self._tgt_mech_pos = self._mech_pos + delta_pos - self._pos_offset
        if self._tgt_mech_pos >= 360.0:
            self._tgt_mech_pos -= 360.0
        if self._tgt_mech_pos < 0.0:
            self._tgt_mech_pos += 360.0
        #print(f'       targetpos={self._mech_to_pos(self._tgt_mech_pos)}')
        self._lock.release()
        self.start()

    def MoveAbsolute(self, pos: float) -> None:
        self._lock.acquire()
        if self._is_moving:
            self._lock.release()
            raise RuntimeError('Cannot start a move while the rotator is moving')
        #print(f'[MoveAbs] pos={str(pos)}')
        self._is_moving = True
        self._tgt_mech_pos = self._pos_to_mech(pos)
        self._lock.release()
        self.start()

    def MoveMechanical(self, pos: float) -> None:
        self._lock.acquire()
        if self._is_moving:
            self._lock.release()
            raise RuntimeError('Cannot start a move while the rotator is moving')
        #print(f'[MoveMech] pos={str(pos)}')
        self._is_moving = True
        self._tgt_mech_pos = pos
        self._lock.release()
        self.start()

    def Sync(self, pos: float) -> None:
        self._lock.acquire()
        if self._is_moving:
            self._lock.release()
            raise RuntimeError('Cannot sync while rotator is moving')
        self._pos_offset = pos - self._mech_pos
        if self._pos_offset < -180.0:
           self._pos_offset += 360.0
        if self._pos_offset >= 180.0:
           self._pos_offset -= 360.0
        self._lock.release()

    def Halt(self) -> None:
        #print('[Halt]')
        self.stop()
