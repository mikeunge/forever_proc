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

# Toggle tests and debug values.
TEST = True
DEBUG = True

def readJson(file_path):
    if not os.path.exists(file_path):
        logger.error()
        return False

class Service:
    def __init__(self):
        pass

    def isUp(self):
        """´
        Check if the service is running.
        :para self: self.storage
        :return: Bool
        """
        # TODO: out is literally garbage.. Output needs to be fixed ASAP..
        out = os.system("forever list | grep /bots/statBot/bot.js")
        print(out)


class App:
    def __init__(self, settings, home_dir):
        self.SETTINGS = settings
        self.HOME = home_dir

    def start(self):
        # Check if the settings file.
        if not os.path.exists(self.SETTINGS):
            logger.error(f"Settings file doesn't exist, make sure the path is correct and the file exists. [{settings}]\nExiting script.")
            sys.exit(1)
        readJson(self.SETTINGS)


# Class for service tests.
class TestService:
    def __init__(self):
        self.service = Service()

    def test_isUp(self):
        self.service.isUp()


if __name__ == '__main__':
    # Get the current users home directory.
    HOME_DIR = str(Path.home())

    # Check if debug mode is active or not.
    if DEBUG == True:
        print("DEBUGGING IS ENABLED!!!\n")
        LOGGING_PATH = "./forever_proc.log"
        SETTINGS_PATH = "./settings.json"
    else:
        # Change paths if needed.
        LOGGING_PATH = "/var/log/forever_proc.log"
        SETTINGS_PATH = f"{HOME_DIR}/.config/forever_proc/settings.json"

    try:
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=log_format)
        logger = logging.getLogger()
    except:
        print("Could not setup the logger, exiting the program.")
        sys.exit(1)

    # Check if tests are enabled.
    if TEST == True:
        logger.info("TESTS ARE ACTIVE!")
        # Write test cases below..

        logger.info("isUp tests started..")
        TestService().test_isUp()
        logger.info("isUp tests finished..")
    else:
        # Initialize the program and run it.
        app = App(SETTINGS_PATH, HOME_DIR)
        app.start()
    sys.exit(0)
