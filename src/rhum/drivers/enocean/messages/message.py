from rhum.rhumlogging import get_logger
from rhum.utils.crc8 import CRC8Utils
from rhum.drivers.enocean.constants import PacketType

class EnOceanMessage:
    
    _logger = get_logger('rhum.drivers.enocean.EnOceanMessage')
    __syncByte = 0x55
    
    def __init__(self, msgType=0xFF, datas=None, optDatas=None):
        self.__type=msgType
        self.__datas=[]
        self.__optDatas=[]
        
        if datas != None:
            self.__datas=datas
            
        if optDatas != None:
            self.__optDatas = optDatas
            
    def build(self):
        self._logger.debug('building message')
        buffer = []
        data_length = len(self.__datas)        
        opt_length = len(self.__optDatas)
        
        #sync byte
        buffer.append(self.__syncByte) # adding sync byte
        
        #header
        buffer.append((data_length >> 8) & 0xFF) #first byte length data
        buffer.append(data_length & 0xFF) #second byte length data
        buffer.append(opt_length & 0xFF) #optionnal data length
        buffer.append(self.__type & 0xFF) #packet type byte
        #CRC Header
        buffer.append(CRC8Utils.calc(buffer[1:5]))
        
        
        #data
        buffer += self.__datas
        buffer += self.__optDatas
        
        #CRC Data
        buffer.append(CRC8Utils.calc(buffer[6:]))
        
        self._logger.debug('buffer : {0}'.format(buffer))
        
        return buffer
    
    def _get(self):
        return self.__type, self.__datas, self.__optDatas

    def __str__(self):
        msg = ''.join( [ "\\x%02X" % x for x in bytes(self.build()) ] ).strip()
        strMsg  = "\nMessage              : {0}".format(msg)
        strMsg += "\nType                 : {0}".format(PacketType(self.__type))
        strMsg += "\nData Length          : {0}".format(len(self.__datas))
        strMsg += "\nOpt Length           : {0}".format(len(self.__optDatas))
        return strMsg