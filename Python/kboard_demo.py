import lib.console as console
import lib.kboard as kb # shortens the class name to kb

def get_row(row:int, rows:int = 1) -> int:
	''' If running from an IDE, row should always be -1
	so no set_cursor_pos is used in Kboard library.
	Otherwise increment row by rows
	'''
	if row == -1:
		return -1
	else:
		return row + rows	

def main() -> None:
	''' Everything runs from here '''
	console.clear()
	row = -1					# assume running in IDE
	if console.is_console:		# running in console / terminal
		row = 0					# start row at 0
		
	user_name = kb.get_string("Type your name", True, 3, 6, row) 			# returns user input in Title Case
	print(f"User name : {user_name} <- see how I used a capital letter!")
	
	row = get_row(row, 2)		# if in IDE row = -1, else row = 2
	user_age = kb.get_integer("How old are you", 5, 120, row) 				# gets an integer between 5 and 120 from the user
	print(f"User age : {user_age}")
	
	row = get_row(row, 2)		# if in IDE row = -1, else row = 4
	user_height = kb.get_float("How tall are you in metres?", 0.5, 2.5, row) # gets a float between 0.5 and 2.5 from the user
	print(f"User height : {user_height}")
	
	row = get_row(row, 2)		# if in IDE row = -1, else row = 6
	user_likes_python = kb.get_boolean("Do you like Python? (y/n)", row) 	# returns True or False from the user
	print(f"User likes Python : {user_likes_python}")
	kb.sleep(2)
	
	row = console.clear()		# resets row to -1 / 0
	title = "What do think of this utility?"
	menu_list = ["Brilliant", "Not bad", "Could do better", "Rubbish"]
	user_choice = kb.menu(title, menu_list, row)
	print(f"User thinks this utility is : {menu_list[user_choice]}")
	
	if console.is_console:
		# if running from a console/terminal instead of an IDE to prevent closing.
		kb.get_string("Press Enter to Quit", False, 0, 20) # Used instead of input("Press Enter to Quit")
	
main()
