
import sys, os, time
from signal import signal, SIGINT
from sys import exit
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/libs")
from mgr import *
from pal_rpc.ttypes import * # pal_port_speed_t, pal_fec_type_t

PROGRAM_NAME="prog"
m = Manager(PROGRAM_NAME)
# m.add_multinode_mc_group(1066, [(196, 1)])

def main():
    signal(SIGINT, handler)
    print ("controller running (idle) -- press ctrl+c to exit")
    example_port_up()
    example_table_add()
    while True:
        time.sleep(1)

def example_port_up():
    # bring up port with dpid 128 at 100G.
    # constants are defined in pal_rpc.ttypes
    m.port_up(128, pal_port_speed_t.BF_SPEED_10G, pal_fec_type_t.BF_FEC_TYP_NONE)    

def example_table_add():
    m.addExactEntry("tiWire", ["ig_intr_md.ingress_port"], [128], "aiOut", {"out_port":128})


def handler(signal_received, frame):
    # Handle any cleanup here
    print('Exiting..')
    m.disconnect()
    exit(0)

if __name__ == '__main__':
    main()
