from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

log = core.getLogger()

class Firewall ( EventMixin ):
	def __init__(self):
		self.listenTo(core . openflow)
		log.debug("Enabling Firewall Module")

	def _handle_PacketIn (self, event):
		print "llego"
		if (event.port ==  80):
			log.debug( "Noooope"

	
	def launch ():
		core.openflow.addListcketIn", _handle_PacketIn)
		core.registerNew(Firewall)
		
