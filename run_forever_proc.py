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
	data = False
	if not os.path.exists(path):
		# File does not exist.
		logger.error(f"File does not exist, please make sure the path is correct and the file exists.. [{path}]")
	else:
		# Check if the file is empty.
		if os.stat(path).st_size == 0:
			# The file is empty..
			logger.error(f"File is empty, please check the content or given file.. [{path}]")
		else:
			try:
				# Open the file and read the content to data.
				with open(path, "r") as file:
					data = json.load(file)
			except IOError as io:
				logger.error(f"File is currently busy, please close the json file and try it again. [{path}]")
			except Exception as ex:
				logger.error(f"Something unexpected happened, please try again.\nError: {ex}", 1)
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


class Job:
	def __init__(self, max_jobs):
		MAX_JOBS = max_jobs


	def getRegisteredJobs(self, data):
		"""
		Destruct the passed data to get all the registered jobs.
		Loop over the 'jobs' DOM and extract all registered job ids, the numbers are trivial for
			the controller to function.
		:param self: [INT] self.MAX_JOBS
		:param data: [DICT] dict of all jobs in settings.json
		:return [ARRAY]: job id's of registered jobs eg. [1,2,3,4,...]
						 if this fails, reutrns [BOOL] -> False
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

	
	def jobController(self, data):
		"""
		Load the requested job from the passed data dict.
		:param self: 
		:param data: [DICT] dict of all jobs in settings.json
		:param job_id: [INT] 
		"""
		err = False
		job_ids = getRegisteredJobs(data)	# Get all registered jobs (ARRAY).
	
		if err:
			return False
		return True


	def isUp(self, job):
		"""
		Check if the job is running or not.
		"""
		cmd = f"forever list | grep {job} >> /dev/null"  # Command to execute.
		out = os.system(cmd)
		# Check the commands output.
		if out == 0:
			logger.info(f"Daemon [{job}] is running")
			is_up =  True
		elif out == 256:
			logger.info(f"Daemon [{job}] is not running")
			is_up = False
		else:
			logger.error("Something went wrong..")
			is_up = False
		return is_up



class Program:
	def __init__(self, settings, max_jobs, home_dir):
		self.SETTINGS = settings
		self.HOME = home_dir
		self.MAX_JOBS = max_jobs


	def start(self):
		"""
		Start the program and run the workflow(s).
		"""
		# Read the settings file.
		data = readJson(self.SETTINGS)
		if type(data) == dict:
			job = Job(self.MAX_JOBS)
			job.jobController(data)

			# DEBUG
			sys.exit(0)
		else:
			# Data is corrupt/not valid json formatted..
			logger.error(f"Data is not a valid format or corrupt, please check logs for more information..")
			sys.exit(1)


if __name__ == '__main__':
	# Toggle DEBUG mode.
	DEBUG = True

	# Get the current users home directory.
	HOME_DIR = str(Path.home())

	# Check if debug mode is active or not.
	if DEBUG == True:
		settings = {
			"LOG_LEVEL": "DEBUG",
			"LOGGING_PATH": "./forever_proc.log",
			"SETTINGS_PATH": "./settings.json",
			"MAX_JOBS": 10
		}
	else:
		settings = {
			"LOG_LEVEL": "INFO",
			"LOGGING_PATH": f"{HOME_DIR}/forever_proc.log",
			"SETTINGS_PATH": f"{HOME_DIR}/.config/forever_proc/settings.json",
			"MAX_JOBS": 5
		}

	logger = setup_logger(settings[0], settings[1])
	logger.debug(f"[SYSTEM_INFO]\nHOME_DIR: {HOME_DIR}\nDEBUGGING: {str(DEBUG)}\nLOG_LEVEL: {settings[0]}\nLOGGING_PATH: {settings[1]}\nSETTINGS_PATH: {settings[2]}\nMAX_JOBS: {settings[3]}")

	# Initialize the program and start it.
	prog = Program(
		settings[2], 
		settings[3],
		HOME_DIR
	)
	prog.start()
	sys.exit(0)