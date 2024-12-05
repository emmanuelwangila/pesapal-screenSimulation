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
        if 0 <= x < screenWidth and 0 <= y < screenHight:
            screen.addstr(x , y , char , color);  

          




      