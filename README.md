# openmv20
2020 and 2019 Offseason OpenMV Development

This code is based on using the OpenMV camera modules and the CANshield
to allow them to be powered via 12VDC from the PCP and connect to the
Robot CANBus.

Each OpenMV module must use unique CAN arbitration ID's that must be
different from all other IDs on the CANbus. These CAN arbitation ID's
are 29-bit long identifiers on CANBus that must follow the WPILib /
FRC conventions for creating an dusing CAN arbitration IDs.

Information on the FRC format is available here:
https://docs.wpilib.org/en/latest/docs/software/can-devices/can-addressing.html


OpenMV programs are written to respond to / send a collection of
CANBus messages from the main robot program on the RoboRio. This gives
us a flexible custom sensing module that can be very reliably
connected to the RoboRio over CANBus and powered by 12V PDP power.

This approach allows you to write and select many different, fast
low-level vision algorithms like target detection, line following,
blob following, etc. and send back simple information messages to the
RoboRio without using up the RoboRio compute resources AND without
needing to use unreliable USB connections. CANBus (while limited) is
extremely reliable and allows your OpenMV based sensing to be a
reliable part of the robot system.

If they are engaged as needed, a robot might have many OpenMV cameras
mounted in many different locations very easily and request data from
just the ones it needs at any given moment.

Information about the OpenMV camera modules can be found here:

https://openmv.io/

Details on the OpenMV CANShield can be found here:

https://openmv.io/collections/shields/products/can-shield


# Example Programs

The OpenMV system comes with many example programs itself and we include
additional example programs here specifically to use for CANBus setup
and exchanging CAN messages with the RoboRio.

On the RoboRio you make a Subsystem in your Robot Program that uses
the CAN interface clases to exchange messages with OpenMV cameras
on CANbus.



# Important Limitations

Note that CANBus sends very short messages (just 8 bytes at a time max) and
is used to control the robot motors and monitor the PDP. It is important
to limit the amount of CANBus traffic that you add from your OpenMV camera
sensor modules on the bus. With just a few messages at a few times/second
you can make very powerful systems!

CANBus cannot send an image back to the RoboRio. The OpenMV module
processes images (or other inputs, the OpenMV is super flexible) and
packages the answers from processing (like the location of a target)
up and sends them back to the RoboRio for use in robot code.

Our OpenMV modules are custom sensors on CANBus and do not drive any
motors or actuate any movement of any kind. They just gather data for
our robot program to use and do pre-processing on it for us.


# CANBus Arbitration IDs

The RoboRio expects CANBus 2.0, 29-bit long CAN arbitration ID's to be
made from the device type, manufacturer, device ID and API
index. Example code shows building up an ID of this kind.

Each OpenMV node in CANBus will appear to the RoboRio as a custom
CANBus sensor that has a well defined type, manufacturer, device ID
and a collection of API index "slots" that are each up-to 8 bytes of
data. The OpenMV (depending on what it needs to do, sends the RoboRio
by writing its feedback data to one of these API Index slots).

CANBus arbitration IDs are assigned following the conventions
established by WPILib. For our custom CANBus sensors we need to make
sure they can't conflict with any COTS CAN devices we have on our
robots. Following the FRC CAN specification we select the following
elements of our CANBus arbitration ID's in OpenMV code:

- Device Type [5 bits]: 10 = Miscellaneous.
- Manufacturer [8 bits]: 173 = We're our own 'manufacturer' of custom sensors.
- Device Number [4 bits]: 0,1,2,3 depending on instances of the sensor.
- API Class [6-bit] and API Index [4-bit] will follow formats described below.
- Broadcast Messages: We respond to the disable broadcast message
  which is Device Type = 0, Manufacturer = 0, API Class = 0.


# CANBus Messages

Our OpenMV sensors will all implement API Classes:

- 1 : Configuration API Class
- 2 : Simple Target Tracking API Class
- 3 : Line Segment Tracking API Class
- 4 : Color Detection API Class
- 5 : Advanced Target Tracking API Class


## Configuration API : API Class = 1

The configuration API is implemented by all our OpenMV sensor nodes
and is used to query information about the sensor and configure
the sensor. Each API Index is defined below:


- API Index 0 : Configuration Data : OpenMV => Rio
      - Byte 0 : Mode : 0x00 = unknown, 0x01 = idle, 0x02 = running, 0x03 = calibrating, 0x7f = fault
      - Byte 1 : Reserved = 0
      - Byte 2 : Simple Target Tracking 0x00 = no, > 0x00 = slots
      - Byte 3 : Line Segment Tracking 0x00 = no, > 0x00 = slots
      - Byte 4 : Color Detection 0x00 = no, > 0x00 = yes
      - Byte 5 : Advanced Target Tracking API Class 0x00 = no, > 0x00 = yes
      - Byte 6 : Reserved = 0
      - Byte 7 : Reserved = 0

- API Index 1 : Camera Status: OpenMV => Rio
      - Byte 0 : Image Width / 4
      - Byte 1 : Image Height / 4
      - Byte 2 : Reserved = 0
      - Byte 3 : Reserved = 0
      - Byte 4 : Reserved = 0
      - Byte 5 : Reserved = 0
      - Byte 6 : Reserved = 0
      - Byte 7 : Reserved = 0

- API Index 2 : Heartbeat: OpenMV => Rio periodically sent ~ 1/second
      - Byte 0 : Status : As above.
      - Byte 1 : Frame counter high byte. 16-bit unsigned.
      - Byte 2 : Frame counter low byte.

- API Index 3 : Mode Control: Rio => OpenMV
      - Byte 0 : Mode: Set mode to this value.

## Simple Target Tracking API Class: API Class = 2

The simple target tracking API is implemented by nodes that indicate
target tracking in their configuration. When the node is enabled it
provides periodic feedback by writing from the node to the
RoboRio. The simple target tracking concept is for tracking small
blobs like balls that are distinguished by color or have a known
shape. Many differen types can be tracked and reported at the same
time. The center of the target position and its velocity image are
returned along with the type and quality rating.

The current interface allows for 6 simultaneous tracks. When a track
is lost an update is sent with quality = 0 and then it is not sent
again until there is an active track.

- API Index 0 : Track 0 Data : OpenMV => Rio, Periodic
      - Byte 0: 24 bit hi  \
      - Byte 1: 24 bit mid = two 12 bit #'s for Cx, Cy position.
      - Byte 2: 24 bit low /
      - Byte 3: 8 bit +- 127 velocity in X
      - Byte 4: 8 bit +- 127 velocity in Y
      - Byte 5: Type 0-15
      - Byte 6: Quality [0 - 100] %  0 = not active.
- API Index 1 : Track 1 Data : OpenMV => Rio, Periodic
      - Same as Track 0 Data
- API Index 2 : Track 2 Data : OpenMV => Rio, Periodic
      - Same as Track 0 Data
- API Index 3 : Track 3 Data : OpenMV => Rio, Periodic
      - Same as Track 0 Data
- API Index 4 : Track 4 Data : OpenMV => Rio, Periodic
      - Same as Track 0 Data
- API Index 5 : Track 5 Data : OpenMV => Rio, Periodic
      - Same as Track 0 Data

The pixel coordinates are 2 12-bit numbers packed into 3 bytes as follows:

Byte 0: high 8 bits of X coordinate.
Byte 1: upper 4 bits are lower 4 bits of X coordinate.
        lower 4 bits are upper 4 bits of Y coordinate.
Byte 2: lower 8 bits of Y coordinate.


## Line Segment Tracking API Class: API Class = 3

The line segment API is implemented by nodes that indicate segment
tracking in their configuration. These are sent to Rio when segments
are found. When segments are lost, updates with quality = 0 are sent
to Rio. There can be many line segment types returned. The current
protocol can reutrn up to 6 lines at a time.

- API Index 0: Segment 0 Data : OpenMV => Rio, Periodic
      - Byte 0: 24 bit hi  \
      - Byte 1: 24 bit mid = Two 12 bit #'s for X0,Y0
      - Byte 2: 24 bit low /
      - Byte 3: 24 bit hi  \
      - Byte 4: 24 bit mid = Two 12 bit #'s for X1,Y1
      - Byte 5: 24 bit low /
      - Byte 6: Type [ 0 - 15]
         - 0 = White
         - 1 = Red
         - 2 = Blue
      - Byte 7: Quality [0-100] %  0 = not active.
- API Index 1: Segment 1 Data : OpenMV => Rio, Periodic
      - Same as Segment 0 Data
- API Index 2: Segment 2 Data : OpenMV => Rio, Periodic
      - Same as Segment 0 Data
- API Index 3: Segment 3 Data : OpenMV => Rio, Periodic
      - Same as Segment 0 Data
- API Index 4: Segment 4 Data : OpenMV => Rio, Periodic
      - Same as Segment 0 Data
- API Index 5: Segment 5 Data : OpenMV => Rio, Periodic
      - Same as Segment 0 Data

The pixel coordinates are 2 12-bit numbers packed into 3 bytes as follows:

Byte 0: high 8 bits of X coordinate.
Byte 1: upper 4 bits are lower 4 bits of X coordinate.
        lower 4 bits are upper 4 bits of Y coordinate.
Byte 2: lower 8 bits of Y coordinate.


## Color Detection API Class: API Class = 4

The color detection API class is implemented by nodes that indicate
color detection in their configuration. The color detection API is
used to distingush color sequences or areas. The colors are presented
in order in the scene. Colors should be reported in left-to-right
order from the image and their horizontal locations [percentage]
provided.

- API Index 0: Color Detection Report: OpenMV => Rio, Periodic
      - Byte 0: Color Code (leftmost) 0 : see code
      - Byte 1: [0-100] % of image position 0 = left edge, 100 = right edge
      - Byte 2: Color Code (next leftmost) 1 : see code
      - Byte 3: [0-100] % of image position 0 = left edge, 100 = right edge
      - Byte 4: Color Code 2 : see code
      - Byte 5: [0-100] % of image position 0 = left edge, 100 = right edge
      - Byte 6: Color Code 3 : see code
      - Byte 7: [0-100] % of image position 0 = left edge, 100 = right edge

The code values for colors are:
    - 0 = inactive slot
    - 1 = unknown
    - 2 = red
    - 3 = yellow
    - 4 = green
    - 5 = blue

## Advanced Target Tracking API Class: API Class = 5

The advanced target trading API is implemented by nodes that indicate
advanced target tracking in their configuration. The Advanced Target
Tracking interface adds additional details to the simple target
tracking interface but tracks fewer targets and offers illumination
control. When the target is returned as quality = 0, there is no
target.


- API Index 0: Advanced Target Tracking API Control: Rio => OpenMV
      - Byte 0: [0 - 100] % Illumination Power
      - Byte 1: [0 - 127] Illumination Hue

- API Index 1: Advanced Target Data: OpenMV => Rio, Periodic
      - Byte 0: 24 bit hi  \
      - Byte 1: 24 bit mid = two 12 bit #'s for Cx, Cy position.
      - Byte 2: 24 bit low /
      - Byte 3: 16 bit hi - area
      - Byte 4: 16 bit low - area
      - Byte 5: Type 0-15
      - Byte 6: Quality [0 - 100] %  0 = not active.
      - Byte 7: Skew +- 127 skewness of target. 0 = perpendicular.

The pixel coordinates are 2 x 12-bit numbers packed into 3 bytes as
follows:

Byte 0: high 8 bits of X coordinate.
Byte 1: upper 4 bits are lower 4 bits of X coordinate.
        lower 4 bits are upper 4 bits of Y coordinate.
Byte 2: lower 8 bits of Y coordinate.

The area of the target is returned in pixels as a 16-bit number.

