from settings import settings

cacheddns = {}

with open(settings['CachedDnsFile'],'r') as f:
    lines = f.readlines()
    for line in lines:
        ip , domain = line.strip().split(' ')
        ip = ip.strip()
        domain = domain.strip()
        cacheddns[domain] = ip

def local_lookup(domain):
    if domain in cacheddns.keys():
        return (True,cacheddns[domain])
    else:
        return (False,None)

