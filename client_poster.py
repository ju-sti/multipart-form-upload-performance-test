import cProfile
import os
import tempfile
import time

# test_client.py
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2


print tempfile.gettempdir()

# Register the streaming http handlers with urllib2
register_openers()

# Start the multipart/form-data encoding of the file "DSC0001.jpg"
# "image1" is the name of the parameter, which is normally set
# via the "name" parameter of the HTML <input> tag.

# headers contains the necessary Content-Type and Content-Length
# datagen is a generator object that yields the encoded parameters

print os.getpid()
#while True:
def test():
    start_time = time.clock()
    datagen, headers = multipart_encode(
        {"file": open("6GB.bin", "rb")})

    # Create the Request object
    request = urllib2.Request("http://localhost/upload", datagen, headers)
    # Actually do the request, and get the response
    try:
        print urllib2.urlopen(request).read()
    except Exception:
        pass

    print "speed (MiB/s): ", 6260/(time.clock() - start_time)

cProfile.runctx('test()',globals(),locals())
#while True:
#    test()