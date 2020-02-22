# Untitled - By: katherine - Sat Feb 22 2020

import sensor, image, time, image

def list_creator(path):
    frame_list=[]
    video = image.ImageReader(path);
    while(video.next_frame([copy_to_fb=True[, loop=False]]) != None):
       frame_list.append(video.next_frame([copy_to_fb=True[, loop=False]]))

list_creator('Week0Videos/GOODMatch0.mjpeg')

