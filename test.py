import curses

def simpleScreenSimulation(screen):
    curses.curs_set(0)  # Hide cursor
    screen.clear()
    screen.addstr(0, 0, "Hello, this is a test!")
    screen.refresh()
    screen.getch()  # Wait for user input before exiting

def main():
    curses.wrapper(simpleScreenSimulation)

if __name__ == "__main__":
    main()
