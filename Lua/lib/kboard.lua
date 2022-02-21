-- Kboard static class returns string, integer, boolean and menu choices
local Kboard = {}
local blank = string.rep(" ", 79)
local delay = 2

local function trim(s)
	--[[ trim leading and trailing spaces ]]
	return (s:gsub("^%s*(.-)%s*$", "%1"))
end
string.trim = trim
string.strip = trim

--[[from http://lua-users.org/wiki/StringRecipes
	Change an entire string to Title Case (i.e. capitalise the first letter of each word)
	Add extra characters to the pattern if you need to. _ and ' are
	found in the middle of identifiers and English words.
	We must also put %w_' into [%w_'] to make it handle normal stuff
	and extra stuff the same.
	This also turns hex numbers into, eg. 0Xa7d4
	
	str = str:gsub("(%a)([%w_']*)", tchelper)
]]
local function tchelper(first, rest)
   return first:upper()..rest:lower()
end

local function setCursorPos(row, col)
	--[[ position cursor in terminal at row, col ]]
	io.write(string.char(27).."["..row..";"..col.."H")
end

local function clearInputField(row)
	if row >= 0 then
		setCursorPos(row, 0)
		print(blank)
		setCursorPos(row, 0)
	end
end

local function errorMessage(row, errorType, userInput, minValue, maxValue)
	minValue = minValue or 0
	maxValue = maxValue or 0
	local message = "Just pressing the Enter key or spacebar doesn't work" -- default for "noinput"
	if errorType == "string" then
		message = "Try entering text between "..minValue.." and "..maxValue.." characters"
	elseif errorType == "bool" then
		message = "Only anything starting with y or n is accepted"
	elseif errorType == "nan" then
		message = "Try entering a number - "..userInput.." does not cut it"
	elseif errorType == "notint" then
		message = "Try entering a whole number - "..userInput.." does not cut it"
	elseif errorType == "range" then
		message = "Try a number from "..minValue.." to "..maxValue
	end
	
	if row > 0 then
		message = ">>> "..message.." <<<"	-- output to console / terminal
	else
		message = "\n"..message.."..."		-- output to IDE
	end
		
	if row >= 0 then
		clearInputField(row)				-- clear row just used
	end
	print(message)
	if row >= 0 then
		Kboard.sleep(delay)
		clearInputField(row)
	end
end

local function processInput(prompt, minValue, maxValue, dataType, row)
	--[[  This function is private, not called directly from other files ]]
	local validInput = false
	local userInput
	while not validInput do
		clearInputField(row)
		io.write(prompt.."_")
		userInput = io.read():trim()
		local output = userInput
		if dataType == "string" then
			if string.len(userInput) == 0 and minValue > 0 then
				errorMessage(row, "noinput", output)
			else
				if string.len(userInput) > maxValue then
					errorMessage(row, "string", output)
				else
					validInput = true
				end
			end
		else
			if string.len(userInput) == 0 then
				errorMessage(row, "noinput", output)
			else
				if dataType == "bool" then		
					if userInput:sub(1, 1):lower() == "y" then
						userInput = true
						validInput = true
					elseif userInput:sub(1, 1):lower() == "n" then
						userInput = false
						validInput = true
					else
						errorMessage(row, "bool", output)
					end
				else
					if dataType == "int" or dataType == "float" then
						userInput = tonumber(userInput)			
					end
					if userInput == nil then
						errorMessage(row, "nan", output)
					else
						if userInput >= minValue and userInput <= maxValue then
							if math.floor(userInput / 1) ~= userInput and dataType == "int"  then
								errorMessage(row, "notint", output)
							else
								validInput = true
							end
						else
							errorMessage(row, "range", output, minValue, maxValue)
						end
					end
				end
			end
		end
	end
	return userInput
end

function Kboard.getString(prompt, withTitle, minValue, maxValue, row) -- withTitle, minInt and maxInt are given defaults if not passed
	withTitle = withTitle or false
	minValue = minValue or 1
	maxValue = maxValue or 20
	row = row or -1
	if row >= 0 then
		row = row + 1
	end
	local valid = false
	local userInput
	while not valid do
		io.write(prompt.."_")
		userInput = io.read():trim()
		if string.len(userInput) == 0 then
			errorMessage(row, "noinput")
		else		
			if string.len(userInput) >= minValue and string.len(userInput) <= maxValue then
				if withTitle then
					userInput = Kboard.toTitle(userInput)
				end
				valid = true
			else
				errorMessage(row, "string", minValue, maxValue)
			end
		end
	end
	
	return userInput
end

function Kboard.getFloat(prompt, minValue, maxValue, row) -- minInt and maxInt are given defaults if not passed
	minValue = minValue or 0
	maxValue = maxValue or 1000000.0
	row = row or -1
	if row >= 0 then
		row = row + 1
	end

	return processInput(prompt, minValue, maxValue, "float", row)
end

function Kboard.getInteger(prompt, minValue, maxValue, row) -- minInt and maxInt are given defaults if not passed
	minValue = minValue or 0
	maxValue = maxValue or 65536
	row = row or -1
	if row >= 0 then
		row = row + 1
	end

	return processInput(prompt, minValue, maxValue, "int", row)
end
		
function Kboard.getBoolean(prompt, row) -- assumes yes/no type entries from user
	row = row or -1
	if row >= 0 then
		row = row + 1	
	end
	return processInput(prompt, 1, 3, "bool", row)
end
	
function Kboard.toTitle(Text) --converts any string to Title Case
	return Text:gsub("(%a)([%w_']*)", tchelper)
end

function Kboard.sleep(s) 
    --[[ Lua version of Python time.sleep(2) ]]
	local sec = tonumber(os.clock() + s); 
    while (os.clock() < sec) do end 
end

function Kboard.menu(title, list, row)
	--[[ displays a menu using the text in 'title', and a list of menu items (string) ]]
	row = row or -1
	local rows  = -1
	if row >= 0 then
		rows = row + #list + 2
	end
	local index = 1
	print(title)
	for _, item in ipairs(list) do
		if index < 10 then
			print("     "..index..") "..item)
		else
			print("    "..index..") "..item)
		end
		index = index + 1
	end
	print(string.rep("═", 80))
	return Kboard.getInteger("Type the number of your choice (1 to "..index-1 ..")", 1, #list, rows)
end
	
return Kboard
