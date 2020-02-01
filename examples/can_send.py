# CAN Shield Example
#
# This example demonstrates CAN communications between two cameras.
# NOTE: you need two CAN transceiver shields and DB9 cable to run this example.
import pyb
import time, omv
from pyb import CAN

red_led  = pyb.LED(1)
green_led = pyb.LED(2)

def arbitration_id(devtype, mfr, devid, apiid):
    retval = (devtype & 0x1f) << 24
    retval = retval | (mfr & 0xff) << 16
    retval = retval | (apiid & 0x3ff) << 6
    retval = retval | (devid & 0x3f)
    return retval

print("Frequencies:")
print(pyb.freq())

can = CAN(2, CAN.NORMAL)
# Set a different baudrate (default is 125Kbps)
# NOTE: The following parameters are for the H7 only.
#
# can.init(CAN.NORMAL, prescaler=32, sjw=1, bs1=8, bs2=3) # 125Kbps
# can.init(CAN.NORMAL, prescaler=16, sjw=1, bs1=8, bs2=3) # 250Kbps
# can.init(CAN.NORMAL, prescaler=8,  sjw=1, bs1=8, bs2=3) # 500Kbps
can.init(CAN.NORMAL, extframe=True, prescaler=3,  sjw=1, bs1=10, bs2=7)  # 1000Kbps

can.restart()

mysendid = arbitration_id(12, 170, 3, 4)

while (True):
    green_led.on()
    try:
        can.send(b'HelloCan', mysendid, timeout=33)
        red_led.off();
    except:
        red_led.on();
        print('CANBus exception!')
        can.restart()
        pass

    green_led.off()
    time.sleep(500)
