import socket
import struct
from time import time, strftime
from message import Header, Question
from localdns import local_lookup
from settings import settings 
import _thread

r_rd = int().from_bytes(b'\x01\x00',byteorder='big',signed=False)

#check_q_r = 32768

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_address = ('localhost', settings['LocalServerPort'])
sock.bind(server_address)

def response(data,address,timeout=2.0):
    errlog = open("error.log","a")
    errmsgs = []
    rr = b''
    succ = False
    header = Header(data)
    question = Question(data)
    domain = question.get_domain()
    print('recieved request for domain {} , id {}'.format(domain,header.t_id))
    qtype = int().from_bytes(question.qtype,byteorder='big', signed=False)
    qcount = int().from_bytes(header.qdcount,byteorder='big', signed=False)
    qclass = int().from_bytes(question.qclass,byteorder='big', signed=False)
    flag,ip = local_lookup(domain)
    if(flag==1):
        if(ip=="0.0.0.0"):
            print("request domain {} , id {} , status:intercepted".format(domain,header.t_id))
        else:
            print("request domain {} , id {} , status:local".format(domain,header.t_id))
    else:
        print("request domain {} , id {} , status:resolve".format(domain,header.t_id))
    if qtype == 1 and qcount == 1 and qclass == 1 and flag == 1:
        ip0,ip1,ip2,ip3 = ip.split('.')
        r_ip = struct.pack('!BBBB',int(ip0),int(ip1),int(ip2),int(ip3))
        r_header = header.id+header.rflags()+header.qdcount+b'\x00\x01'+b'\x00\x00'+b'\x00\x00'
        r_response = question.qname + question.qtype + question.qclass + b'\x00\x00\xFF\xFF' + b'\x00\x04' + r_ip
        rr = r_header + question.content + r_response
        succ = True

    else:
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        remote_servers = settings['RemoteDnsServer']
        for server in remote_servers:
            remote_server_addr = (server,53)
            try:
                sock_client.settimeout(timeout)
                sock_client.sendto(data,remote_server_addr)
                start = time()
                while time() - start < timeout:
                    sock_client.settimeout(timeout)
                    temp,addr = sock_client.recvfrom(512)
                    check_header = Header(temp)
                    is_response = check_header.is_response
                    #is_response = int().from_bytes(check_header.flag[0:2],byteorder='big',signed=False) & check_q_r
                    if check_header.t_id == header.t_id and is_response > 0:
                        rr = temp
                        succ = True
                        break
                break
            except Exception as e:
                e_time = strftime("[%Y-%m-%d,%H:%M:%S]")
                errmsg = '{} error occured when sending query to remote dns server {}:{}'.format(e_time,remote_server_addr,str(e))
                errmsgs.append(errmsg)
                continue
        sock_client.close()
        
    if succ:
        sock.sendto(rr,address)       
    else:
        for emsg in errmsgs:
            errlog.write(emsg)
        print('error occured when processing domain {} , id {} , please check error.log'.format(domain,header.t_id))
    errlog.close()
    return (succ,rr,address)

def main():
    
    print('starting up on {} port {}'.format(*server_address))
    print('waiting for DNS query')

    while True:
        try:
            query,address = sock.recvfrom(512)
            head = Header(query)
            #is_response = int().from_bytes(head.flag[0:2],byteorder='big',signed=False) & check_q_r
            is_response = head.is_response
            if not is_response:
                argvs = (query,address)
                _thread.start_new_thread(response,argvs)
        except Exception as e:
            continue

if __name__=='__main__':
    main()
