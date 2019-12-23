# -*- coding: utf-8 -*-
'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'TimerHandler',
)

from threading import Thread,Timer
from logging import getLogger
from time import time

from mopidy_pummeluff.actions import shutdown, play_pause, stop
from mopidy_pummeluff.sound import play_sound

LOGGER = getLogger(__name__)


class TimerHandler(Thread):
    
    shutdownTimer=None
    updateTimer=None

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param Event stop_event: The stop event
        '''
        super(TimerHandler, self).__init__()

        self.core       = core
        self.stop_event = stop_event


    # pylint: disable=no-member
    def run(self):
        '''
        Run the thread.
        '''
        ## Setup code here

        self.shutdownTimer=Timer(5400,self.shutdownTimer_callback)
        self.updateTimer=Timer(10,self.updateTimer_callback,[self])
        
        self.stop_event.wait()
        GPIO.cleanup()  # pylint: disable=no-member

    def shutdownTimer_reset(self):
        LOGGER.info('Timer reset')
        self.shutdownTimer.cancel()
        self.shutdownTimer=Timer(5400,self.shutdownTimer_callback)

    def updateTimer_callback(self):
        try:
            requests.get('http://localhost:5000/'+self.core.get_state())
        except:
            pass
    
    def shutdownTimer_callback(self):
        LOGGER.info('Timer shutdown')
        stop(self.core)
        shutdown(self.core)
