###################################################################################################
# @file:        Helper.py
# @developer:   ABHINABA GHOSH
# @date:        APRIL 2022
# @brief:       This file contains all the helper function for main.
# @rights:      Copyright (C) 2022 | All rights reserved | Abhi_as_Jerry
###################################################################################################

# Modules
import base64
import json
import os
import shutil
import subprocess
import time
import zipfile
from datetime import datetime
from multiprocessing import Process, Manager, Queue
from typing import List, Dict, Union

import cv2
import numpy
from selenium import webdriver
from PIL import Image
from filehash import FileHash
from pytesseract import pytesseract
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uiautomator import JsonRPCError
from uiautomator import device


class CommonFunctions:
    def __init__(self):
        self.name = 'automation'
