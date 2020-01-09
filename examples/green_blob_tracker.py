# Blob tracker for the green LED ring for turret use

import sensor, image, time, math, pyb
from pyb import CAN

threshold_index = 0

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(80, 95, -55, -40, -20, 10), # specific_green_threshold @ 900 exposure & 9 volts
             (15, 40, -40, -30, 20, 40)] # specific_green_threshold @ 300 exposure

# Camera settings
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_exposure(False, 900)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

# LEDs for determining blob status
red_led  = pyb.LED(1)
green_led = pyb.LED(2)

# Basic CAN setup
can = CAN(2, CAN.NORMAL)
can.init(CAN.NORMAL, prescaler=3,  sjw=1, bs1=11, bs2=5)  # 1000Kbps
can.restart()

while(True):
    numBlobs = 0
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=150, merge=True):
        numBlobs+=1
        # Below variables are the x and y coordinates of the inner port target
        target_x = int((blob.major_axis_line()[0] + blob.major_axis_line()[2]) / 2)
        target_y = int(min(blob.minor_axis_line()[1], blob.minor_axis_line()[3]))
        img.draw_circle(target_x, target_y, 5)
        img.draw_rectangle(blob.rect())

    # Green LED = at least 1 blob seen, red LED = no blobs seen
    if numBlobs > 0:
        green_led.on()
        red_led.off()
    else:
        green_led.off()
        red_led.on()
