# CAN Shield Example
#
# This example demonstrates CAN communications between two cameras.
# NOTE: you need two CAN transceiver shields and DB9 cable to run this example.
import pyb
import time, omv
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
can.init(CAN.NORMAL, prescaler=3,  sjw=1, bs1=11, bs2=5)  # 1000Kbps

can.restart()

while (True):
    green_led.on()
    # Send message with id 33
    try:
        can.send(b'HelloCan', 33, timeout=100)
        red_led.off();
    except:
        red_led.on();
        pass

    green_led.off()
    time.sleep(500)
