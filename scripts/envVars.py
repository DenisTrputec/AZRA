import os
from pathlib import Path
from PyQt5 import uic


def __path(path: str):
    """
    Join main.py absolute path and variable string
    :param path: string
    :return: string
    """
    return os.path.join(os.getcwd(), path)


def __create_path(path: str):
    """
    Create folder if not exists
    :param path: string (absolute path)
    :return: None
    """
    if not os.path.exists(path):
        Path(path).mkdir(parents=True, exist_ok=True)


# Current user
USERNAME = os.getlogin()

# Passwords
ADMIN_PASSWORD = "FakePassAdmin".encode()
PASSWORD = "FakePassUser".encode()

# Filepaths
INPUT_FOLDER = f"C:/Users/{USERNAME}/Documents/AZRA/Input"
OUTPUT_FOLDER = f"C:/Users/{USERNAME}/Documents/AZRA/Output"
OUTPUT_FILE = "Output_file.xlsx"
LOG_FOLDER = __path("log_files")
INFO_FILE = __path("resources/txt_files/info.txt")
HELP_FILE = __path("resources/txt_files/help.txt")
WEIGHT_FACTORS_FOLDER = __path("resources/weight_factors")
WEIGHT_FACTORS_FILEPATH = __path("resources/weight_factors/weight_factors_encrypted")

# Create paths
__create_path(INPUT_FOLDER)
__create_path(OUTPUT_FOLDER)
__create_path(LOG_FOLDER)

# Load ui files
formMainWindow, baseMainWindow = uic.loadUiType(__path("resources/ui/main.ui"))
formWeightFactorsWindow, baseWeightFactorsWindow = uic.loadUiType(__path("resources/ui/weight_factors.ui"))
formWeightFactorsWindow2, baseWeightFactorsWindow2 = uic.loadUiType(__path("resources/ui/weight_factors2.ui"))
formLoginWindow, baseLoginWindow = uic.loadUiType(__path("resources/ui/login.ui"))
