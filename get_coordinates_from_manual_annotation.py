# Original Author: 
#  Kai Langen (getCoordinates() function) 
#  Mohammed Rashid Chowdhury (rests)

# Date: May 09, 2018

# Description: An script to find all of the 'red' annotation markers in
# the canola flower image
 
# Note: - If annotating with GIMP, ensure that the image is exported at
#         90%, otherwise the 'red' value may not fall within range.
#       
#       - Mask range can be adjusted to relax this requirement.
# 
#       - Assuming cross-shaped annotations 

import sys
import numpy as np
import cv2
import json
import argparse
import glob
import os


def createJSON(data):
    data_dict = {}
    data_dict['image_name'] = data[0]
    data_dict['coordinates'] = data[1]
    return data_dict


def getCoordinates(image):

    img = cv2.imread(image)

    kernel = np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]], np.uint8)

    flowers = []
    height, width, depth = img.shape
    assert(depth == 3)

    mask = cv2.inRange(img, (0,0,200), (100,100,255))

    #mask = cv2.inRange(img, (0,0,240), (0,0,255))
    erosion = cv2.erode(mask, kernel, iterations=1)

    for i in range(width):
        for j in range(height):
            if erosion[j,i]:
                flowers.append((i,j))
    if len(flowers) == 0:
        #print("Zero annotations of radius 2 detected... retrying for annotation radius of 1")
        for i in range(width):
            for j in range(height):
                if mask[j,i]:
                    flowers.append((i,j))

    return flowers



if __name__ == "__main__":

    DEFAULT_IMAGE_PATH = "/home/mrc689/Sampled_Dataset"
    DEFAULT_DEST_PATH = "/home/mrc689/Sampled_Dataset_GroundTruth"

    # Create arguements to parse
    ap = argparse.ArgumentParser(description="Script to cut and paste all the images from sub folders to the parent folder.")

    ap.add_argument("-i", "--image_path", required=False, help="Input path of the images",default = DEFAULT_IMAGE_PATH)
    ap.add_argument("-d", "--destination_path", required=False, help="Destination path of the images",default = DEFAULT_DEST_PATH)

    args = vars(ap.parse_args())

    # Array of dictionaries where each element represents a dictionary which stores each imagename with the corresponding flowers corordinates. 
    Flower_dictionaries = []

    # Will be used for creating the same named folder in destination directory.
    input_prefix = args["image_path"].split("/")[-1]

    #print(input_prefix)

    out_path = args["destination_path"]+"/"+input_prefix

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    print(out_path)

    for each_file in glob.glob(args["image_path"] + "/*"):

        flower_coordinates = getCoordinates(each_file)
        dict_towrite = {}
        dict_towrite['image_name'] = each_file
        dict_towrite['coordinates'] = flower_coordinates

        if(len(flower_coordinates) >= 5):
            print(each_file, len(flower_coordinates))

        Flower_dictionaries.append(dict_towrite)

    print(len(Flower_dictionaries))

    output_path = str(out_path + "/" + "coordinates.txt")

    with open(output_path,"w") as file_object:
        for i in range(0, len(Flower_dictionaries)):
            json_string = json.dumps(Flower_dictionaries[i])
            file_object.write(json_string+"\n")
             



