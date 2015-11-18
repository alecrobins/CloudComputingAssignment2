#!/usr/bin/python

import re, sys, time, select, os, subprocess, threading, errno
from mininet.net import Mininet
from mininet.node import Controller, Host, CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel, info, debug
from optparse import OptionParser
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.util import isShellBuiltin, dumpNodeConnections


"global variables"
h1=0  #host1
h2=0  #host2
h3=0  #host3
s1=0  #switch1
s2=0  #switch2
net = Mininet( controller=Controller, link=TCLink )
net.addController( 'c0' )
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
silentremove("/vagrant/h3-h1-ping.log")
silentremove("/vagrant/h3-h2-ping.log")



def addHosts():
    global h1, h2, h3

    # Add three hosts h1, h2, h3 to the network
    info( '\nadding host h1' )
    h1 = net.addHost('h1', ip='10.0.0.1');

    info( '\nadding host h2')
    h2 = net.addHost('h2', ip='10.0.0.2')

    info( '\nadding host h3' )
    h3 = net.addHost('h3', ip='10.0.0.3' )



def addSwitches():
    global s1, s2

    # Add two switches s1 and s2
    info( '\nadding switch s1:' )
    s1 = net.addSwitch('s1');

    info( '\nadding switch s2:' )
    s2 = net.addSwitch('s2');



def setLinks():

    info( '\nsetting a link between switch s1 and host h1\n' )
    net.addLink(h1, s1)

    info( '\nsetting a link between switch s1 and host h2\n' )
    net.addLink(h2, s1)

    info( '\nsetting a link between switch s2 and host h3\n' )
    net.addLink(h3, s2)

    info( '\nsetting a link between switch s1 and switch s2\n' )
    net.addLink(s1, s2)


def networking_application():
    "obtaining the values of hosts from network."
    h1 = net.get('h1')  
    h2 = net.get('h2')  
    h3=  net.get('h3')  

    info( '\nrunning a command on h3\n' )
    command =  "/bin/bash -c 'while true; do ping -D -c 4 10.0.0.1 &>> /vagrant/h3-h1-ping.log; ping -D -c 4 10.0.0.2 &>> /vagrant/h3-h2-ping.log; sleep 1; done'"
    h3.sendCmd(command)

    "normal case: when all links are working"
    info( '\n(Normal Case): when all links are working\n' )
    time.sleep(50);



    "fault 1: bring down link between h1 and s1"
    info( '\n(Fault 1): Bringing down link between h1 and s1\n' )
    net.configLinkStatus('h1','s1','down')

    time.sleep(50)


    "fault 2: bring down link between s1 and s2 . (first, bring up link between h1 and s1 that you just brought down)"
    info( '\n(Fault 2): Bringing down link between s1 and s2\n' )
    net.configLinkStatus('h1','s1','up')
    net.configLinkStatus('s1','s2','down')
    "write your code here. use net.configLinkStatus command"


    time.sleep(50)


    "now you can check the h3-h1-ping.log and h3-h2-ping.log files in the current folder of your laptop or at /vagrant folder of the VM "
    "three 50 seconds periods"
    "during first period: h3 should be able ping to both h1 and h2"
    "during second period: h3 should be able ping to h2 but not h1"
    "during third period: h3 should be able ping neither to h1 nor to h2"
    "(optional)also you can check how link parameters that you set before like bandwidth, delay and packet loss affect this communication."

if __name__ == '__main__':
    setLogLevel( 'info' )
    info( '\n(1) Adding Hosts..(removing first if exists)\n' )
    #addHosts();    # Uncomment this line and implement this function. see above
    info( '\n\n(2) Adding switches..(removing first if exists)\n' )
    #addSwitches(); # Uncomment this line and implement this function. see above
    info( '\n\n(3) Setting Links amongst Hosts and Switches\n')
    #setLinks(); # Uncomment this line and implement this function. see above
    info( '\n\n(4) Starting mininet virtual network\n')
    #net.start() # Uncomment this line
    info( '\n\n(5) Deploying networking_application on this mininet network topology\n' )
    #networking_application(); # Uncomment this line and implement this function. see above
  
