import logging
from log_common import logger
import cv2
from cv2 import dnn_superres
from fileman import *

'''
logging.basicConfig(level=logging.DEBUG, 
					format="%(asctime)s : %(levelname)-8s : %(name)s : %(message)s", 
					datefmt="%m/%d/%Y %I:%M:%S %p %Z")
'''

logger = logging.getLogger(__name__)


def upscale():
	# Create an SR object
	sr = dnn_superres.DnnSuperResImpl_create()

	# Read image
	image = cv2.imread('./input.png')

	# Read the desired model
	path = "EDSR_x3.pb"
	sr.readModel(path)

	# Set the desired model and scale to get correct pre- and post-processing
	sr.setModel("edsr", 3)

	# Upscale the image
	result = sr.upsample(image)

	# Save the image
	cv2.imwrite("./upscaled.png", result)


def upscale2(input: str, output: str = 'upscaled_img', model_name: str = 'FSRCNN', scale_x: int = 4, has_cuda: bool = False):
	logger.debug(f"calling upscale2('{input}', '{output}', '{model_name}', {scale_x}, {has_cuda})")

	list_scales = [2, 3, 4, 8]
	list_models = ['EDSR', 'ESPCN', 'FSRCNN', 'LapSRN']
	model_path = ""

	print(f"\tupscale image(s) [DIR]='{input}' --> [DIR]='{output}'\n")

	if not isDir(input):
		logger.error(f"unable to find [DIR]='{input}' for input images.")
		return

	if not createDir(output, False):
		logger.error(f"unable to create [DIR]='{output}' for upscaled results.")
		return

	if scale_x not in list_scales:
		logger.warning(f"scale_x = {scale_x} was out of range, it was set to be 4 (default).")
		scale_x = 4

	if model_name in list_models:
		model_path = os.path.join('models', model_name, model_name + '_x' + str(scale_x) + '.pb')

	if isEmptyStr(model_path):
		logger.error(f"'{model_name}' was unknown, it was out of range {list_models})")
		return
	elif not isFile(model_path):
		logger.error(f"'{model_path}' not found, please download it first.")
		return
	else:
		print(f"\tmodel='{model_path}' was found.")

	# return

	logger.debug(f"create an sr object.")
	sr = dnn_superres.DnnSuperResImpl_create()

	logger.debug(f"read the model at '{model_path}'")
	sr.readModel(model_path)

	logger.debug(f"set the desired model='{model_name.lower()}'and scale={scale_x} to get correct pre- and post-processing")
	sr.setModel(model_name.lower(), scale_x)

	# if you have cuda support, select cuda options for both
	if has_cuda:
		try:
			logger.debug(f"set for processing by CUDA (GPU)")
			sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		except Exception as ex:
			logger.error(f"unable to process by GPU, it was re-set to CPU instead, {ex}")
			sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
			sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
	else:
		logger.debug(f"set for processing by normal CPU")
		sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
		sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	suffix = f"{model_name.lower()}_x{scale_x}"
	file_count = 0
	# filenames = ["parent_path", "filename", "name", ".ext"]
	exts = (".jpg", ".png", ".jpeg", ".gif", ".bmp", )
	
	for img_name in fileList(input):
		file_count += 1
		filenames = pathSplit(img_name)

		print(f"{file_count}) upscaling [FILE]='{img_name}' ... ", end="")

		if filenames[3] in exts:
			try:
				img = cv2.imread(os.path.join(input, img_name))
				result = sr.upsample(img)

				saved_to = os.path.join(
					output, filenames[2] + '_' + suffix + filenames[3])

				if pathExists(saved_to):
					delFile(saved_to)

				cv2.imwrite(saved_to, result)

				print(f"saved as '{saved_to}'")
			except Exception as ex:
				print(f"error, {ex}")
				logger.critical(f"{ex}")
		else:
			print(f"skip, '{filenames[1]}' is not image file.")
			file_count -= 1

	print(f"\n\tdone, {file_count} file(s) were upscaled totally.")


def main():
	upscale2('upload_img', 'upscaled_img', 'LapSRN', 4, False)


if __name__ == "__main__":
	main()
