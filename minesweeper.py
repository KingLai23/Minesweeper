import pygame, random, json
    
grid_unopened = []
grid_values = []
grid_flags = []

def play(num_row, num_col, num_mines, mode):
    NUM_ROW, NUM_COL, NUM_MINES, MODE = num_row, num_col, num_mines, mode
    init_grids(NUM_ROW, NUM_COL)
    
    UNCLICKED_COLOR = (245, 249, 255)
    GRID_COLOR = (179, 195, 227)
    EMPTY_COLOR = (209, 220, 237)
    CLICKED_COLOR = (245, 249, 255)

    TILE_WIDTH = TILE_HEIGHT = 30
    MARGIN = 2
    TEXT_AREA = 60

    images = getImages()
    
    pygame.init
    
    GAME_WIDTH = TILE_HEIGHT*NUM_COL+(NUM_COL+1)*MARGIN
    GAME_HEIGHT = TILE_WIDTH*NUM_ROW+(NUM_ROW+1)*MARGIN
    
    WINDOW_WIDTH = GAME_WIDTH
    WINDOW_HEIGHT = GAME_HEIGHT+TEXT_AREA
    WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]
    
    BUTTON_WIDTH, BUTTON_HEIGHT = 110, 38
    BUTTON_TOP = (TEXT_AREA - BUTTON_HEIGHT)//2 + GAME_HEIGHT
    PLAYB_LEFT = (WINDOW_WIDTH // 2) - BUTTON_WIDTH - 9
    MENUB_LEFT= (WINDOW_WIDTH // 2) + 9
    
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Minesweeper")

    done = False
    lost = False
    gameover = False
    restart = False
    
    isHighscore = False
        
    goBackToMenu = False
    
    clock = pygame.time.Clock()
    frame_rate = 60
    
    firstClick = True
    extraTime, finishTime = 0,0

    while not done:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (TILE_WIDTH + MARGIN)
                row = pos[1] // (TILE_HEIGHT + MARGIN)
                
                tile_click = row < NUM_ROW and column < NUM_COL
                
                if firstClick and tile_click:
                    gen_board(row, column, NUM_ROW, NUM_COL, NUM_MINES)
                    extraTime = pygame.time.get_ticks()
                    firstClick = False
                
                
                #print(row, column)
                
                if not gameover and tile_click:
                    if (event.button == 1 and not grid_flags[row][column]):
                        open_tiles(row, column, NUM_ROW, NUM_COL)
                        open_number(NUM_ROW, NUM_COL)   
                        
                        if (grid_values[row][column] == 10):
                            lost = True
                    elif (event.button == 3):
                        grid_flags[row][column] = not grid_flags[row][column]
                else:
                    if (event.button == 1):
                        if (pos[0] >= PLAYB_LEFT and pos[0] <= PLAYB_LEFT+BUTTON_WIDTH):
                            if (pos[1] >= BUTTON_TOP and pos[1] <= BUTTON_TOP+BUTTON_HEIGHT):
                                resetBoard(NUM_ROW, NUM_COL) 
                                restart = True
                                done = True
                        if (pos[0] >= MENUB_LEFT and pos[0] <= MENUB_LEFT+BUTTON_WIDTH):
                            if (pos[1] >= BUTTON_TOP and pos[1] <= BUTTON_TOP+BUTTON_HEIGHT):
                                resetBoard(NUM_ROW, NUM_COL) 
                                goBackToMenu = True
                                done = True
        
        screen.fill(GRID_COLOR)
        
        for row in range(NUM_ROW):
            for column in range(NUM_COL):
                color = UNCLICKED_COLOR
                if (grid_unopened[row][column]):
                    color = CLICKED_COLOR
                    
                pygame.draw.rect(screen, color, [(MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN, TILE_WIDTH, TILE_HEIGHT])
                
                if (grid_unopened[row][column]):
                    if (grid_values[row][column] == 10):
                        screen.blit(images[0], ((MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN)) 
                    elif (grid_values[row][column] != 0):
                        screen.blit(images[grid_values[row][column]], ((MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN)) 
                    else:
                        pygame.draw.rect(screen, EMPTY_COLOR, [(MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN, TILE_WIDTH, TILE_HEIGHT])
                
                if (not grid_unopened[row][column] and grid_flags[row][column]):
                    screen.blit(images[9], ((MARGIN + TILE_WIDTH) * column + MARGIN, (MARGIN + TILE_HEIGHT) * row + MARGIN)) 
            
        
        if not (firstClick or gameover):
            if checkWin(NUM_ROW, NUM_COL):
                finishTime = (pygame.time.get_ticks() - extraTime)/1000
                isHighscore = setHighScore(MODE, finishTime)
                gameover = True
            
            if lost:
                gameover = True
                revealGrid(NUM_ROW, NUM_COL)
        
        if gameover:
            MESSAGE_COLOR = (51, 63, 84)
            MESSAGE_WIDTH, MESSAGE_HEIGHT = 180, 70
            
            TEXT_WIDTH = WINDOW_WIDTH//2
            TEXT_HEIGHT = (WINDOW_HEIGHT-TEXT_AREA)//2 - 10
            
            showTime = False
            
            msg = ""
            if lost:
                msg = "bad click"
            else:
                if isHighscore:
                    msg="Highscore!"
                else:
                    msg = "Not bad"
                    
                MESSAGE_HEIGHT = 90
                TEXT_HEIGHT -= 12
                showTime = True
                
            MESSAGE_LEFT = (WINDOW_WIDTH - MESSAGE_WIDTH)//2
            MESSAGE_TOP = (WINDOW_HEIGHT - TEXT_AREA - MESSAGE_HEIGHT)//2 - 10
        
            msg_font = pygame.font.Font('freesansbold.ttf', 24)               
            text = msg_font.render(msg, True, (255,255,255), MESSAGE_COLOR)   
            
            textRect = text.get_rect()
            textRect.center = (TEXT_WIDTH, TEXT_HEIGHT)
            
            pygame.draw.rect(screen, MESSAGE_COLOR, [MESSAGE_LEFT, MESSAGE_TOP, MESSAGE_WIDTH, MESSAGE_HEIGHT])
            screen.blit(text, textRect) 
            
            if showTime:                
                time_font = pygame.font.Font('freesansbold.ttf', 20) 
                time_text = time_font.render(str(finishTime)+"s", True, (218, 222, 224), MESSAGE_COLOR)   
            
                time_text_rect = time_text.get_rect()
                time_text_rect.center = (TEXT_WIDTH, TEXT_HEIGHT + 27)
                screen.blit(time_text, time_text_rect) 
        
        BUTTON_COLOR = (62, 78, 99)
        BUTTON_TEXT_COLOR = (255,255,255)
        
        pygame.draw.rect(screen, BUTTON_COLOR, [PLAYB_LEFT, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT])
        pygame.draw.rect(screen, BUTTON_COLOR, [MENUB_LEFT, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT])
        
        play_font = pygame.font.Font('freesansbold.ttf', 16)               
        play_text = play_font.render("restart", True, BUTTON_TEXT_COLOR, BUTTON_COLOR)   
            
        play_rect = play_text.get_rect()
        play_rect.center = (PLAYB_LEFT+BUTTON_WIDTH//2, BUTTON_TOP+BUTTON_HEIGHT//2)
        screen.blit(play_text, play_rect) 
        
        menu_font = pygame.font.Font('freesansbold.ttf', 16)               
        menu_text = menu_font.render("menu", True, BUTTON_TEXT_COLOR, BUTTON_COLOR)   
            
        menu_rect = menu_text.get_rect()
        menu_rect.center = (MENUB_LEFT+BUTTON_WIDTH//2, BUTTON_TOP+BUTTON_HEIGHT//2)
        screen.blit(menu_text, menu_rect) 
            
        clock.tick(frame_rate)
        pygame.display.flip()
    
    if goBackToMenu:
        gameMenu()
    elif restart:
        play(NUM_ROW, NUM_COL, NUM_MINES, MODE)
    
    pygame.quit()
    
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

def setHighScore(mode, time):
    with open("highscores.txt") as highscores:
        data = json.load(highscores)
    
        if mode == 0:
            diff="easy"
        elif mode == 1:
            diff="kindaEasy"
        else:
            diff="notEasy"
        
    if float(data[diff]) == -1 or float(data[diff]) > time:
        data[diff] = str(time)
        with open ("highscores.txt", "w") as highscores:
            json.dump(data, highscores)
        return True
        
    return False
            
def gameMenu():
    SCREEN_WIDTH, SCREEN_HEIGHT = 280,300
    SCREEN_DIMENSION = (SCREEN_WIDTH,SCREEN_HEIGHT)
    
    OPT1_LEFT = 97
    OPT1_TOP = 76
    OPT1_WIDTH = 86
    OPT1_HEIGHT = 34
    
    OPT2_LEFT = 67
    OPT2_TOP = 118
    OPT2_WIDTH = 147
    OPT2_HEIGHT = 34
    
    OPT3_LEFT = 82
    OPT3_TOP = 160
    OPT3_WIDTH = 117
    OPT3_HEIGHT = 34
    
    HS_LEFT = 70
    HS_TOP = 220
    HS_WIDTH = 141
    HS_HEIGHT = 34
    
    pygame.init() 

    screen = pygame.display.set_mode(SCREEN_DIMENSION) 
      
    pygame.display.set_caption('Minesweeper') 
      
    prompt_font = pygame.font.Font('freesansbold.ttf', 18) 
    options_font = pygame.font.Font('freesansbold.ttf', 18) 
    highscore_font = pygame.font.Font('freesansbold.ttf', 17) 
      
    text = prompt_font.render('pick a difficulty.', True, (0,0,0), (240, 246, 255))   
    opt1 = options_font.render('easy', True, (0,0,0), (193, 214, 247))
    opt2 = options_font.render('kinda easy', True, (0,0,0), (193, 214, 247))
    opt3 = options_font.render('not easy', True, (0,0,0), (193, 214, 247))
    highscore = highscore_font.render('highscores', True, (0,0,0), (151, 172, 209))
    
    textRect = text.get_rect()
    textRect.center = (140, 50) 
    
    opt1Rect = opt1.get_rect()
    opt1Rect.center = (140, 93)
    opt2Rect = opt2.get_rect()
    opt2Rect.center = (140, 135)
    opt3Rect = opt3.get_rect()
    opt3Rect.center = (140, 177)
    
    hsRect = highscore.get_rect()
    hsRect.center = (140, 237)
    
    scores_font = pygame.font.Font('freesansbold.ttf', 16) 
    
    hstext = prompt_font.render('highscores.', True, (0,0,0), (240, 246, 255))       
    hstextRect = hstext.get_rect()
    hstextRect.center = (140, 65)
    
    
    BACK_WIDTH, BACK_HEIGHT = 100, 35
    BACK_LEFT = (SCREEN_WIDTH-BACK_WIDTH)//2
    BACK_TOP = 215
    
    back_font = pygame.font.Font('freesansbold.ttf', 17) 
    backText = back_font.render('back', True, (0,0,0), (151, 172, 209))       
    backTextRect = backText.get_rect()
    backTextRect.center = (SCREEN_WIDTH//2, BACK_TOP+16)
      
    done = False
    gameStart = False
    
    viewHighscores = False
    easyHS, kindaEasyHS, notEasyHS = 0,0,0
    
    while not done : 
        screen.fill((240, 246, 255)) 
        if not viewHighscores:
            screen.blit(text, textRect) 
            
            pygame.draw.rect(screen, (193, 214, 247), [OPT1_LEFT,OPT1_TOP,OPT1_WIDTH,OPT1_HEIGHT])
            pygame.draw.rect(screen, (193, 214, 247), [OPT2_LEFT,OPT2_TOP,OPT2_WIDTH,OPT2_HEIGHT])
            pygame.draw.rect(screen, (193, 214, 247), [OPT3_LEFT,OPT3_TOP,OPT3_WIDTH,OPT3_HEIGHT])
            pygame.draw.rect(screen, (151, 172, 209), [HS_LEFT,HS_TOP,HS_WIDTH,HS_HEIGHT])
           
            screen.blit(opt1, opt1Rect) 
            screen.blit(opt2, opt2Rect)
            screen.blit(opt3, opt3Rect)
            screen.blit(highscore, hsRect)
            
            row, col, mines, mode = 0,0,0,0
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    
                    if (pos[0] >= OPT1_LEFT and pos[0] <= OPT1_LEFT+OPT1_WIDTH):
                        if (pos[1] >= OPT1_TOP and pos[1] <= OPT1_TOP+OPT1_HEIGHT):
                            row, col, mines = 9,9,10
                            gameStart = True
                            done = True
                    if (pos[0] >= OPT2_LEFT and pos[0] <= OPT2_LEFT+OPT2_WIDTH):
                        if (pos[1] >= OPT2_TOP and pos[1] <= OPT2_TOP+OPT2_HEIGHT):
                            row, col, mines = 16,16,40
                            mode=1
                            gameStart = True
                            done = True
                    if (pos[0] >= OPT3_LEFT and pos[0] <= OPT3_LEFT+OPT3_WIDTH):
                        if (pos[1] >= OPT3_TOP and pos[1] <= OPT3_TOP+OPT3_HEIGHT):
                            row, col, mines = 16,30,99
                            mode=2
                            gameStart = True
                            done = True
                    if (pos[0] >= HS_LEFT and pos[0] <= HS_LEFT+HS_WIDTH):
                        if (pos[1] >= HS_TOP and pos[1] <= HS_TOP+HS_HEIGHT):
                            viewHighscores = True
                            
                            with open("highscores.txt") as json_file:
                                data = json.load(json_file)
                                
                                if float(data["easy"]) == -1:
                                    easyHS = 'n/a'
                                else:
                                    easyHS = data["easy"]+"s"
                                    
                                if float(data["kindaEasy"]) == -1:
                                    kindaEasyHS = 'n/a'
                                else:
                                    kindaEasyHS = data["kindaEasy"]+"s"
                                    
                                if float(data["notEasy"]) == -1:
                                    notEasyHS = 'n/a'
                                else:
                                    notEasyHS = data["notEasy"]+"s"
                 
        else:
            screen.blit(hstext, hstextRect) 
            
            ezScore = scores_font.render('easy: ' + str(easyHS), True, (0,0,0), (240, 246, 255))       
            ezScoreRect = ezScore.get_rect()
            ezScoreRect.center = (140, 109)
            
            medScore = scores_font.render('kinda easy: ' + str(kindaEasyHS), True, (0,0,0), (240, 246, 255))       
            medScoreRect = medScore.get_rect()
            medScoreRect.center = (140, 139)
            
            hardScore = scores_font.render('not easy: ' + str(notEasyHS), True, (0,0,0), (240, 246, 255))       
            hardRect = hardScore.get_rect()
            hardRect.center = (140, 169)
            
            screen.blit(ezScore, ezScoreRect) 
            screen.blit(medScore, medScoreRect) 
            screen.blit(hardScore, hardRect) 
            
            pygame.draw.rect(screen, (151, 172, 209), [BACK_LEFT,BACK_TOP,BACK_WIDTH,BACK_HEIGHT])
            screen.blit(backText, backTextRect)
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    
                    if (pos[0] >= BACK_LEFT and pos[0] <= BACK_LEFT+BACK_WIDTH):
                        if (pos[1] >= BACK_TOP and pos[1] <= BACK_TOP+BACK_HEIGHT):
                            viewHighscores = False
                    
        pygame.display.flip()
        
    if gameStart:
        play(row, col, mines, mode)
        
    pygame.quit()
        
gameMenu() 
    
    
    
    
    
    
    