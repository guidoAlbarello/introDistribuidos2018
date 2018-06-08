from mininet.topo import Topo


class LinearTopo(Topo):
	def __init__(self, num_switches=3):
		Topo.__init__(self)
		switches = self.create_switches(num_switches)
		hosts = self.create_hosts()
		self.create_links(switches, hosts)


	def create_switches(self,num_switches):
		switches = []
		for i in range(num_switches):
			switches.append(self.addSwitch('s%s' % (i)))

		return switches

	def create_hosts(self):
		hosts = []
		for i in range(4):
			hosts.append(self.addHost('h%s' %  (i)))

		return hosts

	def create_links(self, switches, hosts):
		for i in range(len(switches)-1):
			self.addLink(switches[i],switches[i+1])
		self.addLink(hosts[0],switches[0])
		self.addLink(hosts[1],switches[0])
		self.addLink(hosts[2],switches[len(switches)-1])
		self.addLink(hosts[3],switches[len(switches)-1])

topos= {'linear': LinearTopo}
