"""
Original Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO
@author: Guanghan Ning
modified by: Chris Ros, Nektarios Evangelou
"""

import os
import time
from os import walk, getcwd
from PIL import Image

classes = []

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


"""-------------------------------------------------------------------"""

""" Configure Paths """
mypath = "Labels/002/"
outpath = "Labels/converted/{}/".format(int(time.time()))
class_loc = "class.txt"
images_path = 'Images/002/%s.JPG'
os.makedirs(outpath)

""" Load classes """
with open(class_loc) as classes_f:
    for c in classes_f:
        classes.append(c.replace('\n', ''))
    print("Loaded classes: ", classes)
list_file = open('list.txt', 'w+')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")

    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\n')   #for ubuntu, use "\r\n" instead of "\n"

    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")


    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        if(len(line) >= 2):
            ct = ct + 1
            print(line + "\n")
            elems = line.split(' ')
            print(elems)
            xmin = elems[0]
            xmax = elems[2]
            ymin = elems[1]
            ymax = elems[3]
            cls = elems[4]
            img_path = str(images_path % (os.path.splitext(txt_name)[0]))
            im=Image.open(img_path)
            w = int(im.size[0])
            h = int(im.size[1])
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            cls_id = classes.index(cls)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('Images/%s.JPG\n'%(os.path.splitext(txt_name)[0]))

list_file.close()
