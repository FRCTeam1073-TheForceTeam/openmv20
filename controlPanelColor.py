import sensor, image, time, math

thresh = [(45, 70, 65, 90, 45, 75),       #red
          (45, 80, -78, -40, 25, 55),     #green
          (40, 75, -26, 5, -65, -35),     #blue
          (75, 99, -28, -3, 75, 99)]      #yellow

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
        print("red", blob.cx(), blob.cy())

    if blob.code() == 2:        #green
        img.draw_rectangle(blob.rect(), color=(0, 250, 0))
        img.draw_cross(blob.cx(), blob.cy())
        print("green", blob.cx(), blob.cy())

    if blob.code() == 4:        #blue
        img.draw_rectangle(blob.rect(), color=(0, 0, 250))
        img.draw_cross(blob.cx(), blob.cy())
        print("blue", blob.cx(), blob.cy())

    if blob.code() == 8:         #yellow
        img.draw_rectangle(blob.rect(), color=(100, 100, 0))
        img.draw_cross(blob.cx(), blob.cy())
        print("yellow", blob.cx(), blob.cy())


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

def findPercentLocation(blob):
    position = (blob.cx()/img.width()) * 100.0
    return position


while(True):
    print("///////")
    clock.tick()
    img = sensor.snapshot().gamma_corr(gamma = 0.7, contrast = 1.6, brightness = 0.3)
    blobs = img.find_blobs(thresh, pixels_threshold=700, area_threshold=700)
    bubbleSort(blobs, compareBlobs)

    for blob in blobs:
        findColors(blob)
        findPercentLocation(blob)

