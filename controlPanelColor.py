import sensor, image, time, math

thresh = [(50, 85, 70, 90, 60, 75),       #red
          (35, 80, -65, -45, 30, 45),     #green
          (55, 90 -30, -10, -45, -35),      #blue
          (60, 80, -10, 10, 60, 80)]      #yellow

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_saturation(2)
sensor.set_brightness(-1 )
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    for blob in img.find_blobs(thresh, pixels_threshold=200, area_threshold=200):

        if blob.code() == 1:        #red
            img.draw_rectangle(blob.rect(), color=(250, 0, 0))
            img.draw_cross(blob.cx(), blob.cy())
            print("red", blob.w(), blob.h())

        if blob.code() == 2:        #green
            img.draw_rectangle(blob.rect(), color=(0, 250, 0))
            img.draw_cross(blob.cx(), blob.cy())
            print("green", blob.w(), blob.h())

        if blob.code() == 4:        #blue
            img.draw_rectangle(blob.rect(), color=(0, 0, 250))
            img.draw_cross(blob.cx(), blob.cy())
            print("blue", blob.w(), blob.h())


        if blob.code() == 8:         #yellow
            img.draw_rectangle(blob.rect(), color=(100, 100, 0))
            img.draw_cross(blob.cx(), blob.cy())
            print("yellow", blob.w(), blob.h())
