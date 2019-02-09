"""
Author : Mohammed Rashid Chowdhury.

Given a directory containing the ground truth coordinate.txt file, this script creates the visualization to demonstrate the statistics of the ground truth. (e.g, Box plot, Histogram etc.)

Use case: python show_stats_of_dataset_manual.py
"""

import glob
import matplotlib.pyplot as plt
import ast
import numpy as np
import collections

def CountFrequency(arr):

    freq = collections.Counter(arr)
    return freq	 

def make_histogram_multipledataSet(array_of_dataset, number_of_bin):

    colors = ["red","blue","green","yellow","gray","orange","purple","red","blue","green"]

    for i in range(0,len(array_of_dataset)):
        plt.hist(array_of_dataset[i], number_of_bin, facecolor=colors[i], alpha=0.5)
        plt.show()


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


if __name__ == "__main__":

    input_path = "/u1/rashid/FlowerCounter_Dataset_GroundTruth/coordinates/manual/1109-0704"

    all_coordinates = get_all_coordinates(input_path)

    flower_counts = []

    for each in all_coordinates:

        # Converting String dictionary to python dictionary
        d = ast.literal_eval(each)
        img_name = d['image_name']        
        flower_counts.append(len(d['coordinates']))
        if len(d['coordinates']) >= 50:
 
            print(img_name,len(d['coordinates']))
    
    frequency = CountFrequency(flower_counts)
    print(frequency)

    resulting_img_save_path = "/u1/rashid/Annotated_images_manual/visualization/graphs/dataset"
    flower_counts = []
    count_frequency = []

    for key, value in frequency.items():
        flower_counts.append(key)
        count_frequency.append(value)

    x_pos = np.arange(len(flower_counts))
    
    # Get or set the current tick locations and labels of the x-axis.
    fig = plt.figure(figsize=(15, 6))
    fig.set_facecolor('white')
    plt.xticks(x_pos, flower_counts)
    plt.bar(x_pos, count_frequency, log = True, align='center', alpha=0.5)

    for a,b in zip(x_pos, count_frequency):
        plt.text(a, b, str(b), ha = 'center', fontsize= 9)


    plt.xlabel('Flower Counts', size=13)
    plt.ylabel('Frequency', size=13) 

    title_str = "Bar Graph of Camera Day: {} (Manual Annotation)".format(str("1109-0704"))
    plt.title(title_str)

    fig_name = "Camera_Day:{}(Manual Annotation).eps".format(str("1109-0704"))
    plt.savefig(resulting_img_save_path + "/" + fig_name, format='eps', dpi=500)
    plt.show()

