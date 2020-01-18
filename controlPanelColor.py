import sensor, image, time, math

thresh = [(45, 70, 65, 90, 45, 75),       #red
          (30, 80, -55, -30, 13, 35),     #green
          (40, 60, 10, 35, -80, -50),      #blue
          (55, 90, -25, 10, 55, 75)]      #yellow

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False)
sensor.set_saturation(2)
sensor.set_brightness(-1 )
clock = time.clock()


def findColors(blob):
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


def compareBlobs(blob1, blob2):
    if blob1.cx() > blob2.cx():
        return True
    else:
        return False


def bubbleSort(blobs, compare):
    n = len(blobs)
    for i in range(n):
        for j in range (0, n-i-1):
            if compare(blobs[j], blobs[j+1]):
                blobs[j], blobs[j+1] = blobs[j+1], blobs[j]

def orderChooser(blobs, compare)
    if blobs[0].code() == 1:    #red
        print("order = RYBG")

    if blobs[1].code() == 2:    #green
        print("order = GRYB")

    if blobs[2].code() == 4:    #blue
        print("order = BGRY")

    if blobs[3].code() == 8:    #yellow
        print("order = YBGR")



while(True):
    print("///////")
    clock.tick()
    img = sensor.snapshot().gamma_corr(gamma = 0.6, contrast = 1.6, brightness = 0.2)
    blobs = img.find_blobs(thresh, pixels_threshold=700, area_threshold=700)
    bubbleSort(blobs, compareBlobs)

    for blob in blobs:
        findColors(blob)
        orderChooser(blobs) #maybe wrong idk

