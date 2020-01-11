import sensor, image, time, math

thresh = (45, 100, -15, 5, 40, 60)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()


while(True):
    img = sensor.snapshot()
    for blob in img.find_blobs(thresh, pixels_threshold=350, area_threshold=400):
        if blob.elongation() < 0.5:
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)