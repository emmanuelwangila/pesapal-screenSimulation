import curses ;

def screenSimulation(screen , byteStream):
    # boolean to check if screen is initailized 
    setUpDone = False;    
    # define the screen cursors positions 
    cursorX , cursorY = 0 ,  0;
    # screen width and height dimensions and color 
    screenWidth , screenHight , screenColor = 0 , 0 , 0;
    screen.clear();

    index = 0 ;
    while ( index < len(byteStream)):
        instruction = byteStream[index]
        index+= 1;