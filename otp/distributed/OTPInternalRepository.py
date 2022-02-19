from direct.directnotify import DirectNotifyGlobal
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.PyDatagram import *


# TODO: Remove Astron dependence.

class OTPInternalRepository(AstronInternalRepository):
    notify = DirectNotifyGlobal.directNotify.newCategory('OTPInternalRepository')
    dbId = 4003

    def __init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet):
        AstronInternalRepository.__init__(self, baseChannel, serverId=serverId, dcFileNames=dcFileNames,
                                          dcSuffix=dcSuffix, connectMethod=connectMethod, threadedNet=threadedNet)

    def handleConnected(self):
        AstronInternalRepository.handleConnected(self)

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def sendSetZone(self, distObj, zoneId):
        distObj.setLocation(distObj.parentId, zoneId)
        self.sendSetLocation(distObj, distObj.parentId, zoneId)

    def setAllowClientSend(self, avId, distObj, fieldNameList=[]):
        dg = PyDatagram()
        dg.addServerHeader(distObj.GetPuppetConnectionChannel(avId), self.ourChannel, CLIENTAGENT_SET_FIELDS_SENDABLE)
        fieldIds = []
        for fieldName in fieldNameList:
            field = distObj.dclass.getFieldByName(fieldName)
            if field:
                fieldIds.append(field.getNumber())

        dg.addUint32(distObj.getDoId())
        dg.addUint16(len(fieldIds))
        for fieldId in fieldIds:
            dg.addUint16(fieldId)

        self.send(dg)

    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
        except SystemExit as KeyboardInterrupt:
            raise
        except Exception as e:
            if self.getAvatarIdFromSender() > 100000000:
                dg = PyDatagram()
                dg.addServerHeader(self.getMsgSender(), self.ourChannel, CLIENTAGENT_EJECT)
                dg.addUint16(166)
                dg.addString('You were disconnected to prevent a district reset.')
                self.send(dg)
            self.writeServerEvent('INTERNAL-EXCEPTION', self,getAvatarIdFromSender(), self.getAccountIdFromSender, repr(e), traceback.format_exc())
            self.notify.warning('INTERNAL-EXCEPTION: {0} ({1})'.format(repr(e), self.getAvatarIdFromSender))
            print(traceback.format_exc)
            sys.exc_clear()
        return 1