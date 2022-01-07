# Main calling file to automatically process images with python
import imgvidproc as imgproc
import usrinputsvalidation as usrip
import directoryinput as dirip

# Welcome message
imgproc.welcome_msg()


# Menu options: These options can be updated in later revision
menu_options = {'1a': ('1', '1a', 'a1'),
                '1b': ('1b', 'b1')}


# Supported image formats
supported_img_formats = ('jpg', 'JPG',
                         'jpeg', 'JPEG',
                         'png', 'PNG')


# Menu option mapping
usr_option = usrip.menu_mapping(menu_options)


# User input to source folder location, validation, and check of directory existence
src_dir = dirip.compliant_usr_dir('src')

src_and_des_dir_are_equivalent = usrip.yes_no(
    "Source and destination directory are the same?")

if src_and_des_dir_are_equivalent:
    des_dir = src_dir
else:
    des_dir = dirip.compliant_usr_dir('des')


# List all image files in source directory
all_img_files = imgproc.list_all_supported_img_files(
    src_dir, supported_img_formats)


# Call to resize images
imgproc.resize_images(all_img_files, des_dir,
                      supported_img_formats, usr_option)
