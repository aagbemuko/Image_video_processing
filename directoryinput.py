# Specialized module of generic functions for user input of source/destination directories and subsequent
# validation for compliance. This module is expected to be used by other modules requiring such specialized functions.
# (c) 2022 Adedotun Agbemuko

from pathlib import Path

# Function definitions


def dir_exists(dir_type, raw_dir_path):
    """
    path_existence_flag = dir_exists(dir_type, raw_dir_path)

    Accepts the directory path and directory type and checks if a directory exist
    and returns a boolean True or False.

    Only two directory types are currently supported: source ('src') and
    destination ('des') directories.

    For source directories, if they do not exist, a return to the main calling function
    is made. For destination directories, if they don't exist, they are created.
    """

    if dir_type == "src":
        if Path(raw_dir_path).exists():
            dir_flag = True
        else:
            dir_flag = False
    elif dir_type == "des":
        if Path(raw_dir_path).exists():
            dir_flag = True
        else:
            dir_flag = False
    return dir_flag


def raw_usr_dir_input(dir_type):
    """
    input_validated_directory = usr_dir_input(dir_type)

    This function allows the user to enter the required paths based on their selected option
    and validates the raw input.

    Also this function allows to restrict the maximum number of wrong entries.
    """

    nr_of_wrong_tries = 0
    input_ok = False
    while not input_ok:
        try:
            if dir_type == "src":
                raw_dir_path = input(
                    "Type the full path to the source folder: ")
            elif dir_type == "des":
                raw_dir_path = input(
                    "Type the path (full, relative...) to the destination folder: ")

            if raw_dir_path.isnumeric():
                raise Exception("Please enter a valid file path")
            elif raw_dir_path.isspace() or raw_dir_path == "":
                raise Exception("Space or empty inputs not allowed!")
            elif ("/" not in raw_dir_path) and ("\\" not in raw_dir_path):
                raise Exception(
                    "Not a valid file path or recommended location. Input must include at least 1 '/' or '\\'!"
                )
            elif raw_dir_path in ("/", "\\"):
                raise Exception(f"'{raw_dir_path}' is not a valid file path")
        except Exception as err_msg:
            print(err_msg)
            nr_of_wrong_tries = +1
            if nr_of_wrong_tries > 4:
                print(
                    f"Number of reasonable tries ({nr_of_wrong_tries}) exceeded. Program is exiting...")
                return
        else:
            input_ok = True
    return raw_dir_path


def compliant_usr_dir(dir_type):
    """
    validated_path = compliant_usr_dir(dir_type)

    Function accepts the directory type as a string, which is passed on to the
    function that asks for user input to the specified path. This function then
    checks if the path exists. The output is a validated directory path.
    """

    if dir_type == 'src':
        path_exists = False

        while not path_exists:
            raw_dir_path = raw_usr_dir_input(dir_type)

            if dir_exists(dir_type, raw_dir_path):
                validated_dir = raw_dir_path
                print("Source directory exists!")
                path_exists = True
            else:
                print(
                    "The source directory does not exist on this computer.\nEnter a source path that exists.")
    elif dir_type == 'des':
        # this snippet ensures that the first 2 ancestors of destination directory exists, allowing any
        # following children to be created if desired.
        path_exists = False
        while not path_exists:
            raw_dir_path = raw_usr_dir_input(dir_type)
            if dir_exists(dir_type, raw_dir_path):
                validated_dir = raw_dir_path
                path_exists = True
            else:
                try:
                    first_2_ancestors = Path(
                        raw_dir_path).parts[0]+Path(raw_dir_path).parts[1]
                except IndexError:
                    print("Prohibited or non-existent location! Try again.")
                    continue
                else:
                    if dir_exists(dir_type, first_2_ancestors):
                        Path(raw_dir_path).mkdir(parents=True, exist_ok=True)
                        validated_dir = raw_dir_path
                        path_exists = True
                    else:
                        print(
                            "The destination directory does not exist AND cannot be created! \nEnter a valid destination path.")

    return validated_dir
