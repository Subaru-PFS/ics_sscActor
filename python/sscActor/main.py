#!/usr/bin/env python

import actorcore.Actor
import sscActor.Commands.SnmpThread as SnmpThread
import threading

class OurActor(actorcore.Actor.Actor):
    def __init__(self, name,
                 productName=None, configFile=None,
                 modelNames=(),
                 debugLevel=30):

        actorcore.Actor.Actor.__init__(self, name, 
                                       productName=productName, 
                                       configFile=configFile,
                                       modelNames=modelNames)
        self.everConnected = False

    def connectionMade(self):
        if self.everConnected is False:
            self.logger.info("Connected to tron, starting threads")
            self.snmpth = SnmpThread.SnmpThread(
                kwargs = {'actor': self, 'cid': 1})
            self.snmpth.start()
            self.logger.warn('Started threading')
            self.everConnected = True


def main():
    theActor = OurActor('ssc', productName='sscActor')
    theActor.run()

if __name__ == '__main__':
    main()
