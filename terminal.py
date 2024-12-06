import curses
import time

def main(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    print(f"Terminal size: {max_x}x{max_y}")
    time.sleep(2)  # Add a small delay
    stdscr.getch()  

if __name__ == "__main__":
    curses.wrapper(main)

    