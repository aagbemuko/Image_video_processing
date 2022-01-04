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


def list_all_supported_img_files(src_dir, supported_file_types=('*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG')):
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

    # if there are no matching files in the list, return to main and print "no image file in source directory"
