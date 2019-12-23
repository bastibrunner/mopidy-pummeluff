# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff frontend.
'''

from __future__ import absolute_import, unicode_literals, print_function
import requests

__all__ = (
    'PummeluffFrontend',
)

from threading import Event
from logging import getLogger

import pykka
from mopidy import core as mopidy_core

from .threads import GPIOHandler, TagReader, TimerHandler

import mopidy_pummeluff.sound


LOGGER = getLogger(__name__)


class PummeluffFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    '''
    Pummeluff frontend which basically reacts to GPIO button pushes and touches
    of RFID tags.
    '''

    def __init__(self, config, core):  # pylint: disable=unused-argument
        super(PummeluffFrontend, self).__init__()
        self.core         = core
        self.stop_event   = Event()
        self.gpio_handler = GPIOHandler(core=core, stop_event=self.stop_event)
        self.tag_reader   = TagReader(core=core, stop_event=self.stop_event)
        self.timer_handler = TimerHandler(core=core, stop_event=self.stop_event)
        if (config['audio']['output'].split(" ")[2] == alsasink):
            sound.alsadevice = "-D "+config['audio']['output'].split(" ")[1]

    def on_start(self):
        '''
        Start GPIO handler & tag reader threads.
        '''
        self.gpio_handler.start()
        self.tag_reader.start()
        self.timer_handler.start()
        try:
            requests.get('http://localhost:5000/on_start')
        except:
            pass

    def on_stop(self):
        '''
        Set threading stop event to tell GPIO handler & tag reader threads to
        stop their operations.
        '''
        self.stop_event.set()


    def tracklist_changed(self):
        self.timer_handler.shutdownTimer_reset()
        try:
            requests.get('http://localhost:5000/playlist_changed')
        except:
            pass

    def playback_state_changed(self, old_state, new_state):
        self.timer_handler.shutdownTimer_reset()
        try:
            requests.get('http://localhost:5000/'+new_state)
        except:
            pass
