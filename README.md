# SuperRes-OpenCV
Super Resolution by OpenCV

## References
* https://learnopencv.com/super-resolution-in-opencv/
* https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066
* https://www.youtube.com/watch?v=-LqHr5V67C4&t=586s

## Procedures
1. create the virual env in a blank folder
    * `python -m venv SuperRes`
    * `cd SuperRes`
    * `Scripts\activate`
2. install dependencies (https://pyimagesearch.com/2018/09/19/pip-install-opencv/)
    * `pip install opencv-contrib-python` (recommended)
3. download your needed models
    * https://learnopencv.com/super-resolution-in-opencv/  (read model section, the links are there)
4. modify as you needed and run the codes
    * modify the upscale.py and main() function as you needed
    * run by the command, `python upscale.py`


## Models
There are currently 4 different SR models supported in the module. They can all upscale images by a scale of 2, 3 and 4. LapSRN can even upscale by a factor of 8. They differ in accuracy, size and speed.

1. EDSR [1].
    * This is the best performing model.
    * However, it is also the biggest model and therefor has the biggest file size and slowest inference.
    * You can download it [here](https://github.com/Saafke/EDSR_Tensorflow/tree/master/models).
2. ESPCN [2].
    * This is a small model with fast and good inference.
    * It can do real-time video upscaling (depending on image size).
    * You can download it [here](https://github.com/fannymonori/TF-ESPCN/tree/master/export).
3. FSRCNN [3].
    * This is also small model with fast and accurate inference.
    * Can also do real-time video upscaling.
    * You can download it [here](https://github.com/Saafke/FSRCNN_Tensorflow/tree/master/models).
4. LapSRN [4].
    * This is a medium sized model that can upscale by a factor as high as 8.
    * You can download it [here](https://github.com/fannymonori/TF-LapSRN/tree/master/export).
