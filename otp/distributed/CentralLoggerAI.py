from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class CentralLoggerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CentralLoggerAI")

    def sendMessage(self, msg, evt, b1 , b2):
        print(msg)
        print(evt)
        print(b1)
        print(b2)

    def logAIGarbage(self):
        pass