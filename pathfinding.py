import time
import numpy as np



class CellType:
  FIELD = 0 # prazno dostupno polje
  WALL = 1
  BALL = 2
  START = 3
  GOAL = 4

dir_changes_dict = {
  (-1, 0): "down", 
  ( 1, 0): "up",
  
  (0, -1): "right",
  (0,  1): "left",
  
  (-1, -1): "dright",
  (-1,  1): "dleft",
  ( 1, -1): "uright",
  ( 1,  1): "uleft"
  
}
class Pathfinding:
  
  matrix = None # expected to be 24x24
  visited = None
  ball_pos = None
  instructions_list = None
  finished = None
  goal_pos = None

  def __init__(self, _matrix) -> None:
    self.finished = False
    self.matrix = _matrix #TODO: check if no copy works better (e.g. no need for reseting)
    self.visited = np.zeros((24,24), dtype=int) 
    self.instructions_list = []
    self._find_ball_pos(self.matrix)

  def bfs(self, queue, depth = -1):
    current_pos = queue.pop(0)
    self.visited[current_pos[0], current_pos[1]] = depth
    # Debug kod koji ispisuje svaki korak
    #self._print_m(self.visited)

    for offset_x in np.arange(-1, 2):
      for offset_y in np.arange(-1, 2):
        if self._check_constrains(current_pos,(offset_x, offset_y)):
          i = current_pos[0] + offset_x
          j = current_pos[1] + offset_y
          if offset_x == 0 and offset_y == 0:
            continue

          if not self.finished: # Checks if maze was solved in other leaves 
            if self.visited[i][j] == 0: # Checks if current field was visited before
              if self.matrix[i][j] == CellType.FIELD:
                self.visited[i][j] = depth-1
                queue.append((i,j))
                self.bfs(queue.copy(),depth-1)
              
              elif self.matrix[i][j] == CellType.GOAL:
                self.visited[i][j] = depth-1
                self.finished = True
                self.goal_pos = (i,j)
                return

  def backtrack(self):
    self.instructions_list = []
    cursor = self.goal_pos
    pos_changes = []
    print(self._print_m(self.visited))
    while True:
      i = cursor[0]
      j = cursor[1]
      for offset_x in np.arange(-1,2):
        for offset_y in np.arange(-1, 2):
          if self.visited[i][j] < self.visited[i+offset_x][j+offset_y] and self.visited[i+offset_x][j+offset_y] != 0:
            next = (i+offset_x, j+offset_y)
            print(next, self.visited[i+offset_x, j+offset_y])
      
      pos_changes.append((next[0]-i, next[1]-j))
      if next[0] == self.ball_pos[0] and next[1] == self.ball_pos[1]:

        #TODO: mozda treba jos nesto ovde
        break
      cursor = next
    print(pos_changes)

    self.instructions_list = self._generate_instruction_list(pos_changes)

  @staticmethod
  def _generate_instruction_list(pos_changes):
    for change in pos_changes[::-1]:
      print(dir_changes_dict[change])

  def _find_ball_pos(self, matrix) -> None:
    '''Finds the position of the ball'''
    for i, row in enumerate(matrix):
      for j, _ in enumerate(matrix[i]):
        if matrix[i][j] == CellType.BALL:
          self.ball_pos = (i,j)

  def _check_constrains(self, current, offset):
    '''Check if given field is withing matrix dimensions'''
    if current[0]+offset[0] >= 0 and current[0]+offset[0] <= 4:
      if current[1]+offset[1] >= 0 and current[1]+offset[1] <= 4:
        return True

    return False
  
  @staticmethod
  def _print_m(m):
    '''QOL - prints out matrix (m)'''
    print()
    for i in range(5):
      for j in range(5):
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

def test():
  for _ in range(0,1):
    start = time.time()
    test = [[0, 0, 0, 1, 2],
            [0, 1, 0, 1, 0],
            [0, 1, 4, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]]
    p = Pathfinding(test)
    p.bfs([(0,4)], -1)
    p.backtrack()
    stop = time.time()
    print(f"took {(stop-start)*100000}ms")

test()