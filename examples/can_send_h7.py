# CAN Shield Example
#
# This example demonstrates CAN communications between two cameras.
# NOTE: you need two CAN transceiver shields and DB9 cable to run this example.
import pyb
import time, omv
from pyb import CAN

# Create arbitration id from device type, manufacturer, device ID and APIID
def arbitration_id(devtype, mfr, devid, apiid):
    retval = (devtype & 0x1f) << 24
    retval = retval | (mfr & 0xff) << 16
    retval = retval | (apiid & 0x3ff) << 6
    retval = retval | (devid & 0x3f)
    return retval



red_led  = pyb.LED(1)
green_led = pyb.LED(2)

print("Frequencies:")
print(pyb.freq())

can = CAN(2, CAN.NORMAL)
#CAN.initfilterbanks(4);

# Set a different baudrate (default is 125Kbps)
# NOTE: The following parameters are for the H7 only.
#
# can.init(CAN.NORMAL, prescaler=32, sjw=1, bs1=8, bs2=3) # 125Kbps
# can.init(CAN.NORMAL, prescaler=16, sjw=1, bs1=8, bs2=3) # 250Kbps
# can.init(CAN.NORMAL, prescaler=8,  sjw=1, bs1=8, bs2=3) # 500Kbps

# can.init(CAN.NORMAL, prescaler=3,  sjw=1, bs1=11, bs2=5)  # 1000Kbps M7
can.init(CAN.NORMAL, extframe=True, prescaler=4,  sjw=1, bs1=8, bs2=3) # 1000Kbps H7
range_lo = arbitration_id(12,170,3,5)
range_hi = arbitration_id(12,170,3,10)
print("ARB_LO 0x%X"%range_lo)
print("ARB_HI 0x%X"%range_hi)

can.setfilter(0, CAN.RANGE, 0, (range_lo, range_hi))
can.restart()

data1 = bytearray(b'HelloRio')
data2 = bytearray(b'Infinite')
counter = 0

# For efficient reception of can data:
canbuf = bytearray(8)
canlist = [0,0,0,memoryview(canbuf)]

mysendid = arbitration_id(12, 170, 3, 4)
print("MyArbID 0x%X"%mysendid)


while (True):
    green_led.on()
    # Send message with arbitration ID that WPILib will recognize
    try:
        # This uses 29 bit identifier and creates a WPILib compatible arbitration id:
        # The arbitration ID is based on device type = 5 bits, mfr = 8 bits, APIID = 10 bits,
        # DeviceID (in the WPILibsense) is 6 bits.
        # 0x0c = Device Type
        # 0xAA = Manufacturer
        # 0x00 = API ID (which is class + index) of 4 (maps to 0x01 middle byte)
        # 0x03 = Bottom 2 of API PI + DeviceID of 3
        if counter == 0:
            can.send(data1, mysendid, timeout=33)
            counter = counter + 1
        else:
            can.send(data2, mysendid, timeout=33)
            counter = 0

        red_led.off();
    except:
        red_led.on();
        print('CANBus exception!')
        can.restart()
        pass

    green_led.off()
    time.sleep(100)

    # Check for data from CAN:
    if can.any(0):
        can.recv(0, canlist, timeout=50)
        print('!')



