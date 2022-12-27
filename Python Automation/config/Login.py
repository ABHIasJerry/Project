###################################################################################################
# @file:        Login.py
# @developer:   ABHINABA GHOSH
# @date:        APRIL 2022
# @brief:       This file contains all the server login functions.
# @rights:      Copyright (C) 2022 | All rights reserved | Abhi_as_Jerry
###################################################################################################

# Modules
import os
import sys
import datetime
import subprocess
import threading
import paramiko
from typing import Any
from datetime import datetime


class SERVER_SUPPORT:
    def __init__(self, test_case_name: str, wifi_enable=False):
        self.remote_ip = '255.255.255.255'
        if wifi_enable:
            self.remote_ip = '192.168.1.1'
        self.remote_port = 2222
        self.username = 'admin'
        self.password = 'admin'
        self.test_case_name = test_case_name
        self.ssh_client = paramiko.SSHClient()

    def __enter__(self):
        """
            Connect to SERVER_SUPPORT
        Raises:
            Exception : User define failed connection Exception
        """
        try:
            print(f'[{self.test_case_name}] > Connecting to Server ... ')
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.remote_ip, self.remote_port, self.username, self.password, look_for_keys=False)
            if not self.is_connected():
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(self.remote_ip, self.remote_port, self.username, self.password,
                                        look_for_keys=False)
                print(f'[{self.test_case_name}] > Successfully Connected ... ')
                return self
            print(f'[{self.test_case_name}] > Already Connected ... ')
            return self
        except Exception as E:
            print(f"[{self.test_case_name}] > Failed to connect to Server ")
            raise E

    def is_connected(self) -> bool:
        """
            Check Server is connected or not
        Returns:
            bool : Server connection status
        """
        cmd = 'pwd'
        try:
            self.ssh_client.exec_command(cmd, timeout=30)
            return True
        except Exception:
            return False

    def download_file(self, from_location: str, to_location: str) -> bool:
        """
            Download File using sftp
        Returns:
            bool : status of downloading
        Raises:
            Exception : User define failed to download file
        """
        try:
            ftp_client = self.ssh_client.open_sftp()
            ftp_client.get(from_location, to_location)
            ftp_client.close()
            return True
        except Exception as E:
            print(f"[{self.test_case_name}] > Failed to download file from server : " + str(E))
            return False

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """
            Close ssh Connection
        """
        # if self.is_connected():
        if self.is_connected():
            self.ssh_client.close()
        return True