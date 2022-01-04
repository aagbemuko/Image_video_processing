# Specialized module of generic functions to deal with user inputs and
# corresponding validations for use in other modules.


def yes_no(prompt):
    """
    flag = yes_no(prompt)

    A generic function that allows to enter and validate yes/no inout entries.
    The output is a boolean True or False for Yes or No  respectively.

    'prompt' is the informatic text to display why the user should enter yes/no.
    """

    input_ok = False
    while not input_ok:
        usr_response = input(prompt + ": ")
        if usr_response in ('Y', 'YES', 'Yes', 'y'):
            flag = True
            input_ok = True
        elif usr_response in ('N', 'NO', 'No', 'n'):
            flag = False
            input_ok = True
        else:
            print("Please enter 'Y' or 'N'.")
    return flag


def _usr_menu_validation(usr_def_menu_opts, len_dashed_line=85):
    """
    usr_input = usr_menu_validation(usr_def_menu_opts, len_dashed_line=85)

    Function takes in the desired menu options as a tuple, and optionally the length
    of dashed line and validates actual user input against the tuple of options for 
    compliance. If actual user input is not compliant, user is asked for
    the correct inputs repeatedly until the correct one is entered.

    The output is the validated user input
    """

    formatted_line = "-"*len_dashed_line
    print(formatted_line)

    # Input and validation
    input_ok = False
    while not input_ok:
        usr_input = input("Enter the menu option of choice as instructed: ")
        if usr_input in usr_def_menu_opts:
            input_ok = True
        else:
            print("Invalid selection. Menu selection must be as instructed.")
    print(formatted_line)

    return usr_input


def menu_mapping(menu_opts):
    """
    usr_option = usr_sel_mapping(menu_opts)

    'menu_opts' is a dictionary in the form {key1: (possible_opts_that_map_to_key), key2:...}
    e.g. {'1a': ('1', '1a', 'a1')}. Thus any user input in ('1', '1a', 'a1') as a choice of options
    will map to '1a'.

    Therefore this is a function that maps user inputs to one specific unique key for internal use
    """

    # unpack dictionary values into one tuple that combines all possible inputs.
    # Note: this could also be a list, but an immutable structure is desired here.

    all_menu_opts = tuple(valid_input_opt for _, uniq_opts in menu_opts.items()
                          for valid_input_opt in uniq_opts)

    # get validated user input for choice of menu
    usr_input = _usr_menu_validation(all_menu_opts)

    # mapping of options
    for key, opts in menu_opts.items():
        if usr_input in opts:
            usr_option = key
    return usr_option
