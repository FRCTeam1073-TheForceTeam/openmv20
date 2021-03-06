# Multi Color Blob Tracking Example
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math

thresholds = []
groundROIs = []
searchROIs = []
numRegions = 8


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()


regionW = int(sensor.width() / numRegions)
print(regionW)
for i in range(0, numRegions):
    roi = (i*regionW, sensor.height()-10, regionW, 10)
    groundROIs.append(roi)
    roi = (i*regionW, 0, regionW, sensor.height() - 10)
    searchROIs.append(roi)
    thresholds.append((0, 100, -50, 0, -50, 50))
    print(groundROIs)
    print(searchROIs)
    print(thresholds)

while(True):
    img = sensor.snapshot()
    for r in range(0, numRegions):
        stats = img.get_statistics(roi=groundROIs[r])
        thresh = (stats.l_min(), stats.l_max(), stats.a_min(), stats.a_max(), stats.b_min(), stats.b_max())
        thresholds[r] = thresh
        blobs = img.find_blobs([thresholds[r]], roi=searchROIs[r], area_threshold=10, merge=True)
        regionH = 999
        for b in blobs:
            if b.y() < regionH:
                regionH = b.y()
        if regionH != 999:
            img.draw_line(searchROIs[r][0], regionH, searchROIs[r][0]+regionW, regionH, color=(90, 90, 0))
