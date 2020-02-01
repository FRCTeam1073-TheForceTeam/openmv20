# FRC CAN Library test - By: rtpac - Sat Jan 25 2020

import sensor, image, time, pyb
# Import the frc_CAN library for talking with the RoboRio
# import frc_CAN


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
        # Device id [0-63]
        self.devid = devid
        # Mode of the device
        self.mode = 0
        # Configuration data
        self.config_simple_targets = 0
        self.config_line_segments = 0
        self.config_color_detect = 0
        self.config_advanced_targets = 0
        self.frame_counter = 0
        # Buffer for receiving data
        self.cbbuffer = bytearray(8)
        self.cbdata = [0, 0, 0, memoryview(self.cbbuffer)]

        # Initialize CAN based on which type of board we're on
        if omv.board_type() == "H7":
            self.can.init(CAN.NORMAL, extframe=True, prescaler=4,  sjw=1, bs1=8, bs2=3) # 1000Kbps H7
            self.can.initfilterbanks(10)
            # Filter 0 sends messages to FIFO 1 for mode messages.
            self.can.setfilter(0, CAN.RANGE, 1, [self.my_arb_id(self.api_id(1,3)),self.my_arb_id(self.api_id(1,3))])
            print("H7 CAN Interface")

        elif omv.board_type() == "M7":
            self.can.init(CAN.NORMAL, extframe=True, prescaler=3,  sjw=1, bs1=10, bs2=7) # 1000Kbps on M7
            self.can.initfilterbanks(10)
            print("M7 CAN Interface")
        else:
            print("CAN INTERFACE NOT INITIALIZED!")


        self.can.restart()

    # Set config: This is reported to rio when we send config.
    def set_config(self, simple_targets, line_segments, color_detect, advanced_targets):
        self.config_simple_targets = simple_targets
        self.config_line_segments = line_segments
        self.config_color_detect = color_detect
        self.config_advanced_targets = advanced_targets

    # Update counter should be called after each processed frame. Sent to Rio in heartbeat.
    def update_frame_counter(self):
        self.frame_counter = self.frame_counter + 1

    def get_frame_counter(self):
        return self.frame_counter


    # Arbitration ID helper packs FRC CAN indices into a CANBus arbitration ID
    def arbitration_id(devtype, mfr, devid, apiid):
        retval = (devtype & 0x1f) << 24
        retval = retval | ((mfr & 0xff) << 16)
        retval = retval | ((apiid & 0x3ff) << 6)
        retval = retval | (devid & 0x3f)
        return retval


    # Arbitration ID helper, assumes devtype, mfr, and instance devid.
    def my_arb_id(self, apiid):
        devtype = 10   # FRC Miscellaneous is our device type
        mfr = 173      # Team 1073 ID to avoid conflict with all COTS devices
        retval = (devtype & 0x1f) << 24
        retval = retval | ((mfr & 0xff) << 16)
        retval = retval | ((apiid & 0x3ff) << 6)
        retval = retval | (self.devid & 0x3f)
        return retval

    # Return the combined API number of an API class and index:
    def api_id(self, api_class, api_index):
        return ((api_class & 0x3f) << 4) | (api_index & 0x0f)

    # Send message to my API id: Sends from OpenMV to Rio with our address.
    def send(self, apiid, bytes):
        sendid = self.my_arb_id(apiid)
        try:
            self.can.send(bytes, sendid, timeout=33)
        except:
            print("CANbus exception.")
            self.can.restart()

    # API Class - 1:  Configuration
    # Whenever we set the mode from here we send it to the RoboRio
    def set_mode(self, mode):
        self.mode = mode
        self.send_config_data()

    # Allows us to read back mode in case Rio sets the mode.
    def get_mode(self):
        return self.mode

    # Send our Config data to RoboRio
    def send_config_data(self):
        cb = bytearray(8)
        cb[0] = self.mode
        cb[2] = self.config_simple_targets
        cb[3] = self.config_line_segments
        cb[4] = self.config_color_detect
        cb[5] = self.config_advanced_targets
        self.send(self.api_id(1,0), cb)

    # Send our camera status data to RoboRio
    def send_camera_status(self, width, height):
        cb=bytearray(8)
        cb[0] = width/4;
        cb[1] = height/4;
        self.send(self.api_id(1,1), cb)

    # Called by filter when FIFO 1 gets a message.
    def incoming_callback_1(can, reason):
        can.recv(1, self.cbdata, timeout=10)

        if reason == 0 or reason == 1:
            if self.cbdata[0] == self.my_arb_id(self.api_id(1,3)):
                # Set our mode from the incoming data:
                self.mode = self.cbdata[3][0]
            elif self.cbdata[0] == self.my_arb_id(self.api_id(1,0)):
                # Respond with configuration:
                self.send_config_data()
        else:
            print("CAN FIFO message lost.")



    # Send the RIO the heartbeat message with our mode and frame counter:
    def send_heartbeat(self):
        hb = bytearray(3)
        hb[0] = (self.mode & 0xff)
        hb[1] = (self.frame_counter & 0xff00) >> 8
        hb[2] = (self.frame_counter & 0x00ff)
        self.send(self.api_id(1,2), hb)

    # API Class - 2: Simple Target Tracking

    # Send tracking data for a given tracking slot to RoboRio.
    def send_track_data(self, slot, cx, cy, vx, vy, type, qual):
        tdb = bytearray(7)
        tdb[0] = (cx & 0xff0) >> 4
        tdb[1] = (cx & 0x00f) << 4 | (cy & 0xf00) >> 8
        tdb[2] = (cy & 0x0ff)
        tdb[3] = (vx & 0xff)
        tdb[4] = (vy & 0xff)
        tdb[5] = (type & 0xff)
        tdb[6] = (qual & 0xff)
        self.send(self.api_id(2, slot), tdb)

    # Track is empty when quality is zero, send empty slot /w 0 quality.
    def clear_track_data(self, slot):
        # Assume fills with zero.
        tdb = bytearray(7)
        self.send(self.api_id(2, slot), tdb)


    # Line Segment Tracking API Class: 3

    # Send line segment data to a slot to RoboRio.
    def send_line_data(self, slot, x0, y0, x1, y1, ttype, qual):
        ldb = bytearray(8)
        ldb[0] = (x0 & 0xff0) >> 4
        ldb[1] = ((x0 & 0x00f) << 4) | ((y0 & 0xf00) >> 8)
        ldb[2] = (y0 & 0x0ff)
        ldb[3] = (x1 & 0xff0) >> 4
        ldb[4] = ((x1 & 0x00f) << 4) | ((y1 & 0xf00) >> 8)
        ldb[5] = (y1 & 0x0ff)
        ldb[6] = (ttype & 0xff)
        ldb[7] = (qual & 0xff)
        self.send(self.api_id(3,slot), ldb)

    # Send null, 0 quality line to clear a slot for RoboRio.
    def clear_line_data(self, slot):
        ldb = bytearray(8)
        self.send(self.api_id(3,slot), ldb)

    # Color Detection API Class: 4

    # Send the given color segmentation data to the RoboRio
    def send_color_data(self, c0,p0,c1,p1,c2,p2,c3,p3):
        cdb = bytearray(8)
        cdb[0] = c0 & 0xff
        cdb[1] = p0 & 0xff
        cdb[2] = c1 & 0xff
        cdb[3] = p1 & 0xff
        cdb[4] = c2 & 0xff
        cdb[5] = p2 & 0xff
        cdb[6] = c3 & 0xff
        cdb[7] = p3 & 0xff
        self.send(self.api_id(4,0), cdb)

    # Send empty color data / invalid colors to RoboRio.
    def clear_color_data(self):
        cdb = bytearray(8)
        self.send(self.api_id(4,0), cdb)

    # Advanced Target Tracking API Class: 5

    # Send advanced target tracking data to RoboRio
    def send_advanced_track_data(self, cx, cy, vx, vy, ttype, qual, skew):
        atb = bytearray(8)
        atb[0] = (cx & 0xff0) >> 4
        atb[1] = ((cx & 0x00f) << 4) | ((cy & 0xf00) >> 8)
        atb[2] = (cy & 0x0ff)
        atb[3] = (vx & 0xff)
        atb[4] = (vy & 0xff)
        atb[5] = (ttype & 0xff)
        atb[6] = (qual & 0xff)
        atb[7] = (skew & 0xff)
        self.send(self.api_id(5, 1), atb)

    # Send a null / 0 quality update to clear track data to RoboRio
    def clear_advanced_track_data(self):
        atb = bytearray(8)
        self.send(self.api_id(5, 1), atb)

# Test Program Main --------------------------------------------------

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2500)

# Creatae our frcCAN object for interfacing with RoboRio over CAN
can = frcCAN(1)

# Set the configuration for our OpenMV frcCAN device.
can.set_config(1, 0, 0, 0)
# Set the mode for our OpenMV frcCAN device.
can.set_mode(1)

while(True):
    can.update_frame_counter() # Update the frame counter.
    img = sensor.snapshot()

    can.send_heartbeat()       # Send the heartbeat message to the RoboRio
    can.send_advanced_track_data(100, 100, 127, -127, 5, 10, 4)
    pyb.delay(100)
    print("HB %d" % can.get_frame_counter())


# add requirements to be able to send to the main turret command
