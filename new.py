import curses
import sys
import time

# Function to handle different types of commands
def handle_command(stdscr, command_byte, data):
    max_y, max_x = stdscr.getmaxyx()  # Get terminal size (max_y = rows, max_x = columns)
    try:
        if command_byte == 0x1:  # Screen setup (ignored, but required for setup)
            # Data contains width, height, and color_mode, though we are not using them here
            width, height, color_mode = data[:3]
            stdscr.clear()  # Clears the screen (required for setup)
            print(f"Screen setup (Ignoring resize): {width}x{height}, color mode: {color_mode}")

        elif command_byte == 0x2:  # Draw character
            x, y, color_index, char_code = data[:4]  # Data contains coordinates and character code
            if 0 <= x < max_x and 0 <= y < max_y:  # Check if the coordinates are within the terminal bounds
                stdscr.addch(y, x, chr(char_code))  # Draw the character at the specified coordinates
            else:
                print(f"Warning: Ignoring out-of-bounds character at ({x}, {y})")

        elif command_byte == 0x3:  # Draw line (simplified to horizontal or vertical)
            x1, y1, x2, y2, color_index, char_code = data[:6]
            if x1 == x2:  # Vertical line
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    if 0 <= x1 < max_x and 0 <= y < max_y:
                        stdscr.addch(y, x1, chr(char_code))
                    else:
                        print(f"Warning: Ignoring out-of-bounds line segment at ({x1}, {y})")
            elif y1 == y2:  # Horizontal line
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    if 0 <= x < max_x and 0 <= y1 < max_y:
                        stdscr.addch(y1, x, chr(char_code))
                    else:
                        print(f"Warning: Ignoring out-of-bounds line segment at ({x}, {y1})")

        elif command_byte == 0x4:  # Render text
            x, y, color_index = data[:3]  # Data contains coordinates and color index
            text = "".join(chr(b) for b in data[3:])  # Convert the remaining bytes to text
            if 0 <= x < max_x and 0 <= y < max_y:
                stdscr.addstr(y, x, text)  # Render the text at the specified position
            else:
                print(f"Warning: Ignoring out-of-bounds text at ({x}, {y})")

        elif command_byte == 0x5:  # Cursor movement
            x, y = data[:2]  # Data contains new cursor coordinates
            if 0 <= x < max_x and 0 <= y < max_y:
                stdscr.move(y, x)  # Move the cursor to the specified position
            else:
                print(f"Warning: Ignoring out-of-bounds cursor movement to ({x}, {y})")

        elif command_byte == 0x6:  # Draw at cursor position
            char_code, color_index = data[:2]  # Data contains character code and color index
            stdscr.addch(chr(char_code))  # Draw the character at the current cursor position

        elif command_byte == 0x7:  # Clear screen
            stdscr.clear()  # Clear the screen

        elif command_byte == 0xFF:  # End of file (end processing)
            pass  # Nothing to do here, just exit the loop

        else:
            # If command is unknown, raise an error
            raise ValueError(f"Unknown command: 0x{command_byte:02X}")

        stdscr.refresh()  # Refresh the screen after each command to reflect changes

    except (IndexError, ValueError) as e:
        # Catch errors and print an error message if any command is invalid
        print(f"Error processing command 0x{command_byte:02X}: {e}")

# Function to process the byte stream
def process_byte_stream(stdscr, byte_stream):
    i = 0  # Start index for reading the byte stream
    while i < len(byte_stream):  # Loop through the byte stream
        try:
            command_byte = byte_stream[i]  # Read the command byte
            length_byte = byte_stream[i + 1]  # Read the length byte
            data_start = i + 2  # Start of the data (after command and length bytes)
            data_end = data_start + length_byte  # End of the data
            data = byte_stream[data_start:data_end]  # Extract the data portion

            # Validate the length of the data
            if length_byte < 0:
                raise ValueError("Invalid length: Length cannot be negative.")
            if len(data) != length_byte:
                raise ValueError(f"Data length mismatch: Expected {length_byte}, got {len(data)}")

            handle_command(stdscr, command_byte, data)  # Handle the command
            i = data_end  # Move the index to the next command

        except (IndexError, ValueError) as e:
            # Catch errors during processing and skip to the next command
            print(f"Error at byte index {i}: {e}. Skipping to the next command.")
            i += 2  # Skip the faulty command and length byte

# Main function to run the program using curses
def main(stdscr):
    max_y, max_x = stdscr.getmaxyx()  # Get the terminal size
    print(f"Terminal size: {max_x}x{max_y}")  # Print terminal dimensions (for debugging)

    # Define a byte stream with a series of commands
    byte_stream = [
        0x1, 3, 80, 25, 0,  # Screen setup (Width=80, Height=25, Color Mode=0x00)
        0x2, 4, 1, 1, 0, 65,  # Draw 'A' at (1, 1) with color index 0
        0x2, 4, 2, 1, 0, 42,  # Draw '*' at (2, 1) with color index 0
        0x4, 9, 1, 2, 0, 72, 101, 108, 108, 111,  # Render "Hello" at (1, 2) with color index 0
        0x3, 6, 1, 3, 5, 3, 0, 45,  # Draw line from (1, 3) to (5, 3) with '-' and color index 0
        0x06, 2, 64, 1,  # Draw '@' (ASCII 64) at the cursor position
        0x05, 2, 2, 25,  # Move cursor to (2, 25)
        0xFF  # End of file (EOF)
    ]

    # Process the byte stream
    process_byte_stream(stdscr, byte_stream)

    # Add a delay to allow viewing the output before the program exits
    time.sleep(2)

    # Wait for a key press before exiting
    stdscr.getch()

# Run the main function with curses wrapper to set up terminal environment
if __name__ == "__main__":
    curses.wrapper(main)
