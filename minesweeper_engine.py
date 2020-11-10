#MINESWEEPER ENGINE
import random

class minesweeper_engine:
    def __init__(self, row, col, mines):
        self.marked_mines = []
        self.potential_mines = []
        self.finished_tiles = []
        self.row = row
        self.col = col
        self.num_mines=mines
        
        for i in range (self.row):
            self.marked_mines.append([])
            self.finished_tiles.append([])
            self.potential_mines.append([])
            for j in range (self.col):
                self.marked_mines[i].append(False)
                self.finished_tiles[i].append(False)
                self.potential_mines[i].append(False)
    
    # MAKING MOVES
    
    def firstMove(self):
        topx = self.row//3
        topy = self.col//3
        
        return random.randint(topx,2*topx), random.randint(topy,2*topy)
    
    
    def makeMove(self, opened_tile, grid_values):
        self.findPatterns(opened_tile, grid_values)

        to_open = self.openGuaranteed(opened_tile, grid_values)
        
        oneFourTwoFiveThreeSix = self.oneFourTwoFiveThreeSix(opened_tile, grid_values)
        
        for coord in oneFourTwoFiveThreeSix:
            if coord not in to_open:
                to_open.append(coord)
        
        if to_open == []:
            choices = self.openFromPotentialMines(opened_tile)
            if choices != []:
                to_open = self.guessTile(choices)
                print("GUESSES AVAILABLE: " + str(choices))            
                
        print(to_open)
        return to_open
   
    def findPatterns(self, opened_tile, grid_values):
        self.minesAroundCell(opened_tile, grid_values)
        self.oneTwoOneHoriz(opened_tile, grid_values)
        self.oneTwoOneVert(opened_tile, grid_values)
        self.twoThreeTwoHorz(opened_tile, grid_values)
        self.twoThreeTwoVert(opened_tile, grid_values)
        self.twoThreeOne(opened_tile, grid_values)
        self.oneTwoTwoOneHorz(opened_tile, grid_values)
        self.oneTwoTwoOneVert(opened_tile, grid_values)
    
    def makeRandomMove(self, opened_tile):
        r,c = random.randint(0,self.row-1), random.randint(0,self.col-1)
        found = not (opened_tile[r][c] or self.marked_mines[r][c])
        
        while not found:
            r,c = random.randint(0,self.row-1), random.randint(0,self.col-1)
            found = not (opened_tile[r][c] or self.marked_mines[r][c]) 
            
        return [[r,c]]        

    def guessTile(self, choices):
        c = random.randint(0,len(choices)-1)
        
        return [choices[c]]
    
    
    # COUNTING MINES AROUND A CELL
    
    def minesAroundCell(self, opened_tile, grid_values):        
        for i in range (self.row):
            for j in range (self.col):
                if opened_tile[i][j] and not self.finished_tiles[i][j]:
                    num = grid_values[i][j]
                    maybe = []
                    
                    if (i-1 > -1 and j-1 > -1):
                        if not opened_tile[i-1][j-1]:
                            maybe.append([i-1, j-1])
                    if (i-1 > -1):
                        if not opened_tile[i-1][j]:
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        if not opened_tile[i-1][j+1]:
                            maybe.append([i-1, j+1])
                    if (j-1 > -1):
                        if not opened_tile[i][j-1]:
                            maybe.append([i, j-1])
                    if (j+1 < self.col):
                        if not opened_tile[i][j+1]:
                            maybe.append([i, j+1])
                    if (i+1 < self.row and j-1 > -1):
                        if not opened_tile[i+1][j-1]:
                            maybe.append([i+1, j-1])
                    if (i+1 < self.row):
                        if not opened_tile[i+1][j]:
                            maybe.append([i+1, j])
                    if (i+1 < self.row and j+1 < self.col):
                        if not opened_tile[i+1][j+1]:
                            maybe.append([i+1, j+1])
                    
                    if len(maybe) == num:
                        for coord in maybe:
                            self.marked_mines[coord[0]][coord[1]] = True
                            
                        if (i-1 > -1 and j-1 > -1):
                            self.potential_mines[i-1][j-1] = False
                        if (i-1 > -1):
                            self.potential_mines[i-1][j] = False
                        if (i-1 > -1 and j+1 < self.col):
                            self.potential_mines[i-1][j+1] = False
                        if (j-1 > -1):
                            self.potential_mines[i][j-1] = False
                        if (j+1 < self.col):
                            self.potential_mines[i][j+1] = False
                        if (i+1 < self.row and j-1 > -1):
                            self.potential_mines[i+1][j-1] = False
                        if (i+1 < self.row):
                            self.potential_mines[i+1][j] = False
                        if (i+1 < self.row and j+1 < self.col):
                            self.potential_mines[i+1][j+1] = False
    
    def openGuaranteed(self, opened_tile, grid_values):
        to_open = []
        
        for i in range (self.row):
            for j in range (self.col):
                if opened_tile[i][j] and not self.finished_tiles[i][j]:
                    found_mines = 0
                    num = grid_values[i][j]
                    maybe = []
                    if (i-1 > -1 and j-1 > -1):
                        if self.marked_mines[i-1][j-1]:
                            found_mines+=1
                        elif (not opened_tile[i-1][j-1]):
                            maybe.append([i-1,j-1])
                    if (i-1 > -1):
                        if self.marked_mines[i-1][j]:
                            found_mines+=1
                        elif (not opened_tile[i-1][j]):
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        if self.marked_mines[i-1][j+1]:
                            found_mines+=1
                        elif (not opened_tile[i-1][j+1]):
                            maybe.append([i-1,j+1])
                    if (j-1 > -1):
                        if self.marked_mines[i][j-1]:
                            found_mines+=1
                        elif (not opened_tile[i][j-1]):
                            maybe.append([i,j-1])
                    if (j+1 < self.col):
                        if self.marked_mines[i][j+1]:
                            found_mines+=1
                        elif (not opened_tile[i][j+1]):
                            maybe.append([i,j+1])
                    if (i+1 < self.row and j-1 > -1):
                        if self.marked_mines[i+1][j-1]:
                            found_mines+=1
                        elif (not opened_tile[i+1][j-1]):
                            maybe.append([i+1,j-1])
                    if (i+1 < self.row):
                        if self.marked_mines[i+1][j]:
                            found_mines+=1
                        elif (not opened_tile[i+1][j]):
                            maybe.append([i+1,j])
                    if (i+1 < self.row and j+1 < self.col):
                        if self.marked_mines[i+1][j+1]:
                            found_mines+=1
                        elif (not opened_tile[i+1][j+1]):
                            maybe.append([i+1,j+1])
                    
                    if found_mines == num:
                        self.finished_tiles[i][j] = True
                        for coord in maybe:
                            to_open.append(coord)
        
        return to_open
    
    
    # FINDING PATTERNS
    
    def oneTwoOneHoriz(self, opened_tile, grid_values):
        for i in range(self.row):
            for j in range (self.col-3):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (opened_tile[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [1,2,1]:
                    if (i+1 == self.row or (opened_tile[i+1][j] and opened_tile[i+1][j+2])):
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                            
                        print("ONE-TWO-ONE (H): " + str(i) + "," + str(j+1))
                        
                    elif (i == 0 or (opened_tile[i-1][j] and opened_tile[i-1][j+2])):
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True
                            
                        print("ONE-TWO-ONE (H): " + str(i) + "," + str(j+1))
    
        
    def oneTwoOneVert(self, opened_tile, grid_values):
        for i in range(self.row-3):
            for j in range (self.col):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (opened_tile[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if row == [1,2,1]:
                    if (j+1 == self.col or (opened_tile[i][j+1] and opened_tile[i+2][j+1])):
                        if not self.marked_mines[i][j-1]:
                            self.marked_mines[i][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                            
                        print("ONE-TWO-ONE (V): " + str(i+1) + "," + str(j))
                    elif (j == 0 or (opened_tile[i][j-1] and opened_tile[i+2][j-1])):
                        if not self.marked_mines[i][j+1]:
                            self.marked_mines[i][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True
                            
                        print("ONE-TWO-ONE (V): " + str(i+1) + "," + str(j))
                        
                        
    def twoThreeTwoHorz(self, opened_tile, grid_values):
        for i in range(1, self.row-1):
            for j in range(self.col-3):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (opened_tile[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [2,3,2]:
                    if opened_tile[i+1][j] and opened_tile[i+1][j+2]:
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                        
                        print("TWO_THREE_TWO (H): " + str(i) + "," + str(j+1))
                    
                    elif opened_tile[i-1][j] and opened_tile[i-1][j+2]:
                        if not self.marked_mines[i-1][j+1]:
                            self.marked_mines[i-1][j+1] = True
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True 
                        
                        print("TWO_THREE_TWO (H): " + str(i) + "," + str(j+1))
                        
    def twoThreeTwoVert(self, opened_tile, grid_values):
        for i in range(self.row-3):
            for j in range(1,self.col-1):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (opened_tile[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if row == [2,3,2]:
                    if opened_tile[i][j+1] and opened_tile[i+2][j+1]:
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i][j-1]:
                            self.marked_mines[i][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                        
                        print("TWO_THREE_TWO (V): " + str(i+1) + "," + str(j))
                    
                    elif opened_tile[i][j-1] and opened_tile[i+2][j-1]:
                        if not self.marked_mines[i+1][j-1]:
                            self.marked_mines[i+1][j-1] = True
                        if not self.marked_mines[i][j+1]:
                            self.marked_mines[i][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True 
                        
                        print("TWO_THREE_TWO (V): " + str(i+1) + "," + str(j))
                        
    def twoThreeOne(self, opened_tile, grid_values):
        for i in range(1, self.row-1):
            for j in range(self.col-3):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (opened_tile[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [2,3,1]:
                    if opened_tile[i+1][j+1] and opened_tile[i+1][j+2]:
                        if not self.marked_mines[i+1][j]:
                            self.marked_mines[i+1][j] = True
                        if not self.marked_mines[i-1][j]:
                            self.marked_mines[i-1][j] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                        
                        print("TWO_THREE_ONE: " + str(i) + "," + str(j+1))
                    
    def oneTwoTwoOneHorz(self, opened_tile, grid_values):
        for i in range(self.row):
            for j in range(self.col-4):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                    
                if (opened_tile[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if (opened_tile[i][j+3] and not self.finished_tiles[i][j+3]):
                    row.append(grid_values[i][j+3])
                    
                if row == [1,2,2,1]:
                    if i+1==self.row or (opened_tile[i+1][j] and opened_tile[i+1][j+1] and opened_tile[i+1][j+2] and opened_tile[i+1][j+3]):
                        if not self.marked_mines[i-1][j+1]:
                            self.marked_mines[i-1][j+1] = True
                        if not self.marked_mines[i-1][j+2]:
                            self.marked_mines[i-1][j+2] = True
                            
                        print("ONE_TWO_TWO_ONE (H): " + str(i) + "," + str(j+1))
                        
                    if i==0 or (opened_tile[i-1][j] and opened_tile[i-1][j+1] and opened_tile[i-1][j+2] and opened_tile[i-1][j+3]):
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i+1][j+2]:
                            self.marked_mines[i+1][j+2] = True
                            
                        print("ONE_TWO_TWO_ONE (H): " + str(i) + "," + str(j+1))
                        
    def oneTwoTwoOneVert(self, opened_tile, grid_values):
        for i in range(self.row-4):
            for j in range(self.col):
                row = []
                if (opened_tile[i][j] and not self.finished_tiles[i][j]):
                    row.append(grid_values[i][j])
                
                if (opened_tile[i+1][j] and not self.finished_tiles[i+1][j]):
                    row.append(grid_values[i+1][j])
                    
                if (opened_tile[i+2][j] and not self.finished_tiles[i+2][j]):
                    row.append(grid_values[i+2][j])
                    
                if (opened_tile[i+3][j] and not self.finished_tiles[i+3][j]):
                    row.append(grid_values[i+3][j])
                    
                if row == [1,2,2,1]:
                    if j+1==self.col or (opened_tile[i][j+1] and opened_tile[i+1][j+1] and opened_tile[i+2][j+1] and opened_tile[i+3][j+1]):
                        if not self.marked_mines[i+1][j-1]:
                            self.marked_mines[i+1][j-1] = True
                        if not self.marked_mines[i+2][j-1]:
                            self.marked_mines[i+2][j-1] = True
                            
                        print("ONE_TWO_TWO_ONE (V): " + str(i+1) + "," + str(j))
                        
                    if j==0 or (opened_tile[i][j-1] and opened_tile[i][j-1] and opened_tile[i+2][j-1] and opened_tile[i+3][j-1]):
                        if not self.marked_mines[i+1][j+1]:
                            self.marked_mines[i+1][j+1] = True
                        if not self.marked_mines[i+2][j+1]:
                            self.marked_mines[i+2][j+1] = True
                            
                        print("ONE_TWO_TWO_ONE (V): " + str(i+1) + "," + str(j))
                    
    def oneFourTwoFiveThreeSix(self, opened_tile, grid_values):
        to_open = []
        
        for i in range (1,self.row-1):
            for j in range (1,self.col-2):
                row = []
                if (opened_tile[i][j+1] and not self.finished_tiles[i][j+1]):
                    row.append(grid_values[i][j+1])
                if (opened_tile[i][j+2] and not self.finished_tiles[i][j+2]):
                    row.append(grid_values[i][j+2])
                    
                if row == [1,4] or row == [2,5] or row == [3,6]:
                    if self.marked_mines[i][j+3] and self.marked_mines[i-1][j+3] and self.marked_mines[i+1][j+3]:
                        if not opened_tile[i][j-1]:
                            to_open.append([i,j-1])
                        if not opened_tile[i-1][j-1]:
                            to_open.append([i-1,j-1])
                        if not opened_tile[i+1][j-1]:
                            to_open.append([i+1,j-1])
                            
                        print("ONE_4_TWO_5_THREE_6: " + str(i) + ", " + str(j))
                
                elif row == [4,1] or row == [5,2] or row == [6,3]:
                    if self.marked_mines[i][j-1] and self.marked_mines[i-1][j-1] and self.marked_mines[i+1][j-1]:
                        if not opened_tile[i][j+3]:
                            to_open.append([i,j+3])
                        if not opened_tile[i-1][j+3]:
                            to_open.append([i-1,j+3])
                        if not opened_tile[i+1][j+3]:
                            to_open.append([i+1,j+3])
                    
                        print("ONE_4_TWO_5_THREE_6: " + str(i) + ", " + str(j))
        
        return to_open


    # FINDING POTENTIAL MINES

    def potentialMines(self, opened_tile, grid_values):
        for i in range(self.row):
            for j in range(self.col):
                if opened_tile[i][j] and not self.finished_tiles[i][j]:
                    num = grid_values[i][j]
                    maybe = []
                    
                    if (i-1 > -1 and j-1 > -1):
                        if not opened_tile[i-1][j-1]:
                            maybe.append([i-1, j-1])
                    if (i-1 > -1):
                        if not opened_tile[i-1][j]:
                            maybe.append([i-1,j])
                    if (i-1 > -1 and j+1 < self.col):
                        if not opened_tile[i-1][j+1]:
                            maybe.append([i-1, j+1])
                    if (j-1 > -1):
                        if not opened_tile[i][j-1]:
                            maybe.append([i, j-1])
                    if (j+1 < self.col):
                        if not opened_tile[i][j+1]:
                            maybe.append([i, j+1])
                    if (i+1 < self.row and j-1 > -1):
                        if not opened_tile[i+1][j-1]:
                            maybe.append([i+1, j-1])
                    if (i+1 < self.row):
                        if not opened_tile[i+1][j]:
                            maybe.append([i+1, j])
                    if (i+1 < self.row and j+1 < self.col):
                        if not opened_tile[i+1][j+1]:
                            maybe.append([i+1, j+1])    
                    
                    for coord in maybe:
                        if self.marked_mines[coord[0]][coord[1]]:
                            maybe.remove(coord)
                            num-=1
                        else:
                            self.potential_mines[coord[0]][coord[1]] = True    
    
    def openFromPotentialMines(self, opened_tile):
        num_poten=self.numPotential()
        to_guess=self.leftToOpen(opened_tile)
        
        if len(to_guess) > num_poten:
            for i in range(self.row):
                for j in range(self.col):
                    if self.potential_mines[i][j]:
                        to_guess.remove([i,j])         
        return to_guess                             

    def openLinkedTiles(self, opened_tile, grid_values):
        print("hello")


    # HELPERS
     
    def isNeighbour(a,b):
        if abs(b[0]-a[0]) <= 1 and abs(b[1]-a[1]) <= 1:
            return True
        return False


    # COUNTERS
                    
    def numPotential(self):
        count=0
        for i in range(self.row):
            for j in range(self.col):
                if self.potential_mines[i][j]:
                    count+=1
        return count        
                    
    def leftToOpen(self,opened_tile):
        left_to_open=[]
        for i in range(self.row):
            for j in range(self.col):
                if not (opened_tile[i][j] or self.marked_mines[i][j]):
                    left_to_open.append([i,j])
        return left_to_open
                    
    def minesMarked(self):
        count=0
        for i in range(self.row):
            for j in range(self.col):
                if self.marked_mines[i][j]:
                    count+=1
        return count
                                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        