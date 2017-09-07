import threading

import opscore.protocols.keys as keys
import opscore.protocols.types as types
from opscore.utility.qstr import qstr
import actorcore.Actor

from pysnmp.hlapi import *

import time

class SnmpThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, kwargs=None, 
            verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                verbose=verbose)
        self.kwargs = kwargs
        return

    def run(self):
        self.actor = self.kwargs['actor']
        self.cid = self.kwargs['cid']
        self.actor.logger.warn('SnmpThread start called')
        while True:
            self.actor.logger.warn('Saying something')
            self.actor.bcast.inform('text=state=abc')
            time.sleep(10)


