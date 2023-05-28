import numpy as np
import cv2 as cv
from enum import Enum

class OriginPoint(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

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

  def get_rois(self):
    top_left = self.copy()
    top_left.img = top_left._get_roi(self.area_left, self.area_top)
    top_right = self.copy()
    top_right.img = top_right._get_roi(self.area_right, self.area_top)
    bottom_left = self.copy()
    bottom_left.img = bottom_left._get_roi(self.area_left, self.area_bottom)
    bottom_right = self.copy()
    bottom_right.img = bottom_right._get_roi(self.area_right, self.area_bottom)
    return (top_left, top_right, bottom_left, bottom_right)

  def _get_roi(self, area_lr: type[Area], area_ud: type[Area]):
    return self.img[area_ud.begin:area_ud.end, area_lr.begin:area_lr.end]
    
  def blur(self, kernel, border):
    return Image(cv.GaussianBlur(self.img, kernel, border))
    
  def gray(self):
    print(self.img)
    return Image(cv.cvtColor(self.img, cv.COLOR_RGB2GRAY))

  def thresh(self):
    return cv.threshold(self.img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

  def edge_corner_detect(self):
    rois = self.get_rois()
    top_left, top_right, bottom_left, bottom_right = tuple(Image(roi) for roi in rois)
    return (
        top_left._edge_corner_detect(self.area_left, self.area_top, np.min, np.min),
        top_right._edge_corner_detect(self.area_right, self.area_top, np.max, np.min),
        bottom_left._edge_corner_detect(self.area_left, self.area_bottom, np.min, np.max),
        bottom_right._edge_corner_detect(self.area_right, self.area_bottom, np.max, np.max),
    )

  def _edge_corner_detect(self, area_lr, area_tb, x_func, y_func):
    i0, i1 = self._edge_indices()
    return (self.area_lr.begin + x_func(i0), self.area_tb.begin + y_func(i1))
        
  def _edge_indices(self):
    grayed = self.gray()
    blured = grayed.blur((15, 15), 0)
    canny = cv.Canny(blured.img, 100, 200)
    axis0 = np.sum(canny, axis=0)
    axis0indices = np.where(axis0 != 0)
    axis1 = np.sum(canny, axis=1)
    axis1indices = np.where(axis1 != 0)
    return (axis0indices, axis1indices)
        

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
  
  def fix_perspective(self, corners, cell_size, cell_num):
    """Fix the perspective of the maze"""
    cell_w, cell_h = cell_size
    cell_nw, cell_nh = cell_num
    img_w = cell_w * cell_nw
    img_h = cell_h * cell_nh
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [img_w - 1, 0], [0, img_h - 1], [img_w - 1, img_h - 1]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    print("Set new areas and origin points!")
    return Image(cv.warpPerspective(self.img, matrix, (img_h, img_w)))

  @staticmethod
  def from_map(m):
    COLOR_CLASSES = [
        (255, 0, 0), # red
        (0, 255, 0), # green
        (0, 255, 255), # cyan
        (0, 0, 0), # black
        (255, 255, 255), # white
    ]
    m = m.m
    w, h = m.shape
    image = np.zeros((h * 10, w * 10, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            image[y*10:(y+1)*10-1, x*10:(x+1)*10-1] = COLOR_CLASSES[m[y, x]]
    return Image(image)
