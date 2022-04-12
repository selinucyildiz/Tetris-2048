import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 35 * grid_w
   stddraw.setCanvasSize((40 * grid_w) + 120, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w+5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w

   # create the game grid
   grid = GameGrid(grid_h, grid_w)

   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   # current_tetromino = create_tetromino(grid_h, grid_w)
   #next_tetromino = create_tetromino(grid_h,grid_w)
   first_tetro_list1 = create_tetromino(grid_h,grid_w)
   second_tetro_list2 = create_tetromino(grid_h, grid_w)
   new_list = [first_tetro_list1,second_tetro_list2]
   grid.new_list = new_list
   current_tetromino = new_list[0]
   grid.current_tetromino = current_tetromino

   new_list.pop(0)

   new_list.append(create_tetromino(grid_h,grid_w))

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid, grid_h, grid_w + 5.6)

   already_dropped = False
   drop = False

   pause = False
   # main game loop (keyboard interaction for moving the tetromino) 
   while True:
      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()
         # Pause
         if key_typed == 'p':
            print("Pause")
            if pause:
               pause = False
            else:
               pause = True
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

         if not pause:
           # check user interactions via the keyboard
           if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
              key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
           # if the left arrow key has been pressed
           if key_typed == "left":
            # move the active tetromino left by one
              current_tetromino.move(key_typed, grid) 
           # if the right arrow key has been pressed
           elif key_typed == "right":
              # move the active tetromino right by one
              current_tetromino.move(key_typed, grid)
           # if the down arrow key has been pressed
           elif key_typed == "down":
              # move the active tetromino down by one 
              # (soft drop: causes the tetromino to fall down faster)
              current_tetromino.move(key_typed, grid)
           elif key_typed == "space":
            # Moves down the tetromino all the way down until it cannot go further
            if not already_dropped:
               while True:
                  sc = current_tetromino.move("down", grid)
                  if not sc:
                     break
               dropped = True

           elif key_typed == "up":
              current_tetromino.reverseTurnTetromino(grid)

           elif key_typed == "z":
              current_tetromino.turnTetromino(grid)

           # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      if not pause:
         success = current_tetromino.move("down", grid)

      # place the tetromino on the game grid when it cannot go down anymore
      if not success and not pause:
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)

         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            show_gameOver(grid_w+4, grid_h-1.5)
            break
      
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         #current_tetromino = create_tetromino(grid_h, grid_w)
         #grid.current_tetromino = new_list[0]
         current_tetromino = new_list[1]
         grid.current_tetromino = current_tetromino
         new_list.pop(0)
         new_list.append(create_tetromino(grid_h,grid_w))

            
      # display the game grid and the current tetromino      
      grid.clear()
      # display the game grid and as well the current tetromino 
      grid.display(pause)

   # print a message on the console when the game is over
   print("Game over")
  
# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'Z' , 'T' , 'S' ,'J', 'L','I', 'O' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino


def show_gameOver(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__ ))
   # path of the image file
   img_file = current_dir + "/images/gameover.jpg"
   # center coordinates to display the image
   img_center_x, img_center_y = ((grid_width - 1) / 2) - 0.4, grid_height - 6
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # center coordinates to display the image
   img_center_x, img_center_y = ((grid_width - 1) / 2) - 0.4, grid_height - 6
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)

   while True:
      # display the menu and wait for a short time (50 ms)
      # menüyü görüntüleyin ve kısa bir süre bekleyin (50 ms)
      stddraw.show(50)
def display_game_menu(grid, grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(stddraw.WHITE)
   text_to_display = "Choose Level and Start Game"
   stddraw.text(img_center_x, 7, text_to_display)
   #Easy
   stddraw.setPenColor(stddraw.GREEN)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w/3, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(stddraw.BLACK)
   text_to_display1 = "Easy"
   stddraw.text(2.7, 5, text_to_display1)
   #Medium
   stddraw.setPenColor(stddraw.YELLOW)
   stddraw.filledRectangle(5.25, button_blc_y, button_w / 3, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(stddraw.BLACK)
   text_to_display2 = "Medium"
   stddraw.text(7.75, 5, text_to_display2)
   #Hard
   stddraw.setPenColor(stddraw.RED)
   stddraw.filledRectangle(10.2, button_blc_y, button_w / 3, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(stddraw.BLACK)
   text_to_display3 = "Hard"
   stddraw.text(12.75, 5, text_to_display3)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               grid.setSpeed_slower()
               break # break the loop to end the method and start the game
         if mouse_x >= 5.25 and mouse_x <= 5.25 + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break
         if mouse_x >= 10.2 and mouse_x <= 10.2 + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               grid.setSpeed_faster()
               break
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               grid.setSpeed_slower()
               break # break the loop to end the method and start the game
         if mouse_x >= 5.25 and mouse_x <= 5.25 + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break
         if mouse_x >= 10.2 and mouse_x <= 10.2 + button_w/3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               grid.setSpeed_faster()
               break

# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()