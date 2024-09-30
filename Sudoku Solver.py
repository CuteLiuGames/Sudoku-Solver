from turtle import Screen, Turtle, _CFG
import turtle
from tkinter import *
import tkinter
import random
import math
import time

class Sudoku:
	def __init__(self, N, K):
		self.N = N
		self.K = K

		# Compute square root of N
		SRNd = math.sqrt(N)
		self.SRN = int(SRNd)
		self.mat = [[0 for _ in range(N)] for _ in range(N)]
	
	def fillValues(self):
		# Fill the diagonal of SRN x SRN matrices
		self.fillDiagonal()

		# Fill remaining blocks
		self.fillRemaining(0, self.SRN)

		# Remove Randomly K digits to make game
		self.removeKDigits()
	
	def fillDiagonal(self):
		for i in range(0, self.N, self.SRN):
			self.fillBox(i, i)
	
	def unUsedInBox(self, rowStart, colStart, num):
		for i in range(self.SRN):
			for j in range(self.SRN):
				if self.mat[rowStart + i][colStart + j] == num:
					return False
		return True
	
	def fillBox(self, row, col):
		num = 0
		for i in range(self.SRN):
			for j in range(self.SRN):
				while True:
					num = self.randomGenerator(self.N)
					if self.unUsedInBox(row, col, num):
						break
				self.mat[row + i][col + j] = num
	
	def randomGenerator(self, num):
		return math.floor(random.random() * num + 1)
	
	def checkIfSafe(self, i, j, num):
		return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))
	
	def unUsedInRow(self, i, num):
		for j in range(self.N):
			if self.mat[i][j] == num:
				return False
		return True
	
	def unUsedInCol(self, j, num):
		for i in range(self.N):
			if self.mat[i][j] == num:
				return False
		return True
	
	
	def fillRemaining(self, i, j):
		# Check if we have reached the end of the matrix
		if i == self.N - 1 and j == self.N:
			return True
	
		# Move to the next row if we have reached the end of the current row
		if j == self.N:
			i += 1
			j = 0
	
	# Skip cells that are already filled
		if self.mat[i][j] != 0:
			return self.fillRemaining(i, j + 1)
	
		# Try filling the current cell with a valid value
		for num in range(1, self.N + 1):
			if self.checkIfSafe(i, j, num):
				self.mat[i][j] = num
				if self.fillRemaining(i, j + 1):
					return True
				self.mat[i][j] = 0
		
		# No valid value was found, so backtrack
		return False

	def removeKDigits(self):
		count = self.K

		while (count != 0):
			i = self.randomGenerator(self.N) - 1
			j = self.randomGenerator(self.N) - 1
			if (self.mat[i][j] != 0):
				count -= 1
				self.mat[i][j] = 0
	
		return

	def printSudoku(self):
		for i in range(self.N):
			for j in range(self.N):
				print(self.mat[i][j], end=" ")
			print()

# Driver code
if __name__ == "__main__":
	N = 9
	K = 40
	sudoku = Sudoku(N, K)
	sudoku.fillValues()


sudoku_list = sudoku.mat
original_list = []
temp_list = []
errors = []
chunk_width = 3
chunk_height = 3

selected_x = -1
selected_y = -1

def print_sudoku(s_list):
    for i in range(len(s_list)):
        for j in range(len(s_list[i])):
            if s_list[i][j] == 0:
                print(".", end=" ")
            else:
                print(s_list[i][j], end=" ")
        print()

def reset_pen():
   turtle.clear()
   turtle.delay(0)
   turtle.speed(0)
   turtle.hideturtle()
   turtle.penup()
   
        
def print_sudoku_gui(s_list, errs, sx, sy):
    global sudoku_list
    reset_pen()
    turtle.pencolor("black")
    for i in range(len(s_list)):
        for j in range(len(s_list[i])):
             if sx == j and sy == i:
                     turtle.setpos(j*30 - 135,(i-1)*-30 + 135)
                     turtle.fillcolor("#FFFF00")
                     turtle.begin_fill()
                     for u in range(4): 
                            turtle.forward(30) 
                            turtle.right(90) 
                     turtle.end_fill()
                     turtle.setpos(j*30 + 16 + - 135,i*-30 + 2 + 135)
             elif errs[i][j] and sudoku_list[i][j] != s_list[i][j]:
                        turtle.setpos(j*30 - 135,(i-1)*-30 + 135)
                        turtle.fillcolor("#FF0000")
                        turtle.begin_fill()
                        for u in range(4): 
                            turtle.forward(30) 
                            turtle.right(90) 
                        turtle.end_fill()
                        turtle.setpos(j*30 + 16 + - 135,i*-30 + 2 + 135)
    
    for i in range(len(s_list) + 1):
        turtle.setpos(0 - 135,(i-1)*-30 + 135)
        turtle.pendown()
        turtle.setpos(len(s_list[0])*30 - 135,(i-1)*-30 + 135)
        turtle.penup()
        turtle.setpos(i*30 - 135, 30 + 135)
        turtle.pendown()
        turtle.setpos(i*30 - 135, (len(s_list)-1)*-30 + 135)
        turtle.penup()
           
    for i in range(len(s_list)):
        for j in range(len(s_list[i])):
            if s_list[i][j] == 0:
                continue
            else:
                turtle.setpos(j*30 + 16 + - 135,i*-30 + 2 + 135)
                if errs[i][j] and sudoku_list[i][j] != s_list[i][j] and not (sx == j and sy == i):
                        turtle.pencolor("white")
                elif sudoku_list[i][j] != s_list[i][j] and not (sx == j and sy == i):
                        turtle.pencolor("blue")
                else:
                        turtle.pencolor("black")
                turtle.write(s_list[i][j], move=False, align='center', font=('Arial', 16, 'normal'))

def check_sudoku(s_list, px, py, chunkW, chunkH, numberToUse):
    correct = True
    error = False
    if numberToUse == 0:
        return error
    chunkX = int(px / chunkW) * chunkW
    chunkY = int(py / chunkH) * chunkH
    for u in range(len(s_list[py])):
        if u == px:
            continue
        else:
            if s_list[py][u] != 0:
                if s_list[py][u] == numberToUse:
                    error = True
                    correct = False
                    #print(numberToUse, end = " ")
                    #print("in", end = " (")
                    #print(px, end = ", ")
                    #print(py, end = "): ")
                    #print("Error in X")

    for u in range(len(s_list)):
        if u == py:
            continue
        else:
            if s_list[u][px] != 0:
                if s_list[u][px] == numberToUse:
                    error = True
                    correct = False
                    #print(numberToUse, end = " ")
                    #print("in", end = " (")
                    #print(px, end = ", ")
                    #print(py, end = "): ")
                    #print("Error in Y")
    for y in range(chunkH):
        for x in range(chunkW):
            if((x + chunkX) == px) and ((y + chunkY) == py):
                continue
            else:
                if s_list[y + chunkY][x + chunkX] != 0:
                  if s_list[y + chunkY][x + chunkX] == numberToUse:
                    error = True
                    correct = False
                    #print(numberToUse, end = " ")
                    #print("in", end = " (")
                    #print(px, end = ", ")
                    #print(py, end = "): ")
                    #print("Error in chunk")
    return error
                    
def sudoku_full_check(s_list, x, y):
    global errors
    errors = []
    for i in range(len(s_list)):
        temp = []
        for j in range(len(s_list[i])):
            temp.append(check_sudoku(s_list, j, i, x, y, s_list[i][j]))
        errors.append(temp)

def start_pos(table):
    for x in range(len(table)):
        for y in range(len(table[x])):
            if table[x][y] == 0:
                return x, y
        return False, False

def value(table,x,y,cx,cy):
    i,j = x//cx, y//cy
    grid = [table[i*cx+r][j*cy+c] for r in range(cx) for c in range(cy)]
    v = set([x for x in range(1,10)]) - set(grid) - set(table[x]) - \
            set(list(zip(*table))[y])
    return list(v)

def get_next(table,x,y,cx,cy):
    for next_y in range(y+1, len(table)):
        if table[x][next_y] == 0:
            return x, next_y
    for next_x in range(x+1, len(table[y])):
        for next_y in range(0,len(table)):
            if table[next_x][next_y] == 0:
                return next_x, next_y
    return -1, -1
        

def solve_sudoku(table,x,y,cx,cy):
    for v in value(table,x,y,cx,cy):
        table[x][y] = v
        nx, ny = get_next(table,x,y,cx,cy)
        if ny == -1:
            return True
        else:
            end = solve_sudoku(table,nx,ny,cx,cy)
            if end:
                return True
            table[x][y] = 0

def start(table, cx, cy):
    x, y = start_pos(table)
    solve_sudoku(table,x,y,cx,cy)
    return table


WIDTH, HEIGHT = 360, 360

_CFG.update({"canvwidth": 380, "canvheight": 380})  # 400 - 20

screen = Screen()
screen.setup(400, 400)
screen.cv._rootwindow.resizable(False, False)

turtle.screensize(WIDTH, HEIGHT)
turtle.reset()
turtle.title("Sudoku 數獨破解程式")
turtle.delay(0)
turtle.speed(0)
reset_pen()


#start
def get_sudoku():
  global selected_x, selected_y, sudoku_list, original_list, temp_list
  N = 9
  K = 40
  sudoku = Sudoku(N, K)
  sudoku.fillValues()
  original_list = sudoku.mat
  sudoku_list = sudoku.mat
  chunk_width = 3
  chunk_height = 3
  #print_sudoku(sudoku_list)
  sudoku_full_check(sudoku_list, chunk_width, chunk_height)
  selected_x = -1
  selected_y = -1
  print_sudoku_gui(sudoku_list, errors, selected_x, selected_y)

  temp_list = []
  for i in range(len(sudoku_list)):
           temps = []
           for j in range(len(sudoku_list[i])):
                   temps.append(sudoku_list[i][j])
           temp_list.append(temps)


def solve():
  global selected_x, selected_y, sudoku_list, original_list, temp_list
  sudoku_list = start(original_list, chunk_width, chunk_height)
  #print_sudoku(sudoku_list)
  sudoku_full_check(sudoku_list, chunk_width, chunk_height)
  selected_x = -1
  selected_y = -1
  print_sudoku_gui(sudoku_list, errors, selected_x, selected_y)

  temp_list = []  
  for i in range(len(sudoku_list)):
           temps = []
           for j in range(len(sudoku_list[i])):
                   temps.append(sudoku_list[i][j])
           temp_list.append(temps)

def check():
  global selected_x, selected_y, temp_list
  sudoku_full_check(temp_list, chunk_width, chunk_height)
  selected_x = -1
  selected_y = -1
  print_sudoku_gui(temp_list, errors, selected_x, selected_y)

def fast_check():
  global selected_x, selected_y, temp_list
  sudoku_full_check(temp_list, chunk_width, chunk_height)

def button(x,y):
        global selected_x, selected_y, temp_list
        for i in range(len(temp_list)):
           for j in range(len(temp_list[i])):
                if x >= (j*30 - 135) and x < ((j+1)*30 - 135) and y < ((i-1)*-30 + 135) and y >= ((i)*-30 + 135):
                   if sudoku_list[i][j] == 0:
                     if selected_x == j and selected_y == i:
                        u = temp_list[i][j]
                        u = u + 1
                        if u > 9:
                              u = 1
                        temp_list[i][j] = u
                     elif temp_list[i][j] != temp_list[selected_y][selected_x]:
                        fast_check()
                     selected_x = j
                     selected_y = i
                     print_sudoku_gui(temp_list, errors, selected_x, selected_y)
                     return

get_sudoku()
root = turtle.Screen()._root
btn = Button(root, text="出題", font=('Arial',12,'normal'), command=get_sudoku)
btn2 = Button(root, text="解題", font=('Arial',12,'normal'),  command=solve)
btn3 = Button(root, text="檢查", font=('Arial',12,'normal'),  command=check)
btn.place(x=WIDTH/2 - 70, y=HEIGHT/2 + 150)
btn2.place(x=WIDTH/2, y=HEIGHT/2 + 150)
btn3.place(x=WIDTH/2 + 70, y=HEIGHT/2 + 150)
turtle.onscreenclick(button, 1, add=False)
turtle.mainloop()
