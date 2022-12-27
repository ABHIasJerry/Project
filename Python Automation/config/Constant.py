###################################################################################################
# @file:        Constant.py
# @developer:   ABHINABA GHOSH
# @date:        APRIL 2022
# @brief:       This file contains all the os paths and dependencies of scripts.
# @rights:      Copyright (C) 2022 | All rights reserved | Abhi_as_Jerry
###################################################################################################

# Modules
import os
import sys
import datetime
from datetime import datetime

# ----------------------------------- Python File Handling System -------------------------------------------
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA = os.path.abspath(PROJECT_PATH + '/data')
LOGS = os.path.abspath(PROJECT_PATH + '/logs')
REPORT = os.path.abspath(PROJECT_PATH + '/report')

IMPORT = os.path.abspath(DATA + '/Import')
UTILITIES = os.path.abspath(PROJECT_PATH + '/Utilities')

IMPORT_DIR_META = {
    'Navic': os.path.abspath(IMPORT + '/Navic'),
}

# ------------------------------------------- Common Constants -------------------------------------------
DATETIME_TODAY = datetime.now().strftime('%d%m%y')
DATETIME_YEAR = datetime.now().strftime('%Y')