import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import random
from tetromino import Tetromino

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # the tetromino that is currently ghost
      self.current_ghost = None
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.next_tetromino = None
      self.new_list = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(214,205, 196)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(150, 121, 105)
      self.boundary_color = Color(158,138,120)
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.002
      self.box_thickness = 7 * self.line_thickness
      # score
      self.score = 0
      # Check reached 2046 to win
      self.reached2048 = False
      # to show next tetrominos

      self.speed = 250

   # Method used for displaying the game grid
   def display(self, pause):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current (active) tetromino ghost
      if self.current_ghost is not None:
         self.current_ghost.draw()
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()

      self.showPiece(self.new_list)
      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(self.speed)
      if(pause):
         stddraw.setPenColor(stddraw.BLACK)
         stddraw.setFontSize(32)
         stddraw.text(self.grid_width/2,self.grid_height/2,"Game is paused")
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(self.speed)

            
   def setSpeed_slower(self):
      self.speed = self.speed * 1.2

   def setSpeed_faster(self):
      self.speed = self.speed / 5
         
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      #Eliminate gaps
      self.delete_tile()
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

      stddraw.setPenColor(self.empty_cell_color)
      stddraw.filledRectangle(13.5,3,5,4)

      # SCORE
      stddraw.setFontSize(26)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 1.5, "SCORE")
      stddraw.boldText(self.grid_width + 2.45, self.grid_height - 2.5, str(self.score))

      # Controls
      stddraw.setFontSize(16)
      stddraw.setPenColor(stddraw.DARK_GRAY)
      stddraw.boldText(self.grid_width + 2.4, self.grid_height - 7.8, "Controls")

      stddraw.setFontSize(10)
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 8.5, "Left Key(←) to left on")
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 9, "Right Key(→) to right on")
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 9.5, "P to Pause")
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 10, "Up Key(↑) to Rotate (Clockwise)")
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 10.5, "Z to Rotate (Anti-Clockwise)")
      stddraw.boldText(self.grid_width + 2.3, self.grid_height - 11,"Space to drop tetromino")

      stddraw.setFontSize(26)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.boldText(self.grid_width+2, self.grid_height-14.5 , "NEXT")
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   def clear(self):
      lines =[] # empty list
      for i in range(self.grid_height):
         if None not in self.tile_matrix[i]: # içeriwide boş yoksa
            lines.append(i - len(lines)) # satırlar aşağı indikçe silsin diye indexleri ona uygun tut

      for row in lines:
         self.tile_matrix = np.delete(self.tile_matrix, (row), axis=0) # dolu olan satırları tilematrixten sil
         self.tile_matrix = np.append(self.tile_matrix, np.full((1, self.grid_width), None), axis=0) # üste boş satır ekle

   def showPiece(self,list):
      stddraw.setPenColor(stddraw.BLACK)
      list[1].show_next_tetromino()

   # Method used for checking whether the cell with given row and column indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      self.merge()
      self.check_grid()
      
      # return the game_over flag
      return self.game_over
   
   def check_grid(self):
      for row in range(self.grid_width):
         if None not in self.tile_matrix[row]:
            self.delete_row(row)
            self.move_row(row)
            self.check_grid()

   def delete_row(self,row):
      for i in range(self.grid_width):
         newScore = self.tile_matrix[row][i].number
         self.score += newScore

      self.tile_matrix = np.delete(self.tile_matrix,row,axis=0)
      self.tile_matrix = np.append(self.tile_matrix, np.reshape(np.full(self.grid_width,[None]),(-1,self.grid_width)),axis=0)


   def move_row(self,row):
      for row_i in range(row,self.grid_height):
         for col_i in range(self.grid_width):
            if self.tile_matrix[row_i][col_i] != None:
               self.tile_matrix[row_i][col_i].move(0,-1)

   def move_column(self,col,row):
      for row_i in range(row,self.grid_height):
         if self.tile_matrix[row_i][col] != None:
            self.tile_matrix[row_i][col].move(0,-1)
      transposed = self.tile_matrix.transpose()
      deleted = np.delete(transposed[col],row)
      transposed[col] = np.append(deleted,[None],axis=0)
      self.tile_matrix = transposed.transpose()

   def merge(self):
      for row_i in range(self.grid_height-1):
         for col_i in range(self.grid_width ):
            if self.tile_matrix[row_i][col_i] != None and self.tile_matrix[row_i+1][col_i] != None:
               if self.tile_matrix[row_i][col_i].number == self.tile_matrix[row_i+1][col_i].number:
                  self.score += self.tile_matrix[row_i][col_i].number * 2
                  self.tile_matrix[row_i][col_i].double()
                  self.tile_matrix[row_i+1][col_i] = None
                  self.move_column(col_i,row_i+1)
                  self.merge()

# Eliminate gaps
   def delete_tile(self):
      n_rows, n_cols = len(self.tile_matrix), len(self.tile_matrix[0])
      for row in range(1, n_rows - 1):
         for col in range(n_cols-1):
               if self.tile_matrix[row][col] != None:
                  if self.tile_matrix[row+1][col] == None:
                     if self.tile_matrix[row-1][col] == None:
                           if self.tile_matrix[row][col-1] == None:
                              if self.tile_matrix[row][col+1] == None:
                                 newScore = self.tile_matrix[row][col].number
                                 self.score += newScore
                                 self.tile_matrix[row][col] = None
                  #Recursive
                                 self.delete_tile()
