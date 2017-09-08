import threading

import opscore.protocols.keys as keys
import opscore.protocols.types as types
from opscore.utility.qstr import qstr
import actorcore.Actor

from pysnmp.hlapi import *

import time

SNMP_DEF_PORT = 161
SNMP_DEF_PUBLIC = 'public'

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
        snmp_target = self.actor.config.get(self.actor.name, 'snmp_target')
        snmp_oid = self.actor.config.get(self.actor.name, 'snmp_oid')
        while True:
            self.actor.logger.warn('Saying something')
            val = self._GetSnmpValue(snmp_target, snmp_oid)
            if val is not None:
                self.actor.bcast.inform('involt=%d' % (val))
            else:
                self.actor.bcast.warn('involt=UNKNOWN')
            time.sleep(10)


    ''' Starting SNMP wrapper methods '''
    def _GetSnmpValue(self, ip_addr, oid):
        for (errIndic, errStat, errIndx, binds) in getCmd(
            SnmpEngine(), CommunityData(SNMP_DEF_PUBLIC),
            UdpTransportTarget((ip_addr, SNMP_DEF_PORT)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))):
            if errIndic:
                return None
            elif errStat:
                return None
            else:
                return binds[0][1]

