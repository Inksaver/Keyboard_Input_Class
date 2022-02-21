import time
'''
kboard static class returns string, integer, float, boolean and menu choices
Use:
import kboard as kb #shortens the class name to kb

Adding a current console row number at the end of each method overwrites errors on the same line
eg. if the console has already got 5 lines of output:
user_name = kb.get_string("Type your name", True, 5) will display messages over the prompt on line 6
for 2 seconds, then re-display the prompt.

The delay can be over-ridden with kb.delay = 3.5 for a longer delay

user_name = kb.get_string("Type your name", True) # returns user input in Title Case

user_age = kb.get_integer("How old are you", 5, 120) # gets an integer between 5 and 120 from the user

user_height = kb.get_float("How tall are you in metres?", 0.5, 2.5) # gets a float between 0.5 and 2.5 from the user

user_likes_python = kb.get_boolean("Do you like Python? (y/n)") # returns True or False from the user

menu_list = ["Brilliant", "Not bad", "Could do better", "Rubbish"]
user_choice = kb.menu("What do think of this utility?", menu_list)
print(f"User thinks this utility is: {menu_list[user_choice]}")

kb.get_string("Press Enter to Quit", False, 0, 20) # Used instead of input("Press Enter to Quit")
at the end of a file to prevent the console closing (does not apply when run from IDE)
'''
blank = "".ljust(79," ")
delay = 2

def process_input(prompt:str, min_value:int, max_value:int, data_type:str, row) -> str:
	''' This function is not called directly from other files. Python does not have a 'Private' keyword'''
	valid_input:bool = False
	while valid_input is False:
		clear_input_field(row)
		user_input:str = input(prompt + "_").strip()		# remove leading and trailing spaces
		output = user_input									# used later if user_input converted to int/float
		if data_type == "string":							# string requested
			if len(user_input) == 0 and min_value > 0:		# enter pressed when min characters > 0
				error_message(row, "noinput", output)
			elif len(user_input) > max_value:
				error_message(row, "string", output)
			else:
				valid_input = True							# string or "" allowed
		else:												# bool, int or float requested
			if len(user_input) == 0:						# enter pressed
				error_message(row, "noinput", output)
			else:
				if data_type == "bool":						# requesting True/False output
					if user_input[0].lower() == "y":
						user_input = True
						valid_input = True
					elif user_input[0].lower() == "n":
						user_input = False
						valid_input = True
					else:
						error_message(row, "bool", output)
				else:										# int or float requested
					try:
						if data_type == "int":
							user_input = int(user_input)
						elif data_type == "float":
							user_input = float(user_input)				
							
						if user_input >= min_value and user_input <= max_value: # number is within limits
							if round(user_input) != user_input and data_type == "int":
								error_message(row, "notint", output)
							else:
								valid_input = True
						else:
							error_message(row, "range", output, min_value, max_value)
					except:
						if data_type == "int":
							error_message(row, "notint", output) # int or float requested, but input not converted
						else:
							error_message(row, "nan", output)
			
	return user_input # True/False or string or int or float returned
			
def get_string(prompt:str, with_title:bool = False, min_value:int = 1, max_value:int = 20, row:int = -1) -> str: # with_title, min_value and max_value can be over-ridden by calling code
	''' Public method: Gets a string from the user, with options for Title Case, length of the string. Set min_value to 0 to allow empty string return '''
	if row >= 0:
		row += 1
	result = process_input(prompt, min_value, max_value, "string", row)
	if with_title:
		result = result.title()

	return result
	
def get_integer(prompt:str, min_value:int = 0, max_value:int = 65536, row:int = -1) -> int: # min_value and max_value can be over-ridden by calling code
	''' Public Method: gets an integer from the user '''
	if row >= 0:
		row += 1	
	return process_input(prompt, min_value, max_value, "int", row)

def get_float(prompt:str, min_value:float = 0.0, max_value:float = 1000000.0, row:int = -1) -> float: # min_value and max_value can be over-ridden by calling code
	''' Public Method: gets a float from the user '''
	if row >= 0:
		row += 1	
	return process_input(prompt, min_value, max_value, "float", row)
	
def get_boolean(prompt:str, row:int = -1) -> bool:
	''' Public Method: gets a boolean (yes/no) type entries from the user '''
	if row >= 0:
		row += 1	
	return process_input(prompt, 1, 3, "bool", row)

def menu(title:str, menu_list:list, row = -1) -> int:
	''' displays a menu using the text in 'title', and a list of menu items (string) '''
	rows = -1
	if row >= 0:
		rows = row + len(menu_list) + 1	
	print(title)
	for i in range(len(menu_list)):
		if i < 9:
			print(f"     {i+1}) {menu_list[i]}")
		else:
			print(f"    {i+1}) {menu_list[i]}") 
			
	return get_integer(f"Type the number of your choice (1 to {len(menu_list)})", 1, len(menu_list), rows) - 1 # -1 to return correct list index

def error_message(row:int, error_type:str, user_input:str, min_value:float = 0, max_value:float = 0) -> None:
	''' display error message. If row number supplied overwrite with delay '''
	
	message = "Just pressing the Enter key or spacebar doesn't work" # default for "noinput"
	
	if error_type == "string":
		message = f"Try entering text between {min_value} and {max_value} characters"
	elif error_type == "bool":
		message = "Only anything starting with y or n is accepted"
	elif error_type == "notint":
		message = f"Try entering a whole number - {user_input} does not cut it"	
	elif error_type == "nan":
		message = f"Try entering a number - {user_input} does not cut it"
	elif error_type == "range":
		message = f"Try a number from {min_value} to {max_value}"
	
		
	if row > 0:
		message = f">>> {message} <<<"
	else:
		message = f"\n{message}..."	
		
	if row >= 0:
		clear_input_field(row)
	print(message)
	if row >= 0:
		time.sleep(delay)
		clear_input_field(row)

def set_cursor_pos(row:int, col:int) -> None:
	''' Sets the cursor position '''
	print(f"\033[{row};{col}H", end = '')
	
def clear_input_field(row:int) -> None:
	if row >= 0:
		set_cursor_pos(row, 0)
		print(blank)
		set_cursor_pos(row, 0)
		
def sleep(s:float) -> None:
	time.sleep(s)
	
