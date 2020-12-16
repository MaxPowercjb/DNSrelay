import struct

r_flags = int().from_bytes(b'\x81\x00',byteorder='big',signed=False)
r_qr = int().from_bytes(b'\x80\x00',byteorder='big',signed=False)

class Header(object):
    def __init__(self,msg):
        self.content = msg[:12]
        (self.t_id,self.t_flag,self.t_qdcount,self.t_ancount,self.t_nscount,self.t_arcount)\
        =  struct.unpack("!HHHHHH",self.content)
        self.id = msg[:2]
        self.flag = msg[2:4]
        self.qdcount = msg[4:6]
        self.ancount = msg[6:8]
        self.nscount = msg[8:10]
        self.arcount = msg[10:12]
        self.is_response = int().from_bytes(self.flag[0:2],byteorder='big',signed=False) & 32768

    def rflags(self):
        rflag = (self.t_flag & r_flags) | r_qr
        rflag = struct.pack('!H',rflag)
        return rflag

class Question(object):
    def __init__(self,query):
        self.length = len(query) - 12
        self.content = query[12:self.length+12]
        self.qname = self.content[:self.length-4]
        self.qtype = self.content[self.length-4:self.length-2]
        self.qclass = self.content[self.length-2:self.length]

    def get_domain(self):
        domain = []
        length = len(self.qname)
        i = 0
        while i < length:
            n_lenth = struct.unpack('!B',self.qname[i:i+1])[0]
            if n_lenth > 0:
                name = struct.unpack('!{}s'.format(n_lenth),self.qname[i+1:i+n_lenth+1])[0]
                name = name.decode()
                i += (n_lenth+1)
                domain.append(name)
            else:
                break
        domain_name = '.'.join(domain)
        return domain_name

    





