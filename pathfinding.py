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
  START = 3
  GOAL = 4


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

dir_changes_dict2 = {
  (-1, 0): "./esp-left.sh", 
  ( 1, 0): "./esp-right.sh",
  
  (0, -1): "./esp-up.sh",
  (0,  1): "./esp-down.sh",
  
  (-1, -1): "./esp-dright.sh",
  (-1,  1): "./esp-uright.sh",
  ( 1, -1): "./esp-dleft.sh",
  ( 1,  1): "./esp-uleft.sh"
}

class Pathfinding:
  
  matrix = None # expected to be 24x24
  visited = None
  ball_pos = None
  instructions_list = None
  finished = None
  goal_pos = None

  path_chosen = None
  queue = None

  last_command = None
  command = None
  def __init__(self, _matrix) -> None:
    self.finished = False
    self.matrix = _matrix #TODO: check if no copy works better (e.g. no need for reseting)
    self.visited = np.zeros((24,24), dtype=int) 
    self.instructions_list = list()
    self.queue = list()
    self.path_chosen = list()
    self._find_ball_pos()

  def bfs(self, depth=-1):
    current_pos = self.queue.pop(0)
    self.visited[current_pos[0]][current_pos[1]] = depth
    # Debug kod koji ispisuje svaki korak
    #self._print_m(self.matrix+self.visited)
    #time.sleep(0.15)
    lookup = [(-1, 0), (-1,-1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    random.shuffle(lookup)
    for offset_x, offset_y in lookup:
        if self._check_constrains(current_pos,(offset_x, offset_y)):
          i = current_pos[0] + offset_x
          j = current_pos[1] + offset_y

          if not self.finished: # Checks if maze was solved in other leaves 
            if self.visited[i][j] == 0: # Checks if current field was visited before
              if self.matrix[i][j] == CellType.GOAL or self.matrix[i][j] == CellType.BALL:
                self.visited[i][j] = depth-1
                self.finished = True
                self.goal_pos = (i,j)
                return

              elif self.matrix[i][j] == CellType.FIELD:
                self.visited[i][j] = depth-1
                self.queue.append((i,j))
    
    self.bfs(depth-1)


  def backtrack(self):
    cursor = self.goal_pos
    pos_changes = []
    while True:
      i = cursor[0]
      j = cursor[1]
      for offset_x in np.arange(-1,2):
        for offset_y in np.arange(-1, 2):
          if self._check_constrains(cursor, (offset_x, offset_y)):
            if self.visited[i][j] < self.visited[i+offset_x][j+offset_y] and self.visited[i+offset_x][j+offset_y] != 0:
              next = (i+offset_x, j+offset_y)
              #print(next, self.visited[i+offset_x, j+offset_y])
      pos_changes.append((next[0]-i, next[1]-j))
      self.path_chosen.append((next[0], next[1]))
      if next[0] == self.ball_pos[0] and next[1] == self.ball_pos[1]:

        break
      cursor = next
    #print(pos_changes)
    
    self._generate_instruction_list(pos_changes)

  
  def _generate_instruction_list(self, pos_changes):
    for change in pos_changes[::-1]:
      self.instructions_list.append(dir_changes_dict2[change])
    return self.instructions_list

  def _find_ball_pos(self) -> None:
    '''Finds the position of the ball'''
    for i, row in enumerate(self.matrix):
      for j, _ in enumerate(self.matrix[i]):
        if self.matrix[i][j] == CellType.BALL:
          self.ball_pos = (i,j)

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
    #print(f"{command} -> {os.system(command)}")
    #print(f"stopping -> {os.system('./esp-stop.sh')}")
    os.system('./esp-stop.sh')
    #time.sleep(0.1)
    print(f"{self.command} -> {os.system(self.command)}")
    return True

vid = cv.VideoCapture(0)
calibration = np.load('rig/calib.npz')
mtx = calibration['mtx']
dist = calibration['dist']
rvecs = calibration['rvecs']
tvecs = calibration['tvecs']

while(True):
    ret, frame = vid.read()
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    ##cv.imshow("frame", frame)

    try:
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

      ##cv.imshow('frame', frame)
      #time.sleep(2)
      p = Pathfinding(fix1_mapa.m)
      p.visited = np.zeros((24,24), dtype=int)
      p.queue.append(p.ball_pos)
      p.bfs(depth=-1)
      
      p.backtrack()
      while p.instructions_list != []:
        if p.execute_next():
          cv.imshow("frame successful", map_image.img)
          cv.imshow("undistorted", fix1_class.img)
          cv.imshow("original", frame)
          #time.sleep(3)
          break
    except Exception as e:
      #time.sleep(0.05)
      #cv.imshow("frame failed", map_image.img)
      #cv.imshow("undistorted", fix1_class.img)
      #cv.imshow("original", frame)
      print(traceback.format_exc())

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()
