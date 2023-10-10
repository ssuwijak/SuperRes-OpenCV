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


def upscale2(input: str, output: str = 'output', model_name: str = 'LapSRN', scale_x: int = 4, has_cuda: bool = False):
	list_scales = [2,3,4,8]
	list_models = ['EDSR','ESPCN','FSRCNN','LapSRN']
	model_path = ''

	if not isDir(input):
		logger.error(f"unable to find the '{input}' folder for input images.")
		return

	if not createDir(output, False):
		logger.error(f"unable to create the '{output}' folder for scaling output.")
		return

	if scale_x not in list_scales:
		logger.warning(f"scale_x = {scale_x} was out of range, it was set to 4 (default).")
		scale_x = 4

	if model_name in list_models:
		model_path = os.path.join('models', model_name, model_name + '_x' + str(scale_x) + '.pb')

	if model_path == '':
		logger.error(f"'{model_name}' was unknown, it was out of range {list_models})")
		return
	elif not isFile(model_path):
		logger.error(f"'{model_path}' not found, please download it first.")
		return
	else:
		print(f"'{model_path}' was found.")

	#return

	sr = dnn_superres.DnnSuperResImpl_create()
	sr.readModel(model_path)
	sr.setModel(model_name.lower(), scale_x)

	# if you have cuda support, select cuda options for both
	if has_cuda:
		sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
	else:
		sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CPU)
		sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	suffix = f"{model_name.lower()}{scale_x}x"
	file_count = 0

	for img_name in fileList(input):
		file_count += 1
		# print(os.path.join(input, img_name))
		print(f"{file_count}) upscaling '{img_name}' ... ", end="")

		try:
			img = cv2.imread(os.path.join(input, img_name))
			result = sr.upsample(img)

			saved_to = os.path.join(output, os.path.splitext(img_name)[0] + '_' + suffix + '.png')

			cv2.imwrite(saved_to, result)

			print(f"saved as '{saved_to}'")
		except Exception as ex:
			print(f"error, {ex}")


	print(f"done, totally {file_count} file(s) were upscaled.")


def main():
	upscale2('input', 'output', 'LapSRN', 6, True)


if __name__ == "__main__":
		main()