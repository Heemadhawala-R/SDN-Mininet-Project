from ryu.base import app_manager              # Provides base class to create Ryu controller applications
from ryu.controller import ofp_event          # Contains OpenFlow event definitions (e.g., switch connect, packet-in)
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls # Decorator to bind functions to specific OpenFlow events
from ryu.ofproto import ofproto_v1_3          # Specifies OpenFlow version 1.3 protocol

# Main controller class that inherits from RyuApp
class StaticRouting(app_manager.RyuApp):

    # Define OpenFlow version supported by this controller
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Function to install a flow rule into a switch
    def add_flow(self, datapath, priority, match, actions):

        ofproto = datapath.ofproto            # Reference to OpenFlow protocol (contains constants)
        parser = datapath.ofproto_parser      # Used to create OpenFlow messages (FlowMod, Match, Action)

        # Instruction tells switch what to do with matching packets
        # Here: apply the specified actions (like forwarding to a port)
        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, actions
            )
        ]

        # Create a FlowMod message (flow rule)
        flow = parser.OFPFlowMod(
            datapath=datapath,     # Target switch
            priority=priority,     # Higher value = higher priority
            match=match,           # Condition to match packets (e.g., input port)
            instructions=instructions  # Actions to perform when matched
        )

        # Send the flow rule to the switch so it can start forwarding packets accordingly
        datapath.send_msg(flow)


    # This function is automatically called when a switch connects to the controller
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath        # Represents the connected switch
        parser = datapath.ofproto_parser
        dpid = datapath.id               # Unique identifier for each switch (e.g., 1 for s1, 2 for s2)

        print(f"Switch {dpid} connected")

        # ---------------- STATIC ROUTING LOGIC ----------------
        # Here we manually define routing behavior using fixed flow rules

        if dpid == 1:
            # Rules for switch s1

            # Rule 1:
            # If a packet enters s1 from port 1 (from h1),
            # forward it to port 2 (towards s2)
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])

            # Rule 2:
            # If a packet enters s1 from port 2 (from s2),
            # forward it to port 1 (towards h1)
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

        elif dpid == 2:
            # Rules for switch s2

            # Rule 1:
            # If packet comes from port 1 (from s1),
            # forward it to port 2 (towards h2)
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])

            # Rule 2:
            # If packet comes from port 2 (from h2),
            # forward it to port 1 (towards s1)
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])


    # This function is triggered when a packet is sent from switch to controller (packet-in event)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        msg = ev.msg                     # Contains packet information
        datapath = msg.datapath          # Switch that sent the packet

        # In this project, we are not doing dynamic routing or learning
        # So we simply log that a packet reached the controller
        print(f"Packet received at switch {datapath.id}")