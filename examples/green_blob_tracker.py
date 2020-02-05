# Blob tracker for the green LED ring for turret use

import sensor, image, time, math, pyb
from pyb import CAN

threshold_index = 2

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(80, 95, -55, -40, -20, 10), # specific_green_threshold @ 900 exposure & 9 volts
             (15, 95, -40, 0, -10, 40),
             (50, 95, -80, -30, -10, 50)]

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

def findLength(blobData):
    return math.sqrt(math.pow(blobData[0] - blobData[2], 2) + math.pow(blobData[1] - blobData[3], 2))

while(True):
    numBlobs = 0
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=100, area_threshold=1000, merge=True):
        # print(findLength(blob.minor_axis_line())) = 90
        # print(findLength(blob.major_axis_line())) = 185
        if findLength(blob.minor_axis_line()) > findLength(blob.major_axis_line())/3 and findLength(blob.minor_axis_line()) < findLength(blob.major_axis_line())/1.8:
            numBlobs += 1
            # Below variables are the x and y coordinates of the inner port target
            target_x = int((blob.major_axis_line()[0] + blob.major_axis_line()[2]) / 2)
            target_y = int(min(blob.minor_axis_line()[1], blob.minor_axis_line()[3]))
            img.draw_circle(target_x, target_y, 5)
            img.draw_rectangle(blob.rect())
            # dims: 37.75 x 18
            # dist for full x on full screen: 320 pixels, 31.5 inches
            # dist for full x on half screen: 160 pixels, 72 inches
            # dist for full x on 4/5 screen: 256 pixels, 40 inches
            # width = 320
            dist = (0.001253 * (findLength(blob.major_axis_line()) ** 2)) - (0.8547 * findLength(blob.major_axis_line())) + 176.7
            print("distance to target is: " + str(dist))

#    try:
#        if counter == 0:
#            can.send(data1, mysendid, timeout=33)
#            counter = counter + 1
#        else:
#            can.send(data2, mysendid, timeout=33)
#            counter = 0
#    except:
#        print('CANBus exception!')
#        can.restart()
#        pass

    # Green LED = at least 1 blob seen, red LED = no blobs seen
    if numBlobs > 0:
        green_led.on()
        red_led.off()
    else:
        green_led.off()
        red_led.on()
#    time.sleep(100)

    # Check for data from CAN:
#    if can.any(0):
#        can.recv(0, canlist, timeout=50)
#        print('!')
