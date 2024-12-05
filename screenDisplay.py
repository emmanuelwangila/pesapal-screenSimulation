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
    elif instruction == 0x2 and setUpDone:
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
        # Brensenham's line algorithm 
        # difference between cordinates 
        dx = (x1 - x2)
        dy = (y1 - y2)
        # step directio dtermination 
        sx = 1 if x1 < x2 else -1 
        sy = 1 if y1 < y2 else -1
        #  initilize error factor
        err = dx -dy 
        # draw the line using a loop
        while True :
            if 0 <= x1 < screenWidth and 0 <= y1 < screenHight :
                screen.addstr(x1 , y1 , char)
            if x1 == x2 and y1 == y2:
                break 
            # update cordinates 
            e2 = err * 2 
            if e2 > -dy :
                err -= dy
                x1 += sx
            if e2 < dx :
                err += dx;
                y1 += sy;   
    elif instruction == 0x4 and setUpDone:
        # reads length byte
        length = byteStream[index]
        index+=1
        # validations for the clear screen
        if length < 3 :
            continue 
        x , y , color = byteStream[index + 3: index + 3 + length - 3 ]
        index+= length;
        if 0 <= x < screenWidth and 0 <= y and screenHight :
            for idx char in enumerate(text):
                


 

          




      