import pygame, random, time, copy
from minesweeper_engine import *
    
grid_unopened = []
grid_values = []
grid_flags = []


def play(num_row, num_col, num_mines, delay, auto_quit):
    NUM_ROW, NUM_COL, NUM_MINES = num_row, num_col, num_mines
    init_grids(NUM_ROW, NUM_COL)
    
    UNCLICKED_COLOR = (232, 239, 250)
    GRID_COLOR = (179, 195, 227)
    EMPTY_COLOR = (209, 220, 237)
    CLICKED_COLOR = (240, 246, 255)

    TILE_WIDTH = TILE_HEIGHT = 30
    MARGIN = 2
    TEXT_AREA = 50

    images = getImages()
    
    pygame.init
    pygame.font.init()
    
    GAME_WIDTH = TILE_HEIGHT*NUM_COL+(NUM_COL+1)*MARGIN
    GAME_HEIGHT = TILE_WIDTH*NUM_ROW+(NUM_ROW+1)*MARGIN
    
    WINDOW_WIDTH = GAME_WIDTH
    WINDOW_HEIGHT = GAME_HEIGHT+TEXT_AREA
    WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]
    
    BUTTON_WIDTH, BUTTON_HEIGHT = 85, 30
    BUTTON_TOP = (TEXT_AREA - BUTTON_HEIGHT)//2 + GAME_HEIGHT
    PLAYB_LEFT = (WINDOW_WIDTH // 2) - BUTTON_WIDTH - 9
    MENUB_LEFT= (WINDOW_WIDTH // 2) + 9
    
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Minesweeper")

    done = False
    lost = False
    gameover = False
    
    clock = pygame.time.Clock()
    frame_rate = 60
    
    start_time = pygame.time.get_ticks()
    firstClick = True

    engine = minesweeper_engine(NUM_ROW, NUM_COL)
    
    moves_made, tiles=0,0
    
    prev_boards = []
    prev_boards.append(copy.deepcopy(grid_unopened))
    current_revision = 0
    usePrev = False

    while not done:             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif gameover:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    
                    if (pos[0] >= PLAYB_LEFT and pos[0] <= PLAYB_LEFT+BUTTON_WIDTH):
                        if (pos[1] >= BUTTON_TOP and pos[1] <= BUTTON_TOP+BUTTON_HEIGHT):
                            if current_revision > 0:
                                current_revision-=1
                                usePrev = True
                    if (pos[0] >= MENUB_LEFT and pos[0] <= MENUB_LEFT+BUTTON_WIDTH):
                        if (pos[1] >= BUTTON_TOP and pos[1] <= BUTTON_TOP+BUTTON_HEIGHT):
                            if current_revision+1 < len(prev_boards):
                                current_revision+=1
                                usePrev = True
                                
        
        if firstClick:
            row = random.randint(0,NUM_ROW-1)
            col =random.randint(0,NUM_COL-1)
            gen_board(row, col, NUM_ROW, NUM_COL, NUM_MINES)
            open_tiles(row, col, NUM_ROW, NUM_COL)
            open_number(NUM_ROW, NUM_COL)
            firstClick = False
            moves_made+=1
            
            prev_boards.append(copy.deepcopy(grid_unopened))
            current_revision+=1

                        
        elif not gameover:
            to_open = makeMove(engine)
            moves_made+=len(to_open)
            for coord in to_open:
                time.sleep(delay)
                row = coord[0]
                column = coord[1]
                if grid_values[row][column] != 10:
                    open_tiles(row, column, NUM_ROW, NUM_COL)
                    open_number(NUM_ROW, NUM_COL)
                    
                    if (prev_boards[current_revision] != grid_unopened):
                        prev_boards.append(copy.deepcopy(grid_unopened))
                        current_revision+=1
                else:
                    lost = True
                            
        
        screen.fill(GRID_COLOR)
        
        for row in range(NUM_ROW):
            for column in range(NUM_COL):
                color = UNCLICKED_COLOR
                if (prev_boards[current_revision][row][column]):
                    color = CLICKED_COLOR
                    
                pygame.draw.rect(screen, color, [(MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN, TILE_WIDTH, TILE_HEIGHT])
                
                if (prev_boards[current_revision][row][column]):
                    if (grid_values[row][column] == 10):
                        screen.blit(images[0], ((MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN)) 
                    elif (grid_values[row][column] != 0):
                        screen.blit(images[grid_values[row][column]], ((MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN)) 
                    else:
                        pygame.draw.rect(screen, EMPTY_COLOR, [(MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN, TILE_WIDTH, TILE_HEIGHT])
        
        if not (firstClick or gameover):
            if checkWin(NUM_ROW, NUM_COL):
                tiles=NUM_ROW*NUM_COL
                print("\nwin")
                print("time elapsed: " + str((pygame.time.get_ticks()-start_time)/1000))
                print("moves made: " + str(moves_made))
                gameover = True

            if lost:
                tiles=tiles_opened(NUM_ROW, NUM_COL)
                revealGrid(NUM_ROW, NUM_COL)
                prev_boards.append(copy.deepcopy(grid_unopened))
                current_revision+=1
                print("\nlost")
                print("time elapsed: " + str((pygame.time.get_ticks()-start_time)/1000))
                print("moves made: " + str(moves_made))
                gameover = True
                
        BUTTON_COLOR = (62, 78, 99)
        BUTTON_TEXT_COLOR = (255,255,255)
        
        pygame.draw.rect(screen, BUTTON_COLOR, [PLAYB_LEFT, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT])
        pygame.draw.rect(screen, BUTTON_COLOR, [MENUB_LEFT, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT])
        
        play_font = pygame.font.Font('freesansbold.ttf', 16)               
        play_text = play_font.render("<<<", True, BUTTON_TEXT_COLOR, BUTTON_COLOR)   
            
        play_rect = play_text.get_rect()
        play_rect.center = (PLAYB_LEFT+BUTTON_WIDTH//2, BUTTON_TOP+BUTTON_HEIGHT//2)
        screen.blit(play_text, play_rect) 
        
        menu_font = pygame.font.Font('freesansbold.ttf', 16)               
        menu_text = menu_font.render(">>>", True, BUTTON_TEXT_COLOR, BUTTON_COLOR)   
            
        menu_rect = menu_text.get_rect()
        menu_rect.center = (MENUB_LEFT+BUTTON_WIDTH//2, BUTTON_TOP+BUTTON_HEIGHT//2)
        screen.blit(menu_text, menu_rect) 
            
        clock.tick(frame_rate)
        pygame.display.flip()

        if auto_quit and gameover:
            done=True
    
    pygame.quit()
    
    if not lost:
        return 1, moves_made, tiles
    return 0, moves_made, tiles
    
def open_tiles(i, j, NUM_ROW, NUM_COL):
    if not grid_unopened[i][j]: 
        grid_unopened[i][j] = True
        if (i-1 > -1 and j-1 > -1 and grid_values[i-1][j-1] == 0):
            open_tiles(i-1, j-1, NUM_ROW, NUM_COL)
        if (i-1 > -1 and grid_values[i-1][j] == 0):
            open_tiles(i-1, j, NUM_ROW, NUM_COL)
        if (i-1 > -1 and j+1 < NUM_COL and grid_values[i-1][j+1] == 0):
            open_tiles(i-1, j+1, NUM_ROW, NUM_COL)
        if (j-1 > -1 and grid_values[i][j-1] == 0):
            open_tiles(i, j-1, NUM_ROW, NUM_COL)
        if (j+1 < NUM_COL and grid_values[i][j+1] == 0):
            open_tiles(i, j+1, NUM_ROW, NUM_COL)
        if (i+1 < NUM_ROW and j-1 > -1 and grid_values[i+1][j-1] == 0):
            open_tiles(i+1, j-1, NUM_ROW, NUM_COL)
        if (i+1 < NUM_ROW and grid_values[i+1][j] == 0):
            open_tiles(i+1, j, NUM_ROW, NUM_COL)
        if (i+1 < NUM_ROW and j+1 < NUM_COL and grid_values[i+1][j+1] == 0):
            open_tiles(i+1, j+1, NUM_ROW, NUM_COL)

def open_number(NUM_ROW, NUM_COL):
    for i in range (NUM_ROW):
        for j in range (NUM_COL):
            if (grid_values[i][j] == 0 and grid_unopened[i][j]):
                if (i-1 > -1 and j-1 > -1 and not grid_unopened[i-1][j-1]):
                    grid_unopened[i-1][j-1] = True
                if (i-1 > -1 and not grid_unopened[i-1][j]):
                    grid_unopened[i-1][j] = True
                if (i-1 > -1 and j+1 < NUM_COL and not grid_unopened[i-1][j+1]):
                    grid_unopened[i-1][j+1] = True
                if (j-1 > -1 and not grid_unopened[i][j-1]):
                    grid_unopened[i][j-1] = True
                if (j+1 < NUM_COL and not grid_unopened[i][j+1]):
                    grid_unopened[i][j+1] = True
                if (i+1 < NUM_ROW and j-1 > -1 and not grid_unopened[i+1][j-1]):
                    grid_unopened[i+1][j-1] = True
                if (i+1 < NUM_ROW and not grid_unopened[i+1][j]):
                    grid_unopened[i+1][j] = True
                if (i+1 < NUM_ROW and j+1 < NUM_COL and not grid_unopened[i+1][j+1]):
                    grid_unopened[i+1][j+1] = True

def gen_mines(row, col, NUM_ROW, NUM_COL, NUM_MINES):
    mine_locations=[]
    
    for i in range (NUM_MINES):
        mine_location=[random.randint(0,NUM_ROW-1), random.randint(0,NUM_COL-1)]
        while mine_location in mine_locations or mine_location == [row, col]:
            mine_location=[random.randint(0,NUM_ROW-1), random.randint(0,NUM_COL-1)]
            
        mine_locations.append(mine_location)
    
    return mine_locations

def gen_board(row, col, NUM_ROW, NUM_COL, NUM_MINES):    
    resetBoard(NUM_ROW, NUM_COL)
        
    mine_locations = gen_mines(row, col, NUM_ROW, NUM_COL, NUM_MINES)        
            
    for mine_location in mine_locations:
        i = mine_location[0]
        j = mine_location[1]
        grid_values[i][j] = 10
        
        if (i-1 > -1 and j-1 > -1 and grid_values[i-1][j-1] != 10):
            grid_values[i-1][j-1]+=1
        if (i-1 > -1 and grid_values[i-1][j] != 10):
            grid_values[i-1][j]+=1
        if (i-1 > -1 and j+1 < NUM_COL and grid_values[i-1][j+1] != 10):
            grid_values[i-1][j+1]+=1
        if (j-1 > -1 and grid_values[i][j-1] != 10):
            grid_values[i][j-1]+=1
        if (j+1 < NUM_COL and grid_values[i][j+1] != 10):
            grid_values[i][j+1]+=1
        if (i+1 < NUM_ROW and j-1 > -1 and grid_values[i+1][j-1] != 10):
            grid_values[i+1][j-1]+=1
        if (i+1 < NUM_ROW and grid_values[i+1][j] != 10):
            grid_values[i+1][j]+=1  
        if (i+1 < NUM_ROW and j+1 < NUM_COL and grid_values[i+1][j+1] != 10):
            grid_values[i+1][j+1]+=1       
                
    return mine_locations
            
def getImages():
    images = []

    images.append(pygame.image.load('images\\mine.jpg'))
    images.append(pygame.image.load('images\\one.jpg'))
    images.append(pygame.image.load('images\\two.jpg'))
    images.append(pygame.image.load('images\\three.jpg'))
    images.append(pygame.image.load('images\\four.jpg'))
    images.append(pygame.image.load('images\\five.jpg'))
    images.append(pygame.image.load('images\\six.jpg'))
    images.append(pygame.image.load('images\\seven.jpg'))
    images.append(pygame.image.load('images\\eight.jpg'))
    images.append(pygame.image.load('images\\flag.jpg'))

    return images    

def checkWin(NUM_ROW, NUM_COL):
    for i in range(NUM_ROW):
        for j in range (NUM_COL):
            if (grid_values[i][j] != 10 and not grid_unopened[i][j]):
                return False
    return True

def revealGrid(NUM_ROW, NUM_COL):
    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            grid_unopened[i][j] = True
    
def resetBoard(NUM_ROW, NUM_COL):
    if (grid_unopened == []):
        return
    
    for row in range(NUM_ROW):
        for column in range(NUM_COL):
            grid_unopened[row][column] = False
            grid_flags[row][column] = False
            grid_values[row][column] = 0
    
def init_grids(NUM_ROW, NUM_COL):
    for row in range(NUM_ROW):
        grid_values.append([])
        grid_unopened.append([])
        grid_flags.append([])
        for column in range(NUM_COL):
            grid_unopened[row].append(False)
            grid_flags[row].append(False)
            grid_values[row].append(0)            
        

def tiles_opened(NUM_ROW, NUM_COL):
    count=0
    for i in range (NUM_ROW):
        for j in range (NUM_COL):
            if grid_unopened[i][j]:
                count+=1
    return count

def makeMove(engine):     
    return engine.detectMine(grid_unopened, grid_values)

def run(mode, delay, trials, autoQ):
    wins = 0
    moves = 0
    tiles = 0
    
    for i in range (trials):
        if mode == 0:
            w,m,t=play(9,9,10,delay,autoQ)
            row,col=9,9
        elif mode == 1:
            w,m,t=play (16,16,40,delay,autoQ)
            row,col=16,16
        else:
            w,m,t=play (16,30,99,delay,autoQ)
            row,col=16,30
            
        wins+=w
        moves+=m
        tiles+=t
            
    print("\n______________________________\n")
    print("    Wins,Win Rate: " + str(wins) + ", " + str(wins*100/trials) + "%")
    print("      Average Moves: " + str(moves//trials))
    print("        Open Rate: " + str(tiles*100//(trials*row*col)) + "%")
    print("______________________________")

#---------------------------------------------------------------------------

MODE=0
DELAY=0
TRIALS=50
AUTOQUIT=True

run(MODE,DELAY,TRIALS,AUTOQUIT)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

