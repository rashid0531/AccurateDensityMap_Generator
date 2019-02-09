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
import argparse

def CountFrequency(arr):

    freq = collections.Counter(arr)
    return freq	 

def make_histogram_multipledataSet(array_of_dataset, number_of_bin):

    colors = ["red","blue","green","yellow","gray","orange","purple","red","blue","green"]

    for i in range(0,len(array_of_dataset)):
        plt.hist(array_of_dataset[i], number_of_bin, facecolor=colors[i], alpha=0.5)
        plt.show()


def get_all_coordinates(inputpath):

    """
    Reads each line from coordinate.txt file and saves into a list.
    input: the input path of the coordinate.txt file.
    output: a list which contains each line from the coordinate.txt file as a string.
    """
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

def convert_string_dict_to_python_dict(all_coordinates):
    """
    Converts each json string from a .txt file to a python dictionary.
    input: an array of strings where each string represents each line from the coordinate.txt file.
    output: a python dictionary which contains each image name as key and the flower counts as value.
    """
    flower_counts = []

    for each in all_coordinates:

        # Converting String dictionary to python dictionary
        d = ast.literal_eval(each)
        img_name = d['image_name']        
        flower_counts.append(len(d['coordinates']))
        
        # Enable the following if block to check images which have more than 50 flowers.
        # Useful to check the truthfulness of manually annotated dataset.
        """
        if len(d['coordinates']) >= 50:
 
            print(img_name,len(d['coordinates']))
        """
    return flower_counts


if __name__ == "__main__":

    DEFAULT_COORDINATE_PATH_MANUAL = "/u1/rashid/FlowerCounter_Dataset_GroundTruth/coordinates/manual/1109-0704"
    DEFAULT_COORDINATE_PATH_AUTOMATIC = "/u1/rashid/FlowerCounter_Dataset_GroundTruth/coordinates/xavier/1109-0704"
    ap = argparse.ArgumentParser(description="Script to demonstrate statistics of manually or automatically annotated dataset.")

    ap.add_argument("-im", "--input_path_manual", required=False, help="Input path of the coordinate file which is manually annotated",default = DEFAULT_COORDINATE_PATH_MANUAL)
    ap.add_argument("-ia", "--input_path_auto", required=False, help="Input path of the coordinate file which is automatically annotated",default = DEFAULT_COORDINATE_PATH_AUTOMATIC)
    ap.add_argument("-show_which", "--which_one_to_show", required=False, help="Input path of the images",default = "compare_man_auto")

    args = vars(ap.parse_args())

    # Assuming the path exists.
    resulting_img_save_path = "/u1/rashid/Annotated_images_manual/visualization/graphs/dataset"

    if args['which_one_to_show'] == "manual":

        all_coordinates = get_all_coordinates(args['input_path_manual'])

        flower_counts = convert_string_dict_to_python_dict(all_coordinates)
        frequency = CountFrequency(flower_counts)

        print(frequency)

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
        plt.bar(x_pos, count_frequency, log=True, align='center', alpha=0.5)

        for a, b in zip(x_pos, count_frequency):
            plt.text(a, b, str(b), ha='center', fontsize=9)

        plt.xlabel('Flower Counts', size=13)
        plt.ylabel('Frequency', size=13)

        title_str = "Bar Graph of Camera Day: {} (Manual Annotation)".format(args['input_path_manual'].split('/')[-1])
        plt.title(title_str)

        fig_name = "Camera_Day:{}(Manual Annotation).eps".format(args['input_path_manual'].split('/')[-1])
        plt.savefig(resulting_img_save_path + "/" + fig_name, format='eps', dpi=500)
        plt.show()

    elif args['which_one_to_show'] == "automatic":

        all_coordinates = get_all_coordinates(args['input_path_auto'])

        flower_counts = convert_string_dict_to_python_dict(all_coordinates)

        number_of_bin = 5
        colors = ["red", "blue", "green", "yellow", "gray", "orange", "purple", "red", "blue", "green"]

        plt.xlabel('Flower Counts', size=13)
        plt.ylabel('Frequency', size=13)

        title_str = "Histogram of Camera Day: {} (Automatic Annotation)".format(args['input_path_auto'].split('/')[-1])
        plt.title(title_str)

        fig_name = "Camera_Day:{}(Automatic Annotation).eps".format(args['input_path_auto'].split('/')[-1])

        plt.hist(flower_counts, number_of_bin, facecolor=colors[4], alpha=0.5)

        plt.savefig(resulting_img_save_path + "/" + fig_name, format='eps', dpi=500)
        plt.show()

    elif args['which_one_to_show'] == "compare_man_auto":

        all_coordinates_manual = get_all_coordinates(args['input_path_manual'])

        flower_counts_manual = convert_string_dict_to_python_dict(all_coordinates_manual)

        all_coordinates_auto = get_all_coordinates(args['input_path_auto'])

        flower_counts_auto = convert_string_dict_to_python_dict(all_coordinates_auto)

        Flower_counts_manual_auto_for_sidebyside_comparison = []

        Flower_counts_manual_auto_for_sidebyside_comparison.append(flower_counts_auto)
        Flower_counts_manual_auto_for_sidebyside_comparison.append(flower_counts_manual)

        fig = plt.figure(1)
        fig.set_facecolor('white')
        camera_id, day = args['input_path_manual'].split('/')[-1].split('-')
        plot_title = "Box Plots: Camera ID : {}, Day : {}.".format(camera_id, day)
        plt.title(plot_title, size=11)
        plt.boxplot(Flower_counts_manual_auto_for_sidebyside_comparison)

        # plt.yscale('log',basey=2, nonposy='clip')

        plt.xticks([1, 2], [args['input_path_manual'].split('/')[-1] + " (Automatic)", args['input_path_manual'].split('/')[-1] + " (Manual)"])

        plt.ylabel('Flower Counts', size=13)

        fig_name = "comparison_boxplot_{}.eps".format(args['input_path_manual'].split('/')[-1])
        plt.savefig(resulting_img_save_path + "/" + fig_name, format='eps', dpi=500)
        plt.show()


