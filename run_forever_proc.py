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
import json
import logging
from pathlib import Path


def readJson(path):
    """
    Read the passed json file and return the content (dict).
    """
    # Read the json file and return the data.
    if not os.path.exists(path):
        # File does not exist.
        logger.error(f"File does not exist, please make sure the path is correct and the file exists.. [{path}]")
        return False
    # Check if the file is empty.
    if os.stat(path).st_size == 0:
        # The file is empty..
        logger.error(f"File is empty, please check the content or given file.. [{path}]")
        return False
    try:
        # Open the file and read the content to data.
        with open(path, "r") as file:
            data = json.load(file)
    except IOError as io:
        logger.error(f"File is currently busy, please close the json file and try it again. [{path}]")
        return False
    except Exception as ex:
        logger.error(f"Something unexpected happened, please try again.\nError: {ex}", 1)
        return False
    return data


def setup_logger(level, path):
    # Change the logging format below..
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    try:
        # Check the different cases, default: DEBUG
        if level.upper() == "DEBUG":
            logging.basicConfig(filename=path, level=logging.DEBUG, format=log_format)
        elif level.upper() == "INFO":
            logging.basicConfig(filename=path, level=logging.INFO, format=log_format)
        elif level.upper() == "WARNING":
            logging.basicConfig(filename=path, level=logging.WARNING, format=log_format)
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
        ERR = False
        # Check the commands output.
        if out == 0:
            msg = f"Daemon [{daemon}] is running"
            is_up =  True
        elif out == 256:
            msg = f"Daemon [{daemon}] is not running"
            is_up = False
        else:
            ERR = True
            msg = "Something went wrong.."
            is_up = False
        # Try if logging is possible.. only used for tests.
        try:
            logger.debug(f"Command: {cmd}, out={out}")
            if ERR:
                logger.error(msg)
            else:
                logger.info(msg)
        finally:
            return is_up


class Program:
    def __init__(self, settings, home_dir, max_jobs):
        self.SETTINGS = settings
        self.HOME = home_dir
        self.MAX_JOBS = max_jobs


    def dataDestruct(self, data):
        """
        Destruct the passed data / get all the registered jobs.
        """
        i = 0
        reg_jobs = []
        for job_id in data['jobs']:
            i += 1
            reg_jobs.append(job_id)
            if i == self.MAX_JOBS:
                break
        # Return array of registered jobs.
        return reg_jobs


    def loadJob(self, data, job_id):
        """
        Load the requested job from the data dict.
        Return the formatted job data.
        """
        
        pass


    def start(self):
        # Read the settings file.
        # TODO: Outsource in new function...
        data = readJson(self.SETTINGS)
        if data == False:
            # Something went wrong while reading the json file...
            logger.warning("Something went wrong, please check the logs...")
            sys.exit(1)
        elif type(data) == dict:    # Check if returned data is a dictonary.
            dest_data = Program.dataDestruct(self, data)
            for job in dest_data:
                print(job)
            # DEBUG
            sys.exit(0)
        else:
            # Data is corrupt/not valid json formatted..
            logger.error(f"Data is not a valid json format, please check your file.. [{self.SETTINGS}]")
            sys.exit(1)
        service = Service()
        if service.isUp("bot.js") == True:
            print("Done")
        else:
            print("Error")


if __name__ == '__main__':
    # Toggle DEBUG mode.
    DEBUG = True

    # Get the current users home directory.
    HOME_DIR = str(Path.home())

    # Define the maximal number of jobs to load.
    MAX_JOBS = 10

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
    logger.debug(f"[SYSTEM_INFO]\nHOME_DIR: {HOME_DIR}\nDEBUGGING: {str(DEBUG)}\nLOG_LEVEL: {LOG_LEVEL}\nLOGGING_PATH: {LOGGING_PATH}\nSETTINGS_PATH: {SETTINGS_PATH}\nMAX_JOBS: {MAX_JOBS}")

    # Initialize the program and start it.
    prog = Program(
        SETTINGS_PATH, 
        HOME_DIR,
        MAX_JOBS
    )
    prog.start()
    sys.exit(0)
