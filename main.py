import numpy as np
import pyautogui

from target.detect import Detector
from target.draw import Point
from aim import move

SIZE = 640

if __name__ == '__main__':
	detector = Detector(threshold=0.5)
	head_point = Point(0, size=10)
	while True:
		img = np.array(pyautogui.screenshot())
		mid = (img.shape[0] // 2, img.shape[1] // 2)
		img = img[mid[0] - SIZE // 2: mid[0] + SIZE // 2, mid[1] - SIZE // 2: mid[1] + SIZE // 2, :]
		base = (mid[0] - SIZE // 2, mid[1] - SIZE // 2)
		point = detector.predict_head(img)
		if point != None:
			target = (base[1] + SIZE * point[1], base[0] + SIZE * point[0])
			head_point.move(int(target[0]), int(target[1]))
			cord = win32api.GetCursorPos()
			move(target[0] - cord[0], target[1] - cord[1], smooth=True)
		else:
			head_point.hide()