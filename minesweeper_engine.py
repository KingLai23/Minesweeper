#MINESWEEPER ENGINE
import random

class minesweeper_engine:
    def __init__(self, row, col):
        self.marked_mines = []
        self.finished_tiles = []
        self.row = row
        self.col = col
        
        for i in range (self.row):
            self.marked_mines.append([])
            self.finished_tiles.append([])
            for j in range (self.col):
                self.marked_mines[i].append(False)
                self.finished_tiles[i].append(False)
        
    def detectMine(self, grid_unopened, grid_values):
        self.minesAroundCell(grid_unopened, grid_values)
        self.oneTwoOneHoriz(grid_unopened, grid_values)
        self.oneTwoOneVert(grid_unopened, grid_values)
        self.twoThreeTwoHorz(grid_unopened, grid_values)
        self.twoThreeTwoVert(grid_unopened, grid_values)
        self.twoThreeOne(grid_unopened, grid_values)
        self.oneTwoTwoOneHorz(grid_unopened, grid_values)
        self.oneTwoTwoOneVert(grid_unopened, grid_values)
        to_open = self.openGuaranteed(grid_unopened, grid_values)
        if (to_open == []):
            to_open = self.makeRandomMove(grid_unopened)
            
        print(to_open)
            
        return to_open
    
    def makeRandomMove(self, grid_unopened):
        r,c = random.randint(0,self.row-1), random.randint(0,self.col-1)
        found = not (grid_unopened[r][c] or self.marked_mines[r][c])
        
        while not found:
            r,c = random.randint(0,self.row-1), random.randint(0,self.col-1)
            found = not (grid_unopened[r][c] or self.marked_mines[r][c]) 
            
        return [[r,c]]        
    
    def minesAroundCellOLD(self, grid_unopened, grid_values):        
        for i in range (self.row):
            for j in range (self.col):
                if grid_unopened[i][j] and not self.finished_tiles[i][j]:
                    num_guarantee,neighbours = 0,0
                    num = grid_values[i][j]
                    maybe = []
                    
                    if (i-1 > -1 and j-1 > -1):
                        neighbours+=1
                        if grid_unopened[i-1][j-1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i-1, j-1])
                    if (i-1 > -1):
                        neighbours+=1
                        if grid_unopened[i-1][j]:
                            num_guarantee+=1
                        else:
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        neighbours+=1
                        if grid_unopened[i-1][j+1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i-1, j+1])
                    if (j-1 > -1):
                        neighbours+=1
                        if grid_unopened[i][j-1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i, j-1])
                    if (j+1 < self.col):
                        neighbours+=1
                        if grid_unopened[i][j+1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i, j+1])
                    if (i+1 < self.row and j-1 > -1):
                        neighbours+=1
                        if grid_unopened[i+1][j-1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i+1, j-1])
                    if (i+1 < self.row):
                        neighbours+=1
                        if grid_unopened[i+1][j]:
                            num_guarantee+=1
                        else:
                            maybe.append([i+1, j])
                    if (i+1 < self.row and j+1 < self.col):
                        neighbours+=1
                        if grid_unopened[i+1][j+1]:
                            num_guarantee+=1
                        else:
                            maybe.append([i+1, j+1])
                    
                    if neighbours - num_guarantee == num:
                        for coord in maybe:
                            self.marked_mines[coord[0]][coord[1]] = True
  
        
    def minesAroundCell(self, grid_unopened, grid_values):        
        for i in range (self.row):
            for j in range (self.col):
                if grid_unopened[i][j] and not self.finished_tiles[i][j]:
                    num = grid_values[i][j]
                    maybe = []
                    
                    if (i-1 > -1 and j-1 > -1):
                        if not grid_unopened[i-1][j-1]:
                            maybe.append([i-1, j-1])
                    if (i-1 > -1):
                        if not grid_unopened[i-1][j]:
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        if not grid_unopened[i-1][j+1]:
                            maybe.append([i-1, j+1])
                    if (j-1 > -1):
                        if not grid_unopened[i][j-1]:
                            maybe.append([i, j-1])
                    if (j+1 < self.col):
                        if not grid_unopened[i][j+1]:
                            maybe.append([i, j+1])
                    if (i+1 < self.row and j-1 > -1):
                        if not grid_unopened[i+1][j-1]:
                            maybe.append([i+1, j-1])
                    if (i+1 < self.row):
                        if not grid_unopened[i+1][j]:
                            maybe.append([i+1, j])
                    if (i+1 < self.row and j+1 < self.col):
                        if not grid_unopened[i+1][j+1]:
                            maybe.append([i+1, j+1])
                    
                    if len(maybe) == num:
                        for coord in maybe:
                            self.marked_mines[coord[0]][coord[1]] = True
    
    def openGuaranteed(self, grid_unopened, grid_values):
        to_open = []
        
        for i in range (self.row):
            for j in range (self.col):
                if grid_unopened[i][j] and not self.finished_tiles[i][j]:
                    found_mines = 0
                    num = grid_values[i][j]
                    maybe = []
                    if (i-1 > -1 and j-1 > -1):
                        if self.marked_mines[i-1][j-1]:
                            found_mines+=1
                        elif (not grid_unopened[i-1][j-1]):
                            maybe.append([i-1,j-1])
                    if (i-1 > -1):
                        if self.marked_mines[i-1][j]:
                            found_mines+=1
                        elif (not grid_unopened[i-1][j]):
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        if self.marked_mines[i-1][j+1]:
                            found_mines+=1
                        elif (not grid_unopened[i-1][j+1]):
                            maybe.append([i-1,j+1])
                    if (j-1 > -1):
                        if self.marked_mines[i][j-1]:
                            found_mines+=1
                        elif (not grid_unopened[i][j-1]):
                            maybe.append([i,j-1])
                    if (j+1 < self.col):
                        if self.marked_mines[i][j+1]:
                            found_mines+=1
                        elif (not grid_unopened[i][j+1]):
                            maybe.append([i,j+1])
                    if (i+1 < self.row and j-1 > -1):
                        if self.marked_mines[i+1][j-1]:
                            found_mines+=1
                        elif (not grid_unopened[i+1][j-1]):
                            maybe.append([i+1,j-1])
                    if (i+1 < self.row):
                        if self.marked_mines[i+1][j]:
                            found_mines+=1
                        elif (not grid_unopened[i+1][j]):
                            maybe.append([i+1,j])
                    if (i+1 < self.row and j+1 < self.col):
                        if self.marked_mines[i+1][j+1]:
                            found_mines+=1
                        elif (not grid_unopened[i+1][j+1]):
                            maybe.append([i+1,j+1])
                    
                    if found_mines == num:
                        self.finished_tiles[i][j] = True
                        for coord in maybe:
                            to_open.append(coord)
        
        return to_open
    
    def oneTwoOneHoriz(self, grid_unopened, grid_values):
        for i in range(self.row):
            for j in range (self.col-3):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (grid_unopened[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [1,2,1]:
                    if (i+1 == self.row or (grid_unopened[i+1][j] and grid_unopened[i+1][j+2])):
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                            
                        print("ONE-TWO-ONE (H): " + str(i) + "," + str(j+1))
                        
                    elif (i == 0 or (grid_unopened[i-1][j] and grid_unopened[i-1][j+2])):
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True
                            
                        print("ONE-TWO-ONE (H): " + str(i) + "," + str(j+1))
    
        
    def oneTwoOneVert(self, grid_unopened, grid_values):
        for i in range(self.row-3):
            for j in range (self.col):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (grid_unopened[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if row == [1,2,1]:
                    if (j+1 == self.col or (grid_unopened[i][j+1] and grid_unopened[i+2][j+1])):
                        if not self.marked_mines[i][j-1]:
                            self.marked_mines[i][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                            
                        print("ONE-TWO-ONE (V): " + str(i+1) + "," + str(j))
                    elif (j == 0 or (grid_unopened[i][j-1] and grid_unopened[i+2][j-1])):
                        if not self.marked_mines[i][j+1]:
                            self.marked_mines[i][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True
                            
                        print("ONE-TWO-ONE (V): " + str(i+1) + "," + str(j))
                        
                        
    def twoThreeTwoHorz(self, grid_unopened, grid_values):
        for i in range(1, self.row-1):
            for j in range(self.col-3):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (grid_unopened[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [2,3,2]:
                    if grid_unopened[i+1][j] and grid_unopened[i+1][j+2]:
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                        
                        print("TWO_THREE_TWO (H): " + str(i) + "," + str(j+1))
                    
                    elif grid_unopened[i-1][j] and grid_unopened[i-1][j+2]:
                        if not self.marked_mines[i-1][j+1]:
                            self.marked_mines[i-1][j+1] = True
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True 
                        
                        print("TWO_THREE_TWO (H): " + str(i) + "," + str(j+1))
                        
    def twoThreeTwoVert(self, grid_unopened, grid_values):
        for i in range(self.row-3):
            for j in range(1,self.col-1):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (grid_unopened[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if row == [2,3,2]:
                    if grid_unopened[i][j+1] and grid_unopened[i+2][j+1]:
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i][j-1]:
                            self.marked_mines[i][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                        
                        print("TWO_THREE_TWO (V): " + str(i+1) + "," + str(j))
                    
                    elif grid_unopened[i][j-1] and grid_unopened[i+2][j-1]:
                        if not self.marked_mines[i+1][j-1]:
                            self.marked_mines[i+1][j-1] = True
                        if not self.marked_mines[i][j+1]:
                            self.marked_mines[i][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True 
                        
                        print("TWO_THREE_TWO (V): " + str(i+1) + "," + str(j))
                        
    def twoThreeOne(self, grid_unopened, grid_values):
        for i in range(1, self.row-1):
            for j in range(self.col-3):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (grid_unopened[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [2,3,1]:
                    if grid_unopened[i+1][j+1] and grid_unopened[i+1][j+2]:
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                        
                        print("TWO_THREE_ONE: " + str(i) + "," + str(j+1))
                    
    def oneTwoTwoOneHorz(self, grid_unopened, grid_values):
        for i in range(self.row):
            for j in range(self.col-4):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (grid_unopened[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if (grid_unopened[i][j+3] and not self.finished_tiles[i][j+3]):
                    row.append(grid_values[i][j+3])
                    
                if row == [1,2,2,1]:
                    if i+1==self.row or (grid_unopened[i+1][j] and grid_unopened[i+1][j+1] and grid_unopened[i+1][j+2] and grid_unopened[i+1][j+3]):
                        if not self.marked_mines[i-1][j+1]:
                            self.marked_mines[i-1][j+1] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                            
                        print("ONE_TWO_TWO_ONE (H): " + str(i) + "," + str(j+1))
                        
                    if i==0 or (grid_unopened[i-1][j] and grid_unopened[i-1][j+1] and grid_unopened[i-1][j+2] and grid_unopened[i-1][j+3]):
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True
                            
                        print("ONE_TWO_TWO_ONE (H): " + str(i) + "," + str(j+1))
                        
    def oneTwoTwoOneVert(self, grid_unopened, grid_values):
        for i in range(self.row-4):
            for j in range(self.col):
                row = []
                if (grid_unopened[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (grid_unopened[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (grid_unopened[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if (grid_unopened[i+3][j] and not self.finished_tiles[i+3][j]):
                    row.append(grid_values[i+3][j])
                    
                if row == [1,2,2,1]:
                    if j+1==self.col or (grid_unopened[i][j+1] and grid_unopened[i+1][j+1] and grid_unopened[i+2][j+1] and grid_unopened[i+3][j+1]):
                        if not self.marked_mines[i+1][j-1]:
                            self.marked_mines[i+1][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                            
                        print("ONE_TWO_TWO_ONE (V): " + str(i+1) + "," + str(j))
                        
                    if j==0 or (grid_unopened[i][j-1] and grid_unopened[i][j-1] and grid_unopened[i+2][j-1] and grid_unopened[i+3][j-1]):
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True
                            
                        print("ONE_TWO_TWO_ONE (V): " + str(i+1) + "," + str(j))
                    
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        