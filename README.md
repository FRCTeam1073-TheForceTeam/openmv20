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



