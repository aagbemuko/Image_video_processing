# computer vision (CV2) is adopted here being an advanced image processing package
import cv2 as cv
import os
from sys import stdout
from time import sleep
from pathlib import Path
from usrinputsvalidation import yes_no
from math import prod, ceil


def welcome_msg():
    """
    Prints welcome message and instructions
    """
    dashed_line = '-'*120
    print("Image processing program with several high-level functionalities")
    print(dashed_line + '\n')
    print("Important Note: when typing file paths it is encouraged to use '/' irrespective of OS.")
    print(dashed_line + '\n')
    print("The menu options are: ")
    print("\t1. Image resize")
    print("\t\ta. Resize image(s) based on percentage of the original (default).")
    print("\t\tb. Resize image(s) based on specific dimensions.")


def list_all_supported_img_files(src_dir, supported_img_formats):
    """
    Function lists all supported image formats in the validated
    source directory path.
    """

    # convert image formats to globs
    img_formats_as_globs = tuple(
        '*.' + img_format for img_format in supported_img_formats)

    # list all file types in source directory that matches the supported file types.
    path_obj_file_list = []

    for file_type in img_formats_as_globs:
        path_obj_file_list.extend(Path(src_dir).glob(file_type))

    # convert path objects to string as required by openCV
    matching_file_list = [str(path_obj) for path_obj in path_obj_file_list]

    return matching_file_list


def resize_images(path_list, des_dir, supported_img_formats, usr_option):
    """
    Function to resize images given the list of objects in the path, the supported image
    formats, and user selected option.
    """

    # ask user if they'd like to resize images to a different format from source image
    change_src_img_format = yes_no(
        "Save resized image files in a different format from original?")

    # if previous statement is true ask for the new format to save images:
    if change_src_img_format:
        new_format = new_img_format(supported_img_formats)

    if usr_option == '1a':
        # ask user for the percentage change if this option is selected
        prompt = "Enter the desired percentage change"
        percent_red = usr_desired_specs(prompt, type_of_change="percentage")
        percent_red = percent_red/100  # percent change in per units
    elif usr_option == '1b':
        # ask user for desired dimensions if this option is selected
        prompt = "Enter the desired dimensions as indicated"
        desired_dimensions = usr_desired_specs(prompt, type_of_change="fixed")

    # loop preamble
    process_counter = 0
    percent_complete = 0
    nr_of_img_files = len(path_list)

    # loop over all images in the list
    for img_path in path_list:
        img = cv.imread(img_path, 1)

        # if it is true that the user desires a different format and current format
        # is not the same as the new format, then the code snippet below is executed.
        if change_src_img_format and os.path.splitext(img_path)[1] != '.' + new_format:
            img_path = f"{os.path.splitext(img_path)[0]}.{new_format}"
        img_name = 're_' + os.path.split(img_path)[1]
        img_path = os.path.join(des_dir, img_name)
        pixel_size = img.size/1e6  # pixel size in mega pixels

        if usr_option == '1a':
            desired_height = ceil(percent_red*img.shape[0])
            desired_width = ceil(percent_red*img.shape[1])
            desired_dimensions = (desired_width, desired_height)

            # only execute resize if images are larger than 3 MP. Pixel size < 3 MP
            # suggests an already small image. TO DO: revise this to allow user decide.
            if pixel_size > 3.0:
                # x--> width, y--> height
                resized_img = cv.resize(img, desired_dimensions)

                # save image in path
                cv.imwrite(img_path, resized_img)

                process_counter += 1  # count resized images
        elif usr_option == '1b':
            # desired size in mega pixels
            desired_pixel_size = prod(desired_dimensions)/1e6

            # only execute resize if images are larger than the desired dimensions
            if pixel_size > desired_pixel_size:
                # x--> width, y--> height
                resized_img = cv.resize(img, desired_dimensions)

                # save image in image path
                cv.imwrite(img_path, resized_img)

                process_counter += 1  # count resized images

        percent_complete += 100 / nr_of_img_files
        stdout.write("\r%d%% complete" % percent_complete)
        stdout.flush()
        sleep(0.02)
    print(f"\nImage resize complete. Check the path {des_dir}")
    print(
        f"Total unique image files resized: {process_counter}/{nr_of_img_files}")


def usr_desired_specs(prompt, type_of_change=None):
    """
    Sub-function (a function designed to be called by another larger function) that allows
    the user to enter the desired dimensions for the resized images.
    """

    input_ok = False
    while not input_ok:
        if type_of_change == 'percentage':
            desired_specs = input(prompt + ": ")
            try:
                if not desired_specs.isnumeric():
                    raise Exception(
                        "Only positive integer values are allowed. Please enter a valid number.")
            except Exception as err_msg:
                print(err_msg)
            else:
                desired_specs = int(desired_specs)
                input_ok = True
        elif type_of_change == 'fixed':
            width = input(prompt + "(width): ")
            height = input(prompt + "(height): ")
            dimensions_ok = width.isnumeric() and height.isnumeric()
            try:
                if not dimensions_ok:
                    raise Exception(
                        "Only positive integer values are allowed for the width and height. Please enter valid integers")
            except Exception as err_msg:
                print(err_msg)
            else:
                desired_specs = (int(width), int(height))
                input_ok = True
        elif type_of_change is None:
            desired_specs = 50  # default is set to the percentage method with 50% change
            input_ok = True
        else:
            print("Invalid resize type. Please enter a valid type.")
    return desired_specs


def new_img_format(supported_img_formats):
    """
    Function that allows the user to input a format they'd like to have their
    images saved in, if desired.
    """
    input_ok = False

    while not input_ok:
        usr_img_format = input(
            "Enter the desired file format to save resized images: ")

        if usr_img_format in supported_img_formats:
            input_ok = True
        else:
            print(
                "The entered image format is incorrectly entered or not currently supported.")
            print(f"Suppored image formats are {supported_img_formats}.")
            print("Enter a supported format (without the quotes).")

    return usr_img_format
