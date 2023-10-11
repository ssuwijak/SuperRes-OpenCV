import os
import shutil
import logging

'''
logging.basicConfig(level=logging.DEBUG, 
					format="%(asctime)s : %(levelname)-8s : %(name)s : %(message)s", 
					datefmt="%m/%d/%Y %I:%M:%S %p %Z")
'''
logger = logging.getLogger(__name__)

def trim(value: str) -> str:
	logger.debug(f"calling trim('{value}')")
	ret = ""
	
	try:
		ret = value.strip()
		logger.info(f"trim('{value}') = '{ret}'")
	except Exception as ex:
		ret = value
		logger.critical(f"unable to trim '{value}', {ex}")

	return ret

def isEmptyStr(value) -> bool:
	logger.debug(f"calling isEmptyStr('{value}')")

	if value is None:
		logger.warning(f"'{value}' is None")
		logger.info(f"isEmptyStr('{value}') = {True}")
		return True
	
	s = trim(value)
	ret = (s == "" or s == '')
	logger.info(f"isEmptyStr('{value}') = {ret}")

	return ret

def pathExists(pathName: str) -> bool:
	logger.debug(f"calling pathExist('{pathName}')")
	flag = False

	if isEmptyStr(pathName):
		logger.warning(f"'{pathName}' is empty string and invalid path.")
		logger.info(f"'{pathName}' (empty string) not exists") 
		return flag
	
	try:
		flag = os.path.exists(pathName)
		if flag:
			logger.info(f"'{pathName}' exists") 
		else:
			logger.warning(f"'{pathName}' not exist.")
	except Exception as ex:
		logger.critical(f"unable to check '{pathName}', {ex}")

	return flag

def isDir(pathName: str) -> bool:
	logger.debug(f"calling isDir('{pathName}')")
	flag = False

	if pathExists(pathName):
		try:
			flag = os.path.isdir(pathName)
			if flag:
				logger.info(f"'{pathName}' is a Directory.")
			else:
				logger.warning(f"'{pathName}' is not a Directory.")
		except Exception as ex:
			logger.critical(f"unable to check '{pathName}', {ex}")

	return flag

def isFile(pathname: str) -> bool:
	logger.debug(f"calling isFile('{pathname}')")
	flag = False
	
	if pathExists(pathname):
		try:
			flag = os.path.isfile(pathname)
			if flag:
				logger.info(f"'{pathname}' is a File.")
			else:
				logger.warning(f"'{pathname}' is not a File.")
		except Exception as ex:
			logger.critical(f"unable to check '{pathname}', {ex}")

	return flag

def pathSplit(pathName: str):
	logger.debug(f"calling pathSplit('{pathName}')")

	parent_path, filename, name, extension = "","","",""
	s = trim(pathName)

	if isEmptyStr(s):
		logger.error(f"pathName='{pathName}' was empty and invalid path.")	
		return parent_path, filename, name, extension

	try:
		#parent_path, filename = pathName.rsplit("/", 1)
		#name, extension = filename.rsplit(".", 1)

		filename = os.path.basename(pathName)
		name, extension = os.path.splitext(filename)
		parent_path = os.path.dirname(pathName)

		logger.info(f"parent_path='{parent_path}' , filename='{filename}' , name='{name}' , ext='{extension}'")
	except Exception as ex:
		logger.critical(f"unable to split the path '{pathName}', {ex}")
	
	return parent_path, filename, name, extension


def delDir(dirname):
	logger.debug(f"calling delDir('{dirname}')")
	flag = False

	if isDir(dirname):
		try:
			shutil.rmtree(dirname)
			flag = True
			logger.info(f"[DIR]= '{dirname}' was deleted successfully.")
		except Exception as ex:
			logger.critical(f"unable to delete [DIR]= '{dirname}', {ex}")

	return flag

def delFile(filename):
	logger.debug(f"calling delFile('{filename}')")
	flag = False
	
	if isFile(filename):
		try:
			os.remove(filename)
			flag = True
			logger.info(f"[FILE]= '{filename}' was deleted successfully.")
		except Exception as ex:
			logger.critical(f"unable to delete [FILE]= '{filename}', {ex}")

	return flag

def createDir(dirname, force_del = True):
	logger.debug(f"caling createDir('{dirname}')")
	flag = 0
	name = ""

	if "/" in dirname or "\\" in dirname:
		name = os.path.basename(dirname)
	else:
		name = dirname
	
	if isFile(name):
		flag = -1
		logger.warning(f"[FILE]= '{dirname}' already exists, please avoid this name.")
		return False
	
	if isDir(name):
		logger.warning(f"[DIR]= '{dirname}' already exists")
		logger.debug(f"force to delete = {force_del}")
		
		if force_del:
			if not delDir(dirname):
				flag = -2
		else:
			flag = 1

	if flag == 0:
		try:
			os.mkdir(dirname)
		except Exception as ex:
			flag = -3
			logger.critical(f"[DIR]= '{dirname}' can\'t be created, {ex}")

	if flag == 0:
		logger.info(f"[DIR]= '{dirname}' was created successfully.")
	elif flag == 1:
		logger.warning(f"[DIR]= '{dirname}' already exists, nothing to create.")
	else:
		pass

	return flag >= 0

def fileList(dirname):
	logger.debug(f"calling fileList('{dirname}')")
	if not isDir(dirname):
		logger.warning(f"fileList('{dirname}') = None")
		return None

	files = os.listdir(dirname)
	files = [f for f in files if os.path.isfile(dirname + '/' + f)] #Filtering only the files.
	# logger.debug(*files, sep="\n")

	logger.info(f"fileList('dirname') = {files}")

	return files

def dirList(dirname):
	logger.debug(f"calling dirList('{dirname}')")
	if not isDir(dirname):
		logger.warning(f"dirList('{dirname}') = None")
		return None

	dirs = os.listdir(dirname)
	dirs = [d for d in dirs if os.path.isdir(dirname + '/' + d)] #Filtering only the files.
	# logger.debug(*dirs, sep="\n")
	
	logger.info(f"dirList('dirname') = {dirs}")
	
	return dirs

