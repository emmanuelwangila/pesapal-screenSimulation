import curses

def screenSimulation(screen, byteStream):
    print("Screen Simulation");
    setUpDone = False
    cursorX, cursorY = 0, 0
    screenWidth, screenHeight, screenColor = 0, 0, 0

    # Setup curses environment
    curses.curs_set(0)  # Hide cursor
    screen.clear()
    screen.refresh()

    index = 0
    while index < len(byteStream):
        instruction = byteStream[index]
        index += 1

        # Screen setup process
        if instruction == 0x1:
            length = byteStream[index]
            index += 1
            if length != 3:
                continue
            screenWidth = byteStream[index]
            screenHeight = byteStream[index + 1]
            screenColor = byteStream[index + 2]
            index += 3
            setUpDone = True
            screen.clear()

        # Draw a character
        elif instruction == 0x2 and setUpDone:
            length = byteStream[index]
            index += 1
            if length != 4:
                continue
            x, y, char, color = byteStream[index:index + 4]
            index += 4
            if 0 <= x < screenWidth and 0 <= y < screenHeight:
                screen.addch(y, x, chr(char), curses.color_pair(color))

        # Draw a line
        elif instruction == 0x3 and setUpDone:
            length = byteStream[index]
            index += 1
            if length != 6:
                continue
            x1, y1, x2, y2, color, char = byteStream[index:index + 6]
            index += 6
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            while True:
                if 0 <= x1 < screenWidth and 0 <= y1 < screenHeight:
                    screen.addch(y1, x1, chr(char), curses.color_pair(color))
                if x1 == x2 and y1 == y2:
                    break
                e2 = err * 2
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        # Render text
        elif instruction == 0x4 and setUpDone:
            length = byteStream[index]
            index += 1
            if length < 3:
                continue
            x, y, color = byteStream[index:index + 3]
            text = byteStream[index + 3:index + 3 + length - 3]
            index += length
            for idx, char in enumerate(text):
                if 0 <= x + idx < screenWidth and 0 <= y < screenHeight:
                    screen.addch(y, x + idx, chr(char), curses.color_pair(color))

        # Move cursor
        elif instruction == 0x5 and setUpDone:
            length = byteStream[index]
            index += 1
            if length != 2:
                continue
            cursorX, cursorY = byteStream[index:index + 2]
            index += 2
            if 0 <= cursorX < screenWidth and 0 <= cursorY < screenHeight:
                # Corrected cursor move
                screen.move(cursorY, cursorX)
                screen.refresh()

        # Draw at cursor position
        elif instruction == 0x6 and setUpDone:
            length = byteStream[index]
            index += 1
            if length != 2:
                continue
            char, color = byteStream[index:index + 2]
            index += 2
            if 0 <= cursorX < screenWidth and 0 <= cursorY < screenHeight:
                screen.addch(cursorY, cursorX, chr(char), curses.color_pair(color))
                screen.refresh()

        # Clear screen
        elif instruction == 0x7 and setUpDone:
            length = byteStream[index]
            index += 1
            if length != 0:
                continue
            screen.clear()

        # End of file
        elif instruction == 0xFF:
            break

        # Unrecognized instruction
        else:
            continue

    screen.refresh()

def main():
    byteStream = [
        0x1, 3, 80, 24, 1,          # Screen setup: 80x24, Color = 1
        0x2, 4, 10, 5, ord('A'), 2, # Draw 'A' at (10, 5) with color 2
        0x3, 6, 2, 2, 15, 5, 3, ord('*'), # Draw line from (2, 2) to (15, 5)
        0x4, 8, 15, 10, 4, ord('H'), ord('e'), ord('l'), ord('l'), ord('o'), # Render "Hello"
        0x5, 2, 40, 12,             # Move cursor to (40, 12)
        0x6, 2, ord('B'), 5,        # Draw 'B' at cursor position
        0x7, 0,                     # Clear the screen
        0xFF                        # End of file
    ]
    curses.wrapper(lambda scr: screenSimulation(scr, byteStream))

if __name__ == "__main__":
    main()

