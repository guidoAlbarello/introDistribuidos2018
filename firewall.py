

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

''' Add your global variables here ... '''

log = core.getLogger()


class Firewall(EventMixin):

    def __init__(self):
        # self.log = core.getLogger("firewall")
        self.listenTo(core.openflow)
        log.info("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        ''' Add your logic here ... '''
        log.info("ConnectionUp event received")

    # def _handle_PacketIn(self, event):
    #     tcpp = event.parsed.find('tcp')
    #     if not tcpp : return
    #     if tcpp.srcport == 80 or tcpp.dstport == 80:
    #         event.halt = True
    #         log.info("Packet Blocked")

    # def _handle_PacketIn(self, event):
    #     udpp = event.parsed.find('udp')
    #     if not udpp : return
    #     if ((udpp.dstport == 5001) and  (str(mac) == "00:00:00:00:00:02")):
    #         event.halt = True
    #         log.info("Packet Blocked")

    def _handle_PacketIn(self, event):
        tcpp = event.parsed.find('ipv4')
        if not tcpp : return
        a = "10.0.0.2"
        b = "10.0.0.3"
        src = str(tcpp.srcip)
        dst = str(tcpp.dstip)
        if (src == a and dst == b ) or (src == b and dst == a):
            event.halt = True
            log.info("Packet Blocked")

def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
