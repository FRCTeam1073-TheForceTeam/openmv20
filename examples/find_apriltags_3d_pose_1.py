# Multi Color Blob Tracking Example
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math, networktables

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [(74, 90, -16, 9, 38, 72), # generic_green_thresholds
              (93, 100, -9, 3, -10, 17)] # generic_blue_thresholds
# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.
sd = NetworkTables.getTable('SmartDashboard')
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

yellow_pixel_array = []
white_pixel_array = []

# Finds the distance from
def distance_finder(blobData, img):
    obj_height = 6.0
    img_height_pixels = img.height()
    blob_pixels = blobData.area()
    camera_height = 8.5
    dist_inches = (blob_pixels*camera_height)/(obj_height*img_height_pixels)
    return dist_inches
# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. Don't set "merge=True" becuase that will merge blobs which we don't want here.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200):
        # These values depend on the blob not being circular - otherwise they will be shaky.

        if blob.elongation() > 0.5:
            #if aspect ratio is high, then red and green lines are drawn
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        #normal rectangle around blob
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        pixelDist = distance_finder(blob, img)
        print("dist: ")
        print(pixelDist)
        sd.setNumber(pixelDist)

        #tuple append_tuple = (blob.cx(), blob.cy())
        #if blob.code() == 0:

        #if blob.code() == 1:

        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
    print(clock.fps())
