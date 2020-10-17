import os
from .Entry import Entry
from .Writer import Writer

class StreamWriter(Writer):
    """
    Attributes:
        
    """
    def __init__(self):
        self._entryMap = {}
        self._stream = None
        self._offset = 0
        self._size = 0
        self._flag = 0

    def HasPath(self, _path):
        return _path in self.__entryMap

    def Write(self, _path, _data):
        """ 写入数据
        Args:
            _path: 路径
            _data: 字节数据

        """
        if None == self._stream:
            return

        if _path in self._entryMap:
            return

        entry = Entry()
        # 实体的偏移值为当前的缓存偏移值
        entry.offset = self._offset
        # 实体的大小为数据的大小
        entry.size = len(_data)
        # 在缓存的尾部追加数据
        self.writeBytes(_data)
        # 在实体表中保存此实体
        self._entryMap[_path] = entry


    def Close(self):
        """ 

        """
        if None == self._stream:
            return 
        
        # 在缓存尾部写入映射表数据
        vTableOffset = self._offset
        # 写入实体数量
        self.writeInt32(len(self._entryMap))
        for path in self._entryMap.keys():
            pathBytes = self.stringToBytes(path)
            # 写入实体路径长度
            self.writeInt32(len(pathBytes))
            # 写入实体路径
            self.writeBytes(pathBytes)
            # 写入实体的偏移值
            self.writeInt64(self._entryMap[path].offset)
            # 写入实体的尺寸
            self.writeInt64(self._entryMap[path].size)

        # 映射表的大小等于缓存的尺寸减去映射表的偏移值
        vTableSize = self._offset - vTableOffset
        # 重置缓存写入指针到最前端
        self._stream.seek(0)
        # 覆盖写入文件的尺寸
        self.writeInt64(self._offset)
        # 覆盖写入标识
        self.writeInt64(self._flag)
        # 覆盖写入映射表的偏移
        self.writeInt64(vTableOffset)
        # 覆盖写入映射表的尺寸
        self.writeInt64(vTableSize)
        self._stream.close()
        self._fileStram = None

    def writeInt32(self, _value):
        """ 写入32位整型值
        Args:
            _value: 32位整型
        """
        buffer = self.int32ToBytes(_value)
        self._stream.write(buffer)
        self._offset += len(buffer)

    def writeInt64(self, _value):
        """ 写入64位整型值
        Args:
            _value: 64位整型
        """
        buffer = self.int64ToBytes(_value)
        self._stream.write(buffer)
        self._offset += len(buffer)

    def writeBytes(self, _value):
        """ 写入字节数组值
        Args:
            _value: 字节数组
        """
        self._stream.write(_value)
        self._offset += len(_value)




