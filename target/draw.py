import cv2
import numpy as np
import win32gui
import win32con

def make_window_borderless(hwnd):	
	style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
	style &= ~win32con.WS_OVERLAPPEDWINDOW
	style |= win32con.WS_POPUP
	win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
	win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
	win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

class Point(object):
	def __init__(self, id, size=4):
		super(Point, self).__init__()
		self.id = id
		self.name = "mask" + str(id)
		self.size = size
		self.screen = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
		# cv2.namedWindow(self.name, cv2.NORMAL_WINDOW)
		cv2.imshow(self.name, np.ones((size, size, 3), np.uint8) * 0)
		self.hwnd = win32gui.FindWindow(0, self.name)
		make_window_borderless(self.hwnd)
		win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
		win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
		win32gui.MoveWindow(self.hwnd, 0, 0, size, size, True)
		self.hide()

	def move(self, x, y):
		cv2.moveWindow(self.name, x - self.size // 2, y - self.size // 2)
		cv2.waitKey(1)

	def hide(self):
		self.move(self.screen[0] - self.size, self.screen[1] - self.size)

	def move_to_percent(self, dx, dy):
		self.move(self.screen[0] + int((self.screen[2] - self.screen[0]) * dx), self.screen[1] + int((self.screen[3] - self.screen[1]) * dy))