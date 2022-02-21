'''
This class is used to get console information.
On Windows ANSI codes can be 'reluctant' to start, so clearing the console is usually the best start
USE: import console" (or folder.console if stored elsewhere)
Call any console function eg console.clear() or console.initialise():
console.initialise() -> runs console.initialise() and sets isInitialised = true
Console.Clear() -> runs Console.Initialise() and sets isInitialised = true
populates properties:
os_name
is_console
window_width
window_height

utf8 box characters stored here for easy copy/paste:

┌ ┬ ┐ ─ ╔ ╦ ╗ ═
 
├ ┼ ┤ │ ╠ ╬ ╣ ║
 
└ ┴ ┘   ╚ ╩ ╝

'''
import os

window_width = 0
window_height = 0
is_console = False
os_name = ""
is_initialised = False
CLEARLINE = '\x1b[2K'  	# clear the line

def add_lines(num_lines, current_lines = None): #default 30 lines if not given
	''' overloaded Python function: supply None as 2nd parameter'''
	# use 1: add_lines(5) adds 5 additional blank lines
	# use 2: add_lines(5, 19) adds sufficient lines to fill console to last 5 lines (as 19 are already used)
	blank = "".rjust(window_width); #string of spaces across entire width of Console
	if current_lines is None:
		if num_lines > 0:
			for i in range(num_lines):
				print(blank)
	else:
		leave_lines = num_lines
		num_lines = window_height - current_lines - leave_lines;
		if num_lines > 0:
			for i in range(num_lines):
				print(blank)

	return num_lines;	

def clear() -> None:
	''' clears console using appropriate method for current platform'''
	if is_console:
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
		return 0		# if running in terminal/console row = 0
	else:
		add_lines(window_height)
		return -1		# if running in ide row = -1
		
def clear_line(line_no):
	set_cursor_pos(1, line_no)
	print(CLEARLINE, end = '')
	
def initialise():
	''' runs on load to get console/terminal info '''
	global window_width, window_height, is_console, is_initialised
	if not is_initialised:
		try:
			window_width = os.get_terminal_size().columns # this will fail if NOT in a console
			window_height = os.get_terminal_size().lines # this will fail if NOT in a console
			is_console = True
		except:
			window_width = 80
			window_height = 25
			is_console = False
		is_initialised = True
		
def resize(window_width, window_height, clear = True):
	''' resize the console / terminal '''
	if is_console:
		if os.name == 'nt':
			os.system(f'mode {window_width},{window_height}')
		else:    
			cmd = f"'\\e[8;{window_height};{window_width}t'"
			os.system("echo -e " + cmd) 
		if clear:
			clear()
			
initialise() # runs when console class is first referenced