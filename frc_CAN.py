# This module implements the FRC CAN support library
# for our OpenMV cameras to talk to the RoboRio using
# FRC Can Arbitration IDs.
#
from pyb import CAN
import omv

# Puts all the CAN support for FRC into one reusable place.
# This class uses FIFO 1 for callbacks in the API Class = 1
# space for mode control. FIFO 0 is used for other messages.
class frcCAN:
    
    def __init__(self, devid):
        self.can = CAN(2, CAN.NORMAL)
        self.devid = devid
        self.status = 0
        self.config_simple_targets = 0
        self.config_line_segments = 0
        self.config_color_detect = 0
        self.config_advanced_targets = 0

        if omv.baord_type() == "H7":
            self.can.init(CAN.NORMAL, extframe=True, prescaler=4,  sjw=1, bs1=8, bs2=3) # 1000Kbps H7
            self.can = null
        elif omv.board_type() == "M7":
            self.can.init(CAN.NORMAL, extframe=True, prescaler=3,  sjw=1, bs1=10, bs2=7)  # 1000Kbps on M7

        self.can.initfilterbanks(10)
        self.can.setfilter(0, CAN.LIST32, 1, [0x00, 0x00])
        self.can.setfilter(1, CAN.LIST32, 1, [0x00, 0x00])
        self.can.restart()

    # Set capability/config:
    def set_config(simple_targets, line_segments, color_detect, advanced_targets):
        self.config_simple_targets = simple_targets
        self.config_line_segments = line_segments
        self.config_color_detect = color_detect
        self.config_advanced_targets = advanced_targets
        

    # Arbitration ID helper:
    def arbitration_id(devtype, mfr, devid, apiid):
        retval = (devtype & 0x1f) << 24
        retval = retval | (mfr & 0xff) << 16
        retval = retval | (apiid & 0x3ff) << 6
        retval = retval | (devid & 0x3f)
        return retval


    # Arbitration ID helper, assumes devtype, mfr, and instance devid.
    def my_arb_id(apiid):
        devtype = 10   # FRC Miscellaneous device type
        mfr = 173      # Team 1073 ID to avoid conflict with COTS devices
        retval = (devtype & 0x1f) << 24
        retval = retval | (mfr & 0xff) << 16
        retval = retval | (apiid & 0x3ff) << 6
        retval = retval | (self.devid & 0x3f)
        return retval

    # Return the combined API number of a class and index:
    def apiid(api_class, api_index):
        return 0

    # Send message to my API id:
    def send(apiid, bytes):
        sendid = my_arb_id(apiid)
        try:
            self.can.send(bytes, sendid, timeout=33)
        except:
            self.can.restart()

    # API Class - 1:  Configuration
    def set_mode(mode):
        self.mode = mode
        send_config_data()

    def get_mode():
        return self.mode

    def send_config_data():
        mb = bytearray(8)
        mb[0] = self.mode
        mb[2] = self.simple_targets
        mb[3] = self.line_segments
        mb[4] = self.color_detect
        mb[5] = self.advanced_targets
        send(api_id(1,0), mb)

    # Send the RIO the heartbeat message:
    def send_heartbeat(counter):
        hb = bytearray(3)
        hb[0] = (self.mode & 0xff)
        hb[1] = (counter & 0xff00) >> 8
        hb[2] = (counter & 0x00ff)
        send(api_id(1,2), hb)

    # API Class - 2: Simple Target Tracking

    # Send tracking data for a given tracking slot.
    def send_track_data(slot, cx, cy, vx, vy, type, qual):
        tdb = bytearray(7)
        tdb[0] = (cx & 0xff0) >> 4
        tdb[1] = (cx & 0x00f) << 4 | (cy & 0xf00) >> 8
        tdb[2] = (cy & 0x0ff)
        tdb[3] = (vx & 0xff)
        tdb[4] = (vy & 0xff)
        tdb[5] = (type & 0xff)
        tdb[6] = (qual & 0xff)
        send(api_id(2, slot), tdb)

    # Track is empty when quality is zero, send empty slot /w 0 quality.
    def clear_track_data(slot):
        # Assume fills with zero.
        tdb = bytearray(7)
        send(api_id(2, slot), tdb)


    # Line Segment Tracking API Class: 3
    
    # Send line segment data to a slot.
    def send_line_data(slot, x0, y0, x1, y1, type, qual):
        ldb = bytearray(8)
        ldb[0] = (x0 & 0xff0) >> 4
        ldb[1] = (x0 & 0x00f) << 4 | (y0 & 0xf00) >> 8
        ldb[2] = (y0 & 0x0ff)
        ldb[3] = (x1 & 0xff0) >> 4
        ldb[4] = (x1 & 0x00f) << 4 | (y1 & 0xf00) >> 8
        ldb[5] = (y1 & 0x0ff)
        ldb[6] = (type & 0xff)
        ldb[7] = (qual & 0xff)
        send(api_id(3,slot), ldb)

    # Send null, 0 quality line to clear a slot.
    def clear_line_data(slot):
        ldb = bytearray(8)
        send(api_id(3,slot), ldb)

    # Color Detection API Class: 4

    def send_color_data(c0,p0,c1,p1,c2,p2,c3,p3):
        cdb = bytearray(8)
        cdb[0] = c0
        cdb[1] = p0
        cdb[2] = c1
        cdb[3] = p1
        cdb[4] = c2
        cdb[5] = p2
        cdb[6] = c3
        cdb[7] = p3
        send(api_id(4,0), cdb)

    def clear_color_data():
        cdb = bytearray(8)
        send(api_id(4,0), cdb)

    # Advanced Target Tracking API Class: 5
    
    def send_advanced_track_data(cx, cy, vx, vy, type, qual, skew):
        atb = bytearray(8)
        atb[0] = (cx & 0xff0) >> 4
        atb[1] = (cx & 0x00f) << 4 | (cy & 0xf00) >> 8
        atb[2] = (cy & 0x0ff)
        atb[3] = (vx & 0xff)
        atb[4] = (vy & 0xff)
        atb[5] = (type & 0xff)
        atb[6] = (qual & 0xff)
        atb[7] = (skew & 0xff)
        send(api_id(5, 1), atb)

    # Send a null / 0 quality update to clear track data.
    def clear_advanced_track_data():
        atb = bytearray(8)
        send(api_id(5, 1), atb)
