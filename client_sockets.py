import cProfile
import socket
import time

class FakeFile(object):
    size = 6727253778
    position = 0
    zero_string = "0"*8096*1024
    def get_size(self):
        return self.size

    def read(self, blocksize):
        if self.position == self.size:
            return ""
        if self.position + blocksize > self.size:
            print "END OF FILE"
            length = self.size - self.position
            self.position = self.size
            return "0"*length
        self.position += blocksize
        return self.zero_string

    def tell(self):
        return self.position

    def reset(self):
        self.position = 0


def test():
    host = "localhost"
    boundary = "9afb0c26-7adf-11e0-b167-1c6f65955350"

    filen = "6GB.bin"

    CRLF = '\r\n'

    bl =[]
    bl.append('--' + boundary)
    bl.append('Content-Disposition: form-data; name="fname"')
    bl.append('')
    bl.append("Raja")
    bl.append('--' + boundary)
    #bl.append('Content-Disposition: form-data; name="uploadedfile"; filename="%s"' % (str(os.path.basename(filen))))
    bl.append('Content-Disposition: form-data; name="uploadedfile"; filename="%s"' % (filen))
    bl.append('Content-Type: %s' % (str('application/octet-stream')))
    bl.append('')

    body = CRLF.join(bl)

    hl =[]
    hl.append('POST / HTTP/1.1')
    hl.append('HOST: %s' % host)
    hl.append('Content-Type: multipart/form-data; boundary=%s' % boundary)
    #fsize = os.path.getsize(filen)
    fsize = fake_file.get_size()
    size = int(fsize)
    #print int(fsize)
    hl.append('Content-Length: %s' % str(len(body)+int(fsize)+len('--' + boundary + '--\r\n'+'\r\n')))
    hl.append('\r\n')

    print "Initializing.."

    headers = CRLF.join(hl)
    #print str(headers)+str(body)
    #return

    socks = serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.connect((host, 80))

    serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    serv.send(str(headers)+str(body))
    #fileh = open(filen, 'rb')
    fileh = fake_file

    #print "Upload loop"
    while 1:
        chunck = fileh.read(8096*1024)
        #print "Uploading..."
        if len(chunck) == 0:
            socks.send('\r\n--' + boundary + '--\r\n')
            socks.send('\r\n')
            response = socks.recv(1024)
            #print response
            if str(response).find('200 OK') == -1:
                return "Error"
            else:
                #print "Done"
                socks.close()
                fileh.close()
                return "Done"
        else:
            try:
                socks.send(chunck)
            except:
                return



fake_file = FakeFile()


#while True:
start_time = time.clock()
#test()
cProfile.runctx('test()',globals(),locals())
fake_file.reset()
print "speed (MiB/s): ", (6260)/(time.clock() - start_time)

