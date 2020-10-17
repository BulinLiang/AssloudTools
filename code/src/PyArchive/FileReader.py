import os
from .StreamReader import StreamReader

class FileReader(StreamReader):

    def Open(self, _filepath):
        if not os.path.isfile(_filepath):
            return

        self._size = os.path.getsize(_filepath)
        self._stream = open(_filepath, 'rb')
        self.parseHeader()
