import tensorflow as tf
import numpy as np
import pyautogui
import time

from target.draw import Point

KEYPOINT_DICT = {
	'nose': 0,
	'left_eye': 1,
	'right_eye': 2,
	'left_ear': 3,
	'right_ear': 4,
	'left_shoulder': 5,
	'right_shoulder': 6,
	'left_elbow': 7,
	'right_elbow': 8,
	'left_wrist': 9,
	'right_wrist': 10,
	'left_hip': 11,
	'right_hip': 12,
	'left_knee': 13,
	'right_knee': 14,
	'left_ankle': 15,
	'right_ankle': 16
}

KEYPOINT_HEAD = {
	'nose': 0,
	'left_eye': 1,
	'right_eye': 2,
	'left_ear': 3,
	'right_ear': 4
}

class Detector(object):
	def __init__(self, large_model=True, threshold=0.5):
		super(Detector, self).__init__()
		tf.device('/GPU:0')
		if large_model:
			self.movenet = tf.saved_model.load("./target/MoveNet_Large").signatures["serving_default"]
			self.crop_size = 256
		else:
			self.movenet = tf.saved_model.load("./target/MoveNet_Small").signatures["serving_default"]
			self.crop_size = 192
		# self.points = []
		# for key in KEYPOINT_HEAD.keys():
		# 	self.points.append(Point(key, size=10))
		#self.screen = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
		self.threshold = threshold

	def predict_head(self, img):
		image = tf.expand_dims(tf.convert_to_tensor(img), axis=0)
		image = tf.cast(tf.image.resize_with_pad(image, self.crop_size, self.crop_size), dtype=tf.int32)
		outputs = self.movenet(image)['output_0'].numpy()[0][0]
		point = [0, 0]
		cnt = 0
		for key in KEYPOINT_HEAD.keys():
			if outputs[KEYPOINT_HEAD[key]][2] >= self.threshold:
				cord = [outputs[KEYPOINT_HEAD[key]][1], outputs[KEYPOINT_HEAD[key]][0]]
				point[0] += cord[0]
				point[1] += (cord[1] - 0.5) * img.shape[1] / img.shape[0] + 0.5
				cnt += 1
		if cnt == 0:
			return None
		point[0] /= cnt
		point[1] /= cnt
		return point

if __name__ == '__main__':
	detector = Detector(threshold=0.5)
	head_point = Point(0, size=10)
	while True:
		point = detector.predict_head(np.array(pyautogui.screenshot()))
		if point != None:
			head_point.move_to_percent(point[0], point[1])
		else:
			head_point.hide()
		time.sleep(0.01)