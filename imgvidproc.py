# computer vision (CV2) is adopted here being an advanced image processing package
import cv2 as cv
import os
from sys import stdout
from time import sleep
from pathlib import Path
from send2trash import send2trash


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
    print("\t\ta. Resize in the same image format as source file, e.g. jpg->jpg (default).")
    print("\t\tb. Resize to a different image format from source file, e.g. jpg->png.")


def list_all_supported_img_files(src_dir, supported_file_types=('*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.bmp')):
    """
    Function lists all supported image formats in the validated source directory path.

    """

    # list all file types in source directory that matches the supported file types.
    path_obj_file_list = []

    for file_type in supported_file_types:
        path_obj_file_list.extend(Path(src_dir).glob(file_type))

    # convert path objects to string as required by openCV
    matching_file_list = [str(path_obj) for path_obj in path_obj_file_list]

    return matching_file_list


def resize_images(img_path_list, des_dir, percent_red=50):
    """
    Function takes in the the list of full path to all image files, 
    the destination directory, and the percentage reduction desired.
    A default of 50% reduction is set.

    Note that the percentage reduction applies a proportional scaling. That is,
    both width and height are scaled equally.
    """

    if not img_path_list:  # if there are no image files in the list return to main
        print("There are no image files or supported image files in the source directory.")
        return

    # loop over all images in the list
    percent_red = percent_red/100  # percent reduction in per units
    for img_path in img_path_list:
        img = cv.imread(img_path, 1)
        img_name = 're_' + os.path.split(img_path)[1]
        img_path = os.path.join(des_dir, img_name)

        # only execute resize if images are larger than 3 MP. Pixel size < 3 MP suggests
        #  an already small image.
        pixel_size = img.size/1e6  # pixel size in mega pixels
        if pixel_size > 3.0:
            # x--> width, y--> height
            resized_img = cv.resize(
                img, None, fx=percent_red, fy=percent_red)

            # save image in image path
            cv.imwrite(img_path, resized_img)
