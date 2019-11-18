# CAN Shield Example
#
# This example demonstrates CAN communications between two cameras.
# NOTE: you need two CAN transceiver shields and DB9 cable to run this example.

import time, omv
import pyb
from pyb import CAN

red_led  = pyb.LED(1)
green_led = pyb.LED(2)

print("Frequencies:")
print(pyb.freq())

can = CAN(2, CAN.NORMAL)
# Set a different baudrate (default is 125Kbps)
# NOTE: The following parameters are for the H7 only.
#
# can.init(CAN.NORMAL, prescaler=32, sjw=1, bs1=8, bs2=3) # 125Kbps
# can.init(CAN.NORMAL, prescaler=16, sjw=1, bs1=8, bs2=3) # 250Kbps
# can.init(CAN.NORMAL, prescaler=8,  sjw=1, bs1=8, bs2=3) # 500Kbps
can.init(CAN.NORMAL, prescaler=3,  sjw=1, bs1=11, bs2=5) # 1000Kbps

can.restart()


# Set a filter to receive messages with id=33,34,35,36
# Filter index, mode (LIST16, etc..), FIFO (0 or 1), params
can.setfilter(0, CAN.LIST16, 0, (33,34,35,36))

while (True):
    # Receive messages on FIFO 0s
    try:
        print(can.recv(0, timeout=1000))
        red_led.off();
        green_led.toggle()
    except:
        red_led.on();
        time.sleep(1000);
        red_led.off();

