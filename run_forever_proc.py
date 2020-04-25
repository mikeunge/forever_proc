#!/usr/bin/python3
#-*- coding: utf-8 -*-
#
# This script starts forever pods.
# Forever lets you run (mainly js) scripts or bots as daemons.
#
# Example:
# forever start -l forever.log -o out.log -e err.log my-daemon.js
import os
import sys
import logging
from pathlib import Path

DEBUG = True    # Toggle DEBUG options.

def readJson(file_path):
    if not os.path.exists(file_path):
        logger.error()
        return False


def setup_logger(level, path):
    # Change the logging format below..
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    try:
        # Check the different cases, default: DEBUG
        if level.upper() == "DEBUG":
            logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
        elif level.upper() == "INFO":
            logging.basicConfig(filename=path, level=logging.INFO, format=log_format)
        elif level.upper() == "ERROR":
            logging.basicConfig(filename=path, level=logging.ERROR, format=log_format)
        else:
            logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
        return logging.getLogger()
    except Exception as ex:
        print(f"Could not setup the logger, exiting the program.\nError: {ex}")
        sys.exit(1)


class Service:
    def isUp(self, daemon):
        """
        Check if the service/daemon is running or not.
        """
        cmd = f"forever list | grep {daemon} >> /dev/null"  # Command to execute.
        out = os.system(cmd)
        if out == 0:
            msg = f"Daemon [{daemon}] is running"
            is_up =  True
        elif out == 256:
            msg = f"Daemon [{daemon}] is not running"
            is_up = False
        else:
            msg = "Something went wrong.."
            is_up = False
        # Try if logging is possible.. only used for tests.
        try:
            logger.debug(f"Command: {cmd}, out={out}")
            logger.info(msg)
        finally:
            return is_up


class Program:
    def __init__(self, settings, home_dir):
        self.SETTINGS = settings
        self.HOME = home_dir

    def start(self):
        # Check if the settings file.
        if not os.path.exists(self.SETTINGS):
            logger.error(f"Settings file doesn't exist, make sure the path is correct and the file exists. [{self.SETTINGS}]\nExiting script.")
            sys.exit(1)
        # Load the settings.
        readJson(self.SETTINGS)
        service = Service()
        if service.isUp("bot.js") == True:
            print("Done")
        else:
            print("Error")


if __name__ == '__main__':
    # Get the current users home directory.
    HOME_DIR = str(Path.home())

    # Check if debug mode is active or not.
    # Debugging mode changes paths and logging levels..
    if DEBUG == True:
        LOG_LEVEL = "DEBUG"
        LOGGING_PATH = "./forever_proc.log"
        SETTINGS_PATH = "./settings.json"
    else:
        LOG_LEVEL = "INFO"
        LOGGING_PATH = f"{HOME_DIR}/forever_proc.log"
        SETTINGS_PATH = f"{HOME_DIR}/.config/forever_proc/settings.json"

    logger = setup_logger(LOG_LEVEL, LOGGING_PATH)
    logger.debug(f"[SYSTEM_INFO]\nHOME_DIR: {HOME_DIR}\nDEBUG: {str(DEBUG)}\nLOG_LEVEL: {LOG_LEVEL}\nLOGGING_PATH: {LOGGING_PATH}\nSETTINGS_PATH: {SETTINGS_PATH}")

    # Initialize the program and start it.
    prog = Program(
        SETTINGS_PATH, 
        HOME_DIR
    )
    prog.start()
    sys.exit(0)
