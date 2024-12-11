# Author: Daniel Glauber
# File: settings_loader.py
# Description: This file contains the settings loader for the simple genetic algorithm (SGA).
import re
from os.path import exists
from typing import Any, List

# Constants
SETTINGS_THAT_MUST_BE_ONE_OR_LESS = [
    "probApplyCrossover",
    "probApplyMutation",
]
SETTINGS_THAT_MUST_BE_TWO_OR_MORE = [
    "populationSizeN"
]
DEFAULT_SETTINGS_FILE = "gasettings.dat"
DEFAULT_SETTINGS = {
    "randSeed": 123,
    "populationSizeN": 100,
    "stringSizen": 50,
    "probApplyCrossover": 0.6,
    "probApplyMutation": 1.0,
    "selectionMethod": 0,
    "tournamentSizek": 2,
    "fitnessFunction": 0,
    "terminateOnFailure": 1,
    "failuresBeforeTermination": 0
}

ga_settings = {}
user_settings_file = DEFAULT_SETTINGS_FILE

def display_help_message() -> None:
    """
    Display the help message for running the SGA program.
    """
    print("Simple GA Help Message")
    print("The command to run program is: python3 sga.py settings.dat")
    print("settings.dat is an optional argument to specify a custom settings file.")
    print("If you do not include a settings file the default settings file gasettings.dat is used.")
    print("To turn on limited debugging use command: python3 sga.py -g settings.dat")
    print("To turn on full debugging use command: python3 sga.py -G settings.dat")

def get_setting(key: str) -> Any:
    """
    Retrieve a setting value by key.
    
    Args:
        key (str): The key of the setting to retrieve.
    
    Returns:
        Any: The value of the setting.
    """
    return ga_settings[key]

def ask_user_continue_question(question: str, default: str = "y") -> None:
    """
    Ask the user a yes/no question to continue.
    
    Args:
        question (str): The question to ask the user.
        default (str): The default answer if the user presses enter.
    """
    user_response = input(f"{question}\n(default={default}) (y/n): ")
    try:
        if user_response.lower() not in ["", "y", "yes"]:
            quit()
    except Exception as e:
        print(f"An error occurred: {e}")
        quit()

def create_default_settings_file() -> None:
    """
    Create the default settings file with predefined values.
    """
    try:
        lines = [f"{key} {value}" for key, value in DEFAULT_SETTINGS.items()]
        with open(DEFAULT_SETTINGS_FILE, "w") as file:
            file.write('\n'.join(lines))
    except (IOError, OSError) as e:
        print(f"An error occurred while creating the default settings file: {e}")

def parse_settings_file(settings_file: str) -> None:
    """
    Parse the settings file and load the settings into the global ga_settings dictionary.
    
    Args:
        settings_file (str): The path to the settings file.
    """
    global ga_settings
    default_settings_needs_fix = False
    is_default_file = settings_file == DEFAULT_SETTINGS_FILE
    finished_parsing = False
    saved_ga_settings = ga_settings.copy()  # Save current settings in case we need to revert
    while_count = 0
    while not finished_parsing:
        if default_settings_needs_fix:
            ga_settings = saved_ga_settings  # Revert to saved settings if default needs fixing
            create_default_settings_file()  # Create default settings file
            default_settings_needs_fix = False

        if while_count > 3:  # Prevent infinite loop by limiting retries
            break
        try:
            with open(settings_file) as file:
                for line in file:
                    split_line = re.split(r'\s+', line)
                    if len(split_line) > 1:
                        error_reason = ""
                        try:
                            if split_line[0] in SETTINGS_THAT_MUST_BE_ONE_OR_LESS:
                                error_reason = "a decimal number that is less than or equal 1.0"
                                float_value = float(split_line[1])
                                if float_value > 1.0:
                                    raise ValueError("Value cannot be greater than 1.0")
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = float_value
                            elif split_line[0] in SETTINGS_THAT_MUST_BE_TWO_OR_MORE:
                                error_reason = "an integer that is greater than or equal 2"
                                integer = int(split_line[1])
                                if integer < 2:
                                    raise ValueError("Value cannot be less than 2")
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = integer
                            else:
                                error_reason = "an integer"
                                integer = int(split_line[1])
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = integer
                        except ValueError as ve:
                            if not is_default_file:
                                print(f"Error parsing settings file {settings_file}")
                                print(f"The value for {split_line[0]} must be {error_reason}")
                                user_question = (f"Do you want to continue with the default value for {split_line[0]} from {DEFAULT_SETTINGS_FILE}?")
                                ask_user_continue_question(user_question)  # Ask user if they want to continue with default value
                                finished_parsing = True
                            else:
                                default_settings_needs_fix = True  # Flag to fix default settings
                                break
        except FileNotFoundError:
            print(f"Settings file {settings_file} not found.")
            if is_default_file:
                create_default_settings_file()  # Create default settings file if not found
            else:
                user_question = (f"Do you want to use the default settings from {DEFAULT_SETTINGS_FILE} instead?")
                ask_user_continue_question(user_question)  # Ask user if they want to use default settings
                finished_parsing = True
        except (IOError, OSError) as e:
            print(f"An error occurred while parsing the settings file: {e}")
            finished_parsing = True
        if not default_settings_needs_fix:
            finished_parsing = True

def load_settings(argv: List[str]) -> None:
    """
    Load settings from the command line arguments and settings file.
    
    Args:
        argv (List[str]): The command line arguments.
    """
    global user_settings_file
    ga_settings["fullDebug"] = False
    ga_settings["limitedDebug"] = False
    if len(argv) > 1:
        if "-h" in argv:
            display_help_message()
            print("Stopped")
            quit()

        if "-g" in argv:
            ga_settings["limitedDebug"] = True
        if "-G" in argv:
            ga_settings["fullDebug"] = True

        if argv[-1] not in ["sga.py", "-h", "-g", "-G"]:
            user_settings_file = argv[-1]
    if not exists(DEFAULT_SETTINGS_FILE):
        create_default_settings_file()
    if user_settings_file != DEFAULT_SETTINGS_FILE:
        if exists(user_settings_file):
            parse_settings_file(user_settings_file)
        else:
            print(f"Could not find settings file {user_settings_file}")
            user_question = (f"Do you want to use the default settings from {DEFAULT_SETTINGS_FILE} instead?")
            ask_user_continue_question(user_question)
    parse_settings_file(DEFAULT_SETTINGS_FILE)
