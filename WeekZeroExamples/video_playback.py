# Untitled - By: katherine - Sat Feb 22 2020
import sensor, image, time
def frame_count(path):
    frame_number = 0
    video = image.ImageReader(path)
    while(video.next_frame(copy_to_fb=True, loop=True) != None):
        frame_number = frame_number+1
    return frame_number


print(frame_count("WeekZeroVideos/testFile.bin"))
#path must be a .bin file. I couldn't push any through github
#because of their size, but there is a conversion if you click the
# tools > Video tools tab on the tool bar. Make sure you choose a
# ImageReader file to convert the mjpeg to (The default option is mp4)
