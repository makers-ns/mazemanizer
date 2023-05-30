import collections
import time
import traceback
import numpy as np
import os
import cv2 as cv
import mapa
import image
import random

class CellType:
  FIELD = 0 # prazno dostupno polje
  WALL = 1
  BALL = 2
  START = 4
  GOAL = 3


BLUE_LOWER = (90, 168, 154)
BLUE_UPPER = (110, 255, 255)
dir_changes_dict = {
  (-1, 0): "./esp-up.sh", 
  ( 1, 0): "./esp-down.sh",
  
  (0, -1): "./esp-left.sh",
  (0,  1): "./esp-right.sh",
  
  (-1, -1): "./esp-uleft.sh",
  (-1,  1): "./esp-uright.sh",
  ( 1, -1): "./esp-dleft.sh",
  ( 1,  1): "./esp-dright.sh"
}


class Pathfinding:
  
  matrix = None # expected to be 24x24
  visited = None
  bvis = None
  ball_pos = None
  instructions_list = None
  finished = None
  goal_pos = None

  map_img = None
  queue = None

  last_command = None
  command = None
  def __init__(self) -> None:
    self.finished = False
    self.matrix = None 
    self.visited = np.zeros((24,24), dtype=int) 
    self.bvis = np.zeros((24, 24), dtype=bool)
    self.instructions_list = list()
    self.queue = list()
    self.path_chosen = list()
    #self._find_ball_pos()

  def set_matrix(self, _matrix):
    self.matrix = _matrix

  def test(self, grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == CellType.GOAL:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < 24 and 0 <= y2 < 24 and grid[y2][x2] != CellType.WALL and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
  def _find_ball_pos(self, mat) -> None:
    '''Finds the position of the ball'''
    h, w = mat.shape[:2]
    for y in range(h):
      for x in range(w):
        if mat[y][x] == CellType.BALL:
          self.ball_pos = (y,x)
    
    
  def _check_constrains(self, current, offset):
    '''Check if given field is withing matrix dimensions'''
    if current[0]+offset[0] >= 0 and current[0]+offset[0] <= 23:
      if current[1]+offset[1] >= 0 and current[1]+offset[1] <= 23:
        return True

    return False
  
  @staticmethod
  def _print_m(m):
    '''QOL - prints out matrix (m)'''
    print()
    for i in range(23):
      for j in range(23):
        print(m[i][j], end="\t")
      print()

  def __str__(self) -> str:
    '''QOL improvement - can print matrix of this class using print()'''
    buffer = ""
    for row in self.matrix:
      for cell in row:
        buffer += f"{str(cell)} "
      buffer += "\n"

    return buffer

  def execute_next(self):
    self.last_command = self.command
    self.command = self.instructions_list.pop(0)
    if self.command == self.last_command:
      return False
    os.system('./esp-stop.sh')
    print(f"{self.command} -> {os.system(self.command)}")
    return True

vid = cv.VideoCapture(0)
calibration = np.load('rig/calib.npz')
mtx = calibration['mtx']
dist = calibration['dist']
rvecs = calibration['rvecs']
tvecs = calibration['tvecs']

p = Pathfinding()
frame = cv.imread('./images/walls.jpg')
img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
h, w = img.shape[:2]
newCameraMtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
undistortedImg = cv.undistort(img, mtx, dist, None, newCameraMtx)

image_class = image.Image(undistortedImg)
image_class.set_areas(
    image.Area(50, 150),
    image.Area(350, 450),
    image.Area(125, 225),
    image.Area(450, 550),
)
image_class.set_origin_points((0, 99), (0, 99))
hsv_class = image_class.rgb_to_hsv()
mask_class = hsv_class.make_mask(BLUE_LOWER, BLUE_UPPER)
corners = mask_class.find_corners()
fix1_class = image_class.fix_perspective(corners, (10, 10), (24, 24))
fix1_mapa = mapa.Mapa.from_image(fix1_class.img, (10, 10), (24, 24))
map_image = image.Image.from_map(fix1_mapa)
p.set_matrix(fix1_mapa.m)

while(True):
    ret, frame = vid.read()
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    newCameraMtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistortedImg = cv.undistort(img, mtx, dist, None, newCameraMtx)

    image_class = image.Image(undistortedImg)
    image_class.set_areas(
        image.Area(50, 150),
        image.Area(350, 450),
        image.Area(125, 225),
        image.Area(450, 550),
    )
    image_class.set_origin_points((0, 99), (0, 99))
    hsv_class = image_class.rgb_to_hsv()
    mask_class = hsv_class.make_mask(BLUE_LOWER, BLUE_UPPER)
    corners = mask_class.find_corners()
    fix1_class = image_class.fix_perspective(corners, (10, 10), (24, 24))
    fix1_mapa = mapa.Mapa.from_image(fix1_class.img, (10, 10), (24, 24))
    map_image = image.Image.from_map(fix1_mapa)
    try:
      
      p._find_ball_pos(fix1_mapa.m)
      p.map_img = map_image.img.copy()
      time.sleep(0.5)
      
      cv.imshow("or", img)

      #p.queue.append(p.ball_pos)
      path = p.test(p.matrix, p.ball_pos)
      for x, y in path:
        p.map_img[y*10:(y+1)*10-1, x*10:(x+1)*10-1] = (0, 255, 255)
      cv.imshow("mapimg", p.map_img)
      p.instructions_list = []
      for i in range(len(path)-1):
        change = (path[i+1][1] - path[i][1],path[i+1][0] - path[i][0])
        p.instructions_list.append(dir_changes_dict[change])
        
      print(p.instructions_list)
      while p.instructions_list != []:
        if p.execute_next():
          cv.imshow("frame successful", map_image.img)
          cv.imshow("undistorted", fix1_class.img)
          cv.imshow("original", frame)
          time.sleep(0.6)
          
    except Exception as e:
      time.sleep(0.05)
      # cv.imshow("frame failed", map_image.img)
      # cv.imshow("undistorted", fix1_class.img)
      # cv.imshow("original", frame)
      # cv.imshow("frame successful", map_image.img)
      # cv.imshow("or", img)
      print(traceback.format_exc())

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()
