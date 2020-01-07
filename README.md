# openmv20
2020 and 2019 Offseason OpenMV Development

This code is based on using the OpenMV camera modules and the CANshield
to allow them to be powered via 12VDC from the PCP and connect to the
Robot CANBus.

Each OpenMV module must have a unique CAN ID that must be different
from all other IDs on the CANbus. Then vision (or other sensor
interface) programs are written that send back (or respond to) CANBus
message from the main robot program on the RoboRio. This gives us a
flexible sensing module that can be very reliably connected to the
RoboRio over CANBus.

The OpenMV approach allows you to write and select many different, fast
low-level vision algorithms like target detection, line following, blob
following, etc. and send back simple information messages to the RoboRio
without using up the RoboRio compute resources AND without needing to use
unreliable USB connections. CANBus (while limited) is extremely reliable
and allows your OpenMV based sensing to be a reliable part of the robot
system.

If they are engaged as needed, a robot might have many OpenMV cameras
mounted in many different locations very easily and request data from
just the ones it needs at any given moment.

Information about the OpenMV camera modules can be found here:

https://openmv.io/


Details on the OpenMV CANShield can be found here:

https://openmv.io/collections/shields/products/can-shield

# Important Limitations

Note that CANBus sends very short messages (just 8 bytes at a time max) and
is used to control the robot motors and monitor the PDP. It is important
to limit the amount of CANBus traffic that you add from your OpenMV camera
sensor modules on the bus. With just a few messages at a few times/second
you can make very powerful systems!

CANBus cannot send an image back to the RoboRio. It processes images
(or other inputs, the OpenMV is super flexible) and packages the
answers up and sends them back to the RoboRio for use in robot code.


# Example Programs

The OpenMV system comes with many example programs itself and we include
additional example programs here specifically to use for CANBus setup
and exchanging CAN messages with the RoboRio.

On the RoboRio you make a Subsystem in your Robot Program that uses
the CAN interface clases to exchange messages with OpenMV cameras
on CANbus.


# CANBus Message Concepts

Each OpenMV occupies many different "API Index" slots for a specific
device type, manufacturer and device ID. These are terms used by the
WPILib CANBus conventions for packing data from hardware to/from
CANBus messages. The RoboRio expects CANBus 2.0, 29-bit long CAN
arbitration ID's to be made from the device type, manufacturer, device
ID and API index. Example code shows building up an ID like this.

Each OpenMV node in CANBus will appear to the RoboRio as a custom
CANBus sensor that has a well defined type, manufacturer, device ID
and a collection of API index "slots" that are each up-to 8 bytes of
data. The OpenMV (depending on what it needs to do, sends the RoboRio
by writing its feedback data to one of these API Index slots).

The following section describes the basic strategy for using these
CANBus slots to send information back to the RoboRio. Specific
functions will each have their own specific messages but they should
all follow this same basic format.


- API Index 0: This is an 8 byte message. It is sent at the heartbeat
  period for the OpenMV module (1/second minimum) or when needed due
  to updates. The RoboRio can detect a module of a specific type by
  listening for the heartbeat of this message.

  - Byte 0:	    Status	0x00 = Unknown, 0x01 = Idle, 0x7f = Fault
    	 	    		0x02 = Running
  - Byte 1:	    Mode	0x00 = Unknown, Other number is running mode
  - Byte 2:	    Data	0x00 = No other feedback data, 0x01 0 0x0f
    	 	    		       Indicates between 1 and 15 items.
  - Byte 3:	    Reserved 	       Not used.
  - Byte 4 - 7:	    Timestamp	       Interpret as 32 bit timer in ms.

- API Index 1: This is a 1 byte message. It is sent from Rio to OpenMV
  and is used to set the operating mode of the module. This is the set
  mode command.

  - Byte 0:   	    Mode  	0x00 = Go to Idle, Other number is go to
    	 	    		       that mode. 

- API Index 2+: There is generally 1 to 15 active data items in the
  next 15 API indices. Each one has its own up to 8 bytes. Example
  data includes:


  API Index 2 + N:	Example tracking data. 8 Bytes
      - Byte 0:		Target ID	 0x00 = None, 0x01 to 0x7f is ID#
      - Byte 1:		Quality		 0x00 = Bad lock, 0x7f = Perfect lock.
      - Byte 2:		X pos		 +- 127 from center (scaled)
      - Byte 3:		Y pos		 +- 127 from center (scaled)
      - Byte 4:		Width		 0x01 to 0x7f target X size.
      - Byte 5:		Height		 0x01 to 0x7f target Y size.
      - Byte 6:		X vel		 +- 127 pixels/t
      - Byte 7:		Y vel		 +- 127 pixels/t


      This can be used to track targets for shooting or collections of
      balls to locae on a field for example.


   API Index 2 + N:	Example line marker data. 7 Bytes
      - Byte 0:	 	Line ID	     	 0x00 = White, 0x01 = Red, 0x02 = Blue
      - Byte 1:		Quality		 0x00 = Bad, 0x7f = Perfect data.
      - Byte 2:		X0		 +- 127 from center (scaled)
      - Byte 3:		Y0		 +- 127 from center (Scaled)
      - Byte 4:		X1		 +- 127 from center (scaled)
      - Byte 5:		Y1		 +- 127 from center (Scaled)
      - Byte 6:		Length		 0x00 = None, 0x7f = Max length (scaled)

      This can be used to transmit lines detected on the field for
      alignment.


  API Index 2 + N:	Example IMU data. 6 Bytes.

      - Byte 0:		Pitch - Lo
      - Byte 1:		Pitch - Hi
      - Byte 2:		Roll - Lo
      - Byte 3:		Roll - Hi
      - Byte 4:		Yaw - Lo
      - Byte 5:		Yaw - Hi

      This can be used to transmit orientation from an IMU at 16 bit
      resolution.

  API Index 2+ N:	Example Ground Plane Segmentation

      - Byte 0 - 7: Free Range 0x00 = infinity, 0x01 to 0x7f is range
        i n a given sector.

	This can be used to avoid collisions with ground plane objects
	by ranging using a single camera


  API Index 2+ N:	4-Color Sector Information

      - Byte 0 		Zone A Color	- 0x00 = Unknown, 0x01 ... 0x7f Color
      - Byte 1		Zone A Quality  - 0x00 = Bad, 0x7f = Best.
      ...
