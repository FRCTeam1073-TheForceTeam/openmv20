# Untitled - By: katherine - Sat Feb 22 2020
import sensor, image, time
def list_creator(path):
    frame_list=[]
    video = image.ImageReader(path);
    while(video.next_frame(copy_to_fb=False, loop=False) != None):
        frame_list.append(video.next_frame())
    return frame_list

images = list_creator('/Users/katherine/Documents/GitHub/openmv20/WeekZeroExamples/Week0Videos/GOODMatch0.mjpeg')
print("images saved!")
