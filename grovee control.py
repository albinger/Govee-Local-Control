import socket
import struct
import json

MCAST_GRP = '239.255.255.250'
MCAST_SPORT = 4001

MESSAGE = {"msg":{"cmd":"scan","data":{"account_topic":"reserve"}}}
MESSAGE = json.dumps(MESSAGE)

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ssock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

# For Python 3, change next line to 'sock.sendto(b"robot", ...' to avoid the
# "bytes-like object is required" msg (https://stackoverflow.com/a/42612820)
ssock.sendto(bytes(MESSAGE,'utf-8'), (MCAST_GRP, MCAST_SPORT))




MCAST_LPORT = 4002
IS_ALL_GROUPS = True

lsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    lsock.bind(('', MCAST_LPORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    lsock.bind((MCAST_GRP, MCAST_LPORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

lsock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  # For Python 3, change next line to "print(sock.recv(10240))"
  print (lsock.recv(10240))
