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
    
     # Initialize screen setup process 
    if instruction == 0x1:
        # reads the length byte
        length = byteStream[index]          
        index+=1;
        # validations for the screen
        if length !=3 :
            continue
        # screen dimensions and color 
        screenWidth = byteStream[index];
        screenHight = byteStream[index + 1];
        screenColor = byteStream[index + 2];
        index+=3;
        setUpDone = True;
        screen.clear();  
    # Initialize drawing the characters 
    elif instruction == 0X2 and setUpDone:
        # reads the length byte
        length = byteStream[index];
        index+=1
        # validations for the character
        if length != 4:
            continue
        # drawing the character
        x , y , char , color = byteStream[index:index + 4]
        index+=4;
        # check if within bounds 
        if 0 <= x < screenWidth and 0 <= y < screenHight:
            # add characters to position
            screen.addstr(x , y , char , color);  
    # Initialize moving cursor , drawing the line
    elif instruction == 0x3 and setUpDone:
        # check the byte length
        length = byteStream[index]
        index+=1
        # validations
        if length !=6 :
            continue
        x1 , y1 , x2 , y2 , color, char = byteStream[index:index + 6]
        index+=6;
        # Bresenh's line algorithm 
 

          




      