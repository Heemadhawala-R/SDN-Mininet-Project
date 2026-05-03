from mininet.topo import Topo   # Import Topo class to create custom network topology

# Define custom topology class
class StaticRoutingTopo(Topo):

    # build() method is automatically called by Mininet to create the network
    def build(self):

        # -------- ADD HOSTS --------
        # Create two end devices (hosts)
        h1 = self.addHost('h1')   # Host 1 (acts as sender)
        h2 = self.addHost('h2')   # Host 2 (acts as receiver)

        # -------- ADD SWITCHES --------
        # Create two switches which will forward packets
        s1 = self.addSwitch('s1')  # First switch
        s2 = self.addSwitch('s2')  # Second switch

        # -------- CREATE LINKS --------
        # Connect hosts and switches to form network

        self.addLink(h1, s1)   # Link between h1 and s1
        self.addLink(s1, s2)   # Link between s1 and s2
        self.addLink(s2, h2)   # Link between s2 and h2

        # Final topology:
        # h1 ---- s1 ---- s2 ---- h2


# Register topology so Mininet can use it via command line
topos = {'staticroutingtopo': StaticRoutingTopo}