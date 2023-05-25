import numpy as np
import cv2 as cv

class Area:
  begin, end = None, None

  def __init__(self, begin, end):
    self.begin = begin
    self.end = end

class Image:
  img = None
  area_top = None
  area_bottom = None
  area_left = None
  area_right = None

  op_top_left = None
  op_top_right = None
  op_bottom_left = None
  op_bottom_right = None

  def __init__(self, img):
    self.img = img
    
  def copy(self):
    image = Image(self.img.copy())
    image.set_areas(
        self.area_top,
        self.area_bottom,
        self.area_left,
        self.area_right,
    )
    image.set_origin_points(
        (self.op_top_left[0], self.op_bottom_left[0]),
        (self.op_top_left[1], self.op_top_right[1]),
    )
    return image

  def set_areas(self, area_top, area_bottom, area_left, area_right):
    self.area_top = area_top
    self.area_bottom = area_bottom
    self.area_left = area_left
    self.area_right = area_right

  def set_origin_points(self, op_tb, op_lr):
    self.op_top_left = (op_tb[0], op_lr[0])
    self.op_top_right = (op_tb[0], op_lr[1])
    self.op_bottom_left = (op_tb[1], op_lr[0])
    self.op_bottom_right = (op_tb[1], op_lr[1])
  
  def make_mask(self, low, high):
    """Make a mask from the image"""
    image = self.copy()
    image.img = cv.inRange(image.img, low, high)
    return image

  def rgb_to_hsv(self):
    image = self.copy()
    image.img = cv.cvtColor(image.img, cv.COLOR_RGB2HSV)
    return image
  
  def find_corners(self):
    """Find the corners of the maze"""
    top_left = self._find_corner(self.area_left, self.area_top, self.op_top_left)
    top_right = self._find_corner(self.area_right, self.area_top, self.op_top_right)
    bottom_left = self._find_corner(self.area_left, self.area_bottom, self.op_bottom_left)
    bottom_right = self._find_corner(self.area_right, self.area_bottom, self.op_bottom_right)

    return (top_left, top_right, bottom_left, bottom_right)

  def _find_corner(self, area_lr: type[Area], area_ud: type[Area], origin_point):
    roi_img = self.img[area_ud.begin:area_ud.end, area_lr.begin:area_lr.end]
    roi_img = np.float32(roi_img)
    roi_harris_corners = cv.cornerHarris(roi_img, blockSize=3, ksize=3, k=0.05)

    roi_harris_points = np.argwhere(roi_harris_corners > 0.025 * roi_harris_corners.max())

    roi_distances = np.array([np.linalg.norm(origin_point - point) for point in roi_harris_points])
    roi_index = np.argmin(roi_distances)
    roi_point = roi_harris_points[roi_index]

    return (roi_point[1] + area_lr.begin, roi_point[0] + area_ud.begin)

  def paint_corners(self, corners):
    for corner, color in zip(corners, [
        [255, 0 ,0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 255, 0],
    ]):
      self._paint_corner(corner, color)
            
  def _paint_corner(self, corner, color):
    self.img[corner[1]-10:corner[1]+10, corner[0]-10:corner[0]+10] = color
  
  def fix_perspective(self, corners):
    """Fix the perspective of the maze"""
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [300 - 1, 0], [0, 300 - 1], [300 - 1, 300 - 1]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    print("Set new areas and origin points!")
    return Image(cv.warpPerspective(self.img, matrix, (300, 300)))

