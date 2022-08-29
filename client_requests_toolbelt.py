import os
from requests_toolbelt import MultipartEncoder
import requests
import time
import cProfile

url = "http://localhost/upload"
files = {"file" : open("6GB.bin", "rb")}
#r = requests.post(url, files=files)

print os.getpid()

class CustomEncoder(MultipartEncoder):
    def read(self, size=None):
        size=8*1024*1024 # modify this in httplib of your python installation
        if size is not None:
            size = int(size) # Ensure it is always an integer
            bytes_length = len(self._buffer) # Calculate this once

            size -= bytes_length if size > bytes_length else 0

        self._load_bytes(size)

        return self._buffer.read(size)

def test():
    m = MultipartEncoder(fields={'file': ("testfile.bin", open("6GB.bin", 'rb'), 'application/octet-stream')})
    start_time = time.clock()
    requests.post(url, data=m, headers={'Content-Type': m.content_type})
    print "speed (MiB/s): ", 6260/(time.clock() - start_time)

while True:
    test()
