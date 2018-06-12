

'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application
Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

''' Add your imports here ... '''
from pox.lib.util import dpid_to_str
from pox.lib.revent import *
''' Add your global variables here ... '''

log = core.getLogger()

class ConnectionUp(Event):
    def __init__(self,connection,ofp):
        Event.__init__(self)
        self.connection = connection
        self.dpid = connection.dpid
        self.ofp = ofp
class ConnectionDown(Event):
    def __init__(self,connection,ofp):
        Event.__init__(self)
        self.connection = connection
        self.dpid = connection.dpid

class Firewall(EventMixin):

    def __init__(self):
        # self.log = core.getLogger("firewall")
        self.listenTo(core.openflow)
        log.info("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        ConnectionUp(event.connection, event.ofp)
        log.info("Switch %s has come up.", dpid_to_str(event.dpid))

    def _handle_ConnectionDown(self, event):
        ConnectionDown(event.connection, event.dpid)
        log.info("Switch %s has shutdown.", dpid_to_str(event.dpid))

    def block_protocol_port(self, event):
        protocol = 'tcp'
        port = 80
        tcpp = event.parsed.find(protocol)
        if not tcpp : return
        if tcpp.srcport == port or tcpp.dstport == port:
            event.halt = True
            log.info("Packet Blocked by Block Protocol " + protocol + " and port " + str(port))

    def block_mac_protocol_and_port(self, event):
        protocol = 'udp'
        port = 5001
        blocked_mac = "00:00:00:00:00:02"
        udpp = event.parsed.find('udp')
        if not udpp : return
        mac = event.parsed.src
        if ((udpp.dstport == 5001) and  (str(mac) == blocked_mac)):
            event.halt = True
            log.info("Packet Blocked by Block Src Mac: " + blocked_mac+ " protocol: " + protocol + " and port: " + str(port))

    def _handle_PacketIn(self, event):

        self.block_protocol_port(event)
        self.block_communication_between_two_hosts(event)
        self.block_mac_protocol_and_port(event)

    def block_communication_between_two_hosts(self, event):
        tcpp = event.parsed.find('ipv4')
        if not tcpp: return
        a = "10.0.0.2"
        b = "10.0.0.3"
        src = str(tcpp.srcip)
        dst = str(tcpp.dstip)
        if ( (src == a or src == b) and (dst == b or dst == a) ):
            event.halt = True
            log.info("Evento capturado en SWITCH: " + dpid_to_str(event.dpid))
            log.info("Packet Blocked by Block communication between two hosts. with ips: " + a + " and " + b)

def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
