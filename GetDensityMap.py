import glob
import os
import ast
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import skimage.io as io
import matplotlib.pyplot as plt

def createDensityMap(shape,name, points):

    # creates an array of only zero values based on the shape of given array.
    dens_map = np.zeros(shape=[shape[0], shape[1]])

    # Take each coordinates from the list "points" and put 255 on that position.
    for point in points:
        dens_map[point[1]][point[0]] = 255

    # Normalizing the array so that the sum over the whole array equals to the number of elements in the list "points".

    if ((np.max(dens_map) - np.min(dens_map)) == 0):
        normalized = (dens_map - np.min(dens_map))
    else :
        normalized = (dens_map - np.min(dens_map)) / (np.max(dens_map) - np.min(dens_map))

    # Changed the sigmoid following the advice from microscopic cell image.
    sigmadots = 7
    dot_anno = gaussian_filter(normalized, sigmadots)

    # Following the advice from microscopic cell image.
    dot_anno.astype(np.float32)

    return dot_anno

def get_all_coordinates(inputpath):

    all_coordintes = []

    for coordinate_file in glob.glob(inputpath + "/*"):

        if coordinate_file.split("/")[-1] == "coordinates.txt": 

            try:
                with open(coordinate_file, 'r') as file_obj:
                    file_contents = file_obj.readlines()

                    for each_line in file_contents:
                        each_line = each_line.strip()
                        all_coordintes.append(each_line)

            except FileNotFoundError:
                msg = each_folder + " does not exist."
                print(msg)

    return all_coordintes


if __name__== '__main__':


    gt_coordinate_path = "/u1/rashid/FlowerCounter_Dataset_GroundTruth/coordinates/manual/1109-0704"

    gt_numpy_save_path = "/u1/rashid/FlowerCounter_Dataset_GroundTruth/density_map/manual/1109-0704"

    if not os.path.exists(gt_numpy_save_path):
        os.makedirs(gt_numpy_save_path)

    all_coordinates = get_all_coordinates(gt_coordinate_path)

    #print(all_coordinates[0])
    tmp = []

    for each in all_coordinates:

        shape = [224,224]

        # Converting String dictionary to python dictionary
        d = ast.literal_eval(each)
        img_name = d['image_name']        

        gt_arr_name = img_name.split("/")[-1]
        gt_arr_name = gt_arr_name.split(".")[0]

        arr = createDensityMap(shape=shape,name=img_name,points = d['coordinates'])

        output_np_path = gt_numpy_save_path + "/" + gt_arr_name

        print(output_np_path)

        """
        if not os.path.exists(output_np_path):
            os.makedirs(output_np_path)
        """

        np.save(output_np_path, arr)
        
