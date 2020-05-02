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


class Job:
	def __init__(self, max_jobs, data):
		self.MAX_JOBS = max_jobs
		self.REG_JOBS = []
		self.JOB_DATA = data


	def registerJobs(self):
		"""
		Loop over the given dataset (self.JOB_DATA) and extract all the exiting/registered jobs.
		The job_ids are then stored in the self.REG_JOBS variable for further process.
		"""
		i = 0
		for id in self.JOB_DATA:
			i += 1
			self.REG_JOBS.append(id)
			if i == self.MAX_JOBS:		# Check if MAX_JOBS is reached or not.
				break


	def jobController(self):
		"""
		This is the "main" function of the "Job" class.
		It initializes all the different components and controlls the further workflow and logic.
		"""
		err = False
		self.registerJobs()	# Get all registered jobs.
		logger.debug(f"Registered jobs: {self.REG_JOBS}")
		for id in self.REG_JOBS:
			job = self.JOB_DATA[id]
			logger.debug(f"Job [{id}] Data: {job}")
			if not self.isUp(job['name']):
				# The job is inactive, try starting it!
				logger.info(f"Trying to start the job. [{job['name']}]")
				if not self.startJob(id):	# Check if the job execution works.
					logger.error(f"Could not start the job [{job['name']}].")
					err = True		# Set error to true..
				else:
					logger.info(f"Successfully startet process {job['name']}!")
		if err:
			return False
		return True


	def startJob(self, job_id):
		"""
		Try to start a new forever processor job.
		"""
		try:
			job = self.JOB_DATA[job_id]		# Initialize the job.
		except Exception as ex:
			logger.error(f"Could not initialize data set..\nError: {ex}")
		try:
			# Map the job data to variables.
			name = job['name']
			start = job['start']
			log = job['log_path']
		except Exception as ex:
			logger.error(f"Could not load data..\nError: {ex}")
			return False

		# Get the last character from the log path.
		# If last char is not "/", it gets added.
		log_last_char = log[-1]
		if log_last_char != "/":
			logger.debug(f"Logging path is missing '/' at the end.. Correcting the path.")
			log += "/"

		# Create the different log paths.
		out_log = log + name + ".out.log"
		err_log = log + name + ".err.log"
		log = log + name + ".log"

		# Construct the forever command.
		cmd = f"forever start -s -a -l {log} -o {out_log} -e {err_log} {start} >> /dev/null"
		try:
			out = os.system(cmd)
			logger.debug(f"Executing command: {cmd}\nOutput: {out}")
			if out != 0:
				return False
			return True
		except Exception as ex:
			logger.error(f"Something went wrong while creating forever processes..\nError: {ex}")
			return False


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
			try:
				# Try to initialize the Job class.
				job = Job(self.MAX_JOBS, data['jobs'])
			except Exception as ex:
				logger.error(f"Could not initialize the jobs..\nError: {ex}")
			
			if not job.jobController():
				logger.error("jobController has returned with errors. Please check the logs for more information.")
				return False
		else:
			# Data is corrupt/not vaslid json formatted..
			logger.error(f"Data is not a valid format or corrupt, please check logs for more information..")
			return False
		return True


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

	logger = setup_logger(settings['LOG_LEVEL'], settings['LOGGING_PATH'])
	logger.debug(f"[SYSTEM_INFO]\nHOME_DIR: {HOME_DIR}\nDEBUGGING: {str(DEBUG)}\nLOG_LEVEL: {settings['LOG_LEVEL']}\nLOGGING_PATH: {settings['LOGGING_PATH']}\nSETTINGS_PATH: {settings['SETTINGS_PATH']}\nMAX_JOBS: {settings['MAX_JOBS']}")

	# Initialize the program and start it.
	prog = Program(
		settings['SETTINGS_PATH'], 
		settings['MAX_JOBS'],
		HOME_DIR
	)
	logger.info("--- Script started ---")

	if not prog.start():
		logger.info("--- Script exits : code 1 ---")
		sys.exit(1)

	logger.info("--- Script exits : code 0 ---")
	sys.exit(0)