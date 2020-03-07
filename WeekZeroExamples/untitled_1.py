# Untitled - By: katherine - Sat Feb 22 2020
import sensor, image, time
def file_reader(path):
    frame_number = 0
    video = image.ImageReader(path)
    while(video.next_frame(copy_to_fb = False, loop = False)):



file_reader("WeekZeroVideos/testFile.bin")
