# tofino_p4_simple_example

This is a simple P4 program for the Tofino meant as a "hello world" type example. This readme has basic instructions for compiling and running it. 


### Contents
prog.p4 -- a p4 program that selects an output port for each packet based on its input port. By default, the program reflects the packet out of the same port that it came in on. 
prog.py -- a python control script that uses grpc and thrift to configure the switch. Runs on the switch cpu. 

### Setup

1. Install the SDE. You can use the configuration file in tofino_8_19_20.yaml. Put ``tofino_8_19_20.yaml`` into ``p4studio_build/profiles`` and run: 

```
./p4studio_build.py -up profiles/tofino_8_19_20.yaml 
``` 

**Note: This was tested with SDE 9.2.0, but should be the same up to 9.5.1. I am not sure after that.**

2. Set the $SDE and $SDE_INSTALL variables in your p4-studio SDE installation.

3. Make sure that the tofino driver kernel module is loaded. 

```
jsonch@localhost:~$ lsmod | grep bf_kpkt
bf_kpkt             16338944  0
```
If you don't see any output, run this command to load the kernel module: 

```
sudo $SDE/install/bin/bf_kpkt_mod_load $SDE/install
```

### Usage

1. **compiling the p4**

run ``$SDE/p4-build.sh prog.p4`` to compile the program to $SDE/build/p4-build/prog.

```
jsonch@localhost:~/projects/reflector$ $SDE/p4_build.sh prog.p4
Using SDE /home/jsonch/bf_sde/bf-sde-9.2.0
Using SDE_INSTALL /home/jsonch/bf_sde/bf-sde-9.2.0/install
Your PATH contains $SDE_INSTALL/bin. Good
Found bf-sde-9.2.0 in $SDE
OS Name:  "Open Network Linux OS ONL-HEAD, 2020-03-16.19
This system has 8GB of RAM and 8 CPU(s)
Parallelization:  Recommended: -j4   Actual: -j4
Compiling for p4_16/tna
P4 compiler: /home/jsonch/bf_sde/bf-sde-9.2.0/install/bin/p4c
P4 compiler version: 9.2.0 (SHA: 639d9ec) (p4c-based)
Using Build Directory /home/jsonch/bf_sde/bf-sde-9.2.0/build/p4-build/prog
  Building prog in `build_dir prog` CLEAR CONFIGURE MAKE INSTALL ... DONE
```

2. **starting the data plane**

Run ``jsonch@localhost:~/projects/reflector$ $SDE/run_switchd.sh -p prog`` to start the program from its build directory. This will load the program into the ASIC and eventually bring you to the bfshell cli: 

```
jsonch@localhost:~/projects/reflector$ $SDE/run_switchd.sh -p prog
Using SDE /home/jsonch/bf_sde/bf-sde-9.2.0
Using SDE_INSTALL /home/jsonch/bf_sde/bf-sde-9.2.0/install
Setting up DMA Memory Pool
Using TARGET_CONFIG_FILE /home/jsonch/bf_sde/bf-sde-9.2.0/install/share/p4/targets/tofino/prog.conf
Using PATH /home/jsonch/bf_sde/bf-sde-9.2.0/install/bin:/home/jsonch/bf_sde/bf-sde-9.2.0/install/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/lib/platform-config/current/onl/bin:/lib/platform-config/current/onl/sbin:/lib/platform-config/current/onl/lib/bin:/lib/platform-config/current/onl/lib/sbin
Using LD_LIBRARY_PATH /usr/local/lib:/home/jsonch/bf_sde/bf-sde-9.2.0/install/lib:
bf_sysfs_fname /sys/class/bf/bf0/device/dev_add
kernel mode packet driver present, forcing kernel_pkt option!
Install dir: /home/jsonch/bf_sde/bf-sde-9.2.0/install (0x55f13d552560)
bf_switchd: system services initialized
bf_switchd: loading conf_file /home/jsonch/bf_sde/bf-sde-9.2.0/install/share/p4/targets/tofino/prog.conf...
bf_switchd: processing device configuration...
Configuration for dev_id 0
  Family        : tofino
  pci_sysfs_str : /sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0
  pci_domain    : 0
  pci_bus       : 5
  pci_fn        : 0
  pci_dev       : 0
  pci_int_mode  : 1
  sbus_master_fw: /home/jsonch/bf_sde/bf-sde-9.2.0/install/
  pcie_fw       : /home/jsonch/bf_sde/bf-sde-9.2.0/install/
  serdes_fw     : /home/jsonch/bf_sde/bf-sde-9.2.0/install/
  sds_fw_path   : /home/jsonch/bf_sde/bf-sde-9.2.0/install/
  microp_fw_path: 
bf_switchd: processing P4 configuration...
P4 profile for dev_id 0
num P4 programs 1
  p4_name: prog
  p4_pipeline_name: pipe
    libpd: 
    libpdthrift: 
    context: /home/jsonch/bf_sde/bf-sde-9.2.0/install/share/tofinopd/prog/pipe/context.json
    config: /home/jsonch/bf_sde/bf-sde-9.2.0/install/share/tofinopd/prog/pipe/tofino.bin
  Pipes in scope [0 1 2 3 ]
  diag: 
  accton diag: 
  Agent[0]: /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/libpltfm_mgr.so
  non_default_port_ppgs: 0
  SAI default initialize: 1 
bf_switchd: library /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/libpltfm_mgr.so loaded
bf_switchd: agent[0] initialized
Tcl server started..
Tcl server: listen socket created
Tcl server: bind done on port 8008, listening...
Tcl server: waiting for incoming connections...
Health monitor started 
Operational mode set to ASIC
Initialized the device types using platforms infra API
ASIC detected at PCI /sys/class/bf/bf0/device
ASIC pci device id is 16
Skipped pkt-mgr init 
Starting PD-API RPC server on port 9090
bf_switchd: drivers initialized
detecting.. IOMMU not enabled on the platform
-
bf_switchd: dev_id 0 initialized

bf_switchd: initialized 1 devices
bf_switchd: Credo python server thread initialized..credo_python_intf: listen socket created
Adding Thrift service for bf-platforms to server
credo_python_intf: bind done on port 9001, listening...
credo_python_intf: listening for incoming connections...
bf_switchd: thrift initialized for agent : 0
bf_switchd: spawning cli server thread
bf_switchd: spawning driver shell
bf_switchd: server started - listening on port 9999
bfruntime gRPC server started on 0.0.0.0:50052

        ********************************************
        *      WARNING: Authorised Access Only     *
        ********************************************
    
bfshell> 
```

3. **Bringing up ports and testing the program**

The first thing you probably want to do is bring up some ports. This can be done in the control script, but you can also do it manually from bfshell > ucli > pm:


```
bfshell> ucli
Starting UCLI from bf-shell 
Cannot read termcap database;
using dumb terminal settings.
bf-sde> pm
bf-sde.pm> ?
# ... list of commands (not shown)
```
pm has a bunch of commands. The most important ones are: 

``show [-a]`` -- show the currently configured ports. If run with -a, show all ports.

```
bf-sde.pm> show -a
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
PORT |MAC |D_P|P/PT|SPEED  |FEC |RDY|ADM|OPR|LPBK    |FRAMES RX       |FRAMES TX       |E
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
1/0  |23/0|128|3/ 0|-------|----|YES|---|---|--------|----------------|----------------|-
1/1  |23/1|129|3/ 1|-------|----|YES|---|---|--------|----------------|----------------|-
```
Important columns are: 
PORT -- the front panel port name. 
D_P -- the port's id from inside of P4. 
RDY -- is a cable detected? 
ADM -- is the port configured? 
OPR -- is the port down (DWN) or up (UP)?
Most of the other columns are self explanatory. LPBK is whether the port is configured as a loopback port. 

To configure a port, use port-add. To bring a configured port up, use port-enb.

`` port-add        <port_str> <speed (1G, 10G, 25G, 40G, 40G_NB, 50G(50G/50G-R2, 50G-R1), 100G(100G/100G-R4, 100G-R2),200G(200G/200G-R4, 200G-R8), 400G 40G_NON_BREAKABLE)> <fec (NONE, FC, RS)>``

``<port_str>`` is the port's front panel id. 100G ports can be split into 4 separate 25G or 10G ports, so each port id has two components: the physical port name and the id of the port's channel: ``<port id>/<channel id>``

So, for example, `1/0` and `2/0` are the first two ports in 100G mode. If you configure port 1 in 4x25G mode, you can also use ports `1/1`, `1/2`, and `1/3`. 

You configure each port individually. So, to bring up 1/0 - 1/3 in 10G mode with no FEC, use: 

```
bf-sde.pm> port-add 1/0 10G NONE
bf-sde.pm> port-add 1/1 10G NONE
bf-sde.pm> port-add 1/2 10G NONE
bf-sde.pm> port-add 1/3 10G NONE
bf-sde.pm> show                 
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
PORT |MAC |D_P|P/PT|SPEED  |FEC |RDY|ADM|OPR|LPBK    |FRAMES RX       |FRAMES TX       |E
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
1/0  |23/0|128|3/ 0|10G    |NONE|YES|DIS|DWN|  NONE  |               0|               0| 
1/1  |23/1|129|3/ 1|10G    |NONE|YES|DIS|DWN|  NONE  |               0|               0| 
1/2  |23/2|130|3/ 2|10G    |NONE|YES|DIS|DWN|  NONE  |               0|               0| 
1/3  |23/3|131|3/ 3|10G    |NONE|YES|DIS|DWN|  NONE  |               0|               0| 
```

Next, to bring up a configured port, say ``1/0``, use ``port-enb``: 

```
bf-sde.pm> port-enb 1/0
bf-sde.pm> show
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
PORT |MAC |D_P|P/PT|SPEED  |FEC |RDY|ADM|OPR|LPBK    |FRAMES RX       |FRAMES TX       |E
-----+----+---+----+-------+----+---+---+---+--------+----------------+----------------+-
1/0  |23/0|128|3/ 0|10G    |NONE|YES|ENB|DWN|  NONE  |               0|               0| 
1/1  |23/1|129|3/ 1|10G    |NONE|YES|DIS|DWN|  NONE  |               0|               0| 
```

At this point, once the ethernet autonegotiation completes the OPR column for an enabled port should change to "UP". 

Once you have a server connected to a port that's UP, you can test the program: send a packet into the switch from the server, the P4 program should send a copy of the exact same packet back. You should see the frames RX and frames TX counters increase in the CLI. 


3. **A simple python control script**

Instead of configuring the switch manually, you can run the control script ``prog.py`` to configure the switch via grpc and thrift interfaces. These interfaces can also be used to add rules to tables, poll counters, and configure most of the other switch setings. 

After starting the data plane, in a separate window, run: 
``python2 prog.py``
```

jsonch@localhost:~/projects/reflector$ python2 prog.py
adding path: /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/python2.7/site-packages/tofino
adding path: /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/python2.7/site-packages
adding path: /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/python2.7/site-packages/p4testutils
adding path: /home/jsonch/bf_sde/bf-sde-9.2.0/install/lib/python2.7/site-packages/bf-ptf
WARNING:root:VXLAN support not found in Scapy
WARNING:root:ERSPAN support not found in Scapy
WARNING:root:GENEVE support not found in Scapy
WARNING:root:NVGRE support not found in Scapy
controller running (idle) -- press ctrl+c to exit
```

The default ``prog.py`` just sets up connections to the switch's drivers and then idles until ctrl+c. It uses ``libs/mgr.py`` to make the connections. ``mgr.py`` also has some helper functions, like port_up and addExactEntry: 

```
def example_ports_up():
    # bring up port with dpid 128 at 100G.
    m.port_up(128, pal_port_speed_t.BF_SPEED_10G, pal_fec_type_t.BF_FEC_TYP_NONE)    

def example_table_add():
    m.addExactEntry("tiWire", ["ig_intr_md.ingress_port"], [128], "aiOut", {"out_port":128})
```

``mgr.py`` doesn't interact with the grpc interfaces directly, it uses the python libraries included with the SDE for testing tofino programs. The python libraries are in $SDE_INSTALL/lib/python2.7/site-packages. You can get a better sense of how the grpc interface works by digging into those libraries. 



