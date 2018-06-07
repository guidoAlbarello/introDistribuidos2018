#!/usr/bin/env python

from mininet.topo import Topo


class CustomTopo(Topo):
    def __init__(self, num_levels=1, num_hosts=2):
        Topo.__init__(self)
        switches_layers = self.create_switches_layers(num_levels)
        hosts = self.create_hosts(num_hosts)
        self.create_links_between_switches_and_hosts(switches_layers, hosts)
        self.create_links_between_switches(switches_layers)

    def create_switches_layers(self, num_levels):
        num_layers = 2 * num_levels - 1
        layers = []
        for i in range(num_layers):
            layers.append([])
            num_nodes = self.get_number_of_nodes_for_layer(i, num_layers)
            for j in range(num_nodes):
                switch = self.addSwitch('s%s-%s' % (i, j))
                layers[i].append(switch)
        return layers

    def get_number_of_nodes_for_layer(self, n, num_layers):
        if n <= int(num_layers / 2):
            coef = n
        else:
            coef = num_layers - 1 - n
        num_nodes = 2 ** coef
        return num_nodes

    def create_hosts(self, num_hosts):
        host_number = 0
        hosts = []
        for i in range(num_hosts):
            host_number += 1
            hosts.append(self.addHost('h%s' % host_number))
        return hosts

    def create_links_between_switches_and_hosts(self, switches_layers, hosts):
        num_hosts = len(hosts)
        num_switches = len(switches_layers)
        left_switch = switches_layers[0][0]
        right_switch = switches_layers[num_switches - 1][0]

        for i in range(num_hosts):
            if i < num_hosts / 2:
                self.addLink(left_switch, hosts[i])
            else:
                self.addLink(right_switch, hosts[i])

    def create_links_between_switches(self, switches_layers):
        num_layers = len(switches_layers)
        for i in range(num_layers - 1):
            layer = switches_layers[i]
            next_layer = switches_layers[i + 1]
            num_nodes = len(layer)
            for j in range(num_nodes):
                node = layer[j]
                if i < int(num_layers / 2):
                    self.addLink(node, next_layer[2 * j])
                    self.addLink(node, next_layer[2 * j + 1])
                else:
                    self.addLink(node, next_layer[int(j / 2)])


topos = {'custom': CustomTopo}