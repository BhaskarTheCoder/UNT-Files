# TCP SYN flood attack

from random import randint
from sys import stdout

from scapy.all import *
from scapy.layers.inet import IP, TCP


