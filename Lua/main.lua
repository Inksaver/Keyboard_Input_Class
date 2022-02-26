kb = require "lib.kboard"
Console = require "lib.console"

local function getRow(row, rows)
	--[[
	If running from an IDE, row should always be -1
	so no SetCursorPos is used in Kboard library.
	Otherwise increment row by rows
	]]
	rows = rows or 1
	if row == -1 then
		return -1
	else
		return row + rows
	end
end

function testKboard()
	--[[
	If in IDE row is kept at -1, which disables the SetCursorPos in Kboard library
	so the output scrolls as normal
	Otherwise incorrect answers keep the output on the same linefred
	]]
	Console.Clear()
	local row = -1				-- assume running in IDE
	if Console.IsConsole then	-- running in console / terminal
		row = 0					-- start row at 0
	end
	local name = kb.getString("What is your name?", true, 1, 10, row)
	print("User name : "..name.." <- See how I used a capital letter!")
	
	row = getRow(row, 2)		-- if in IDE row = -1, else row = 2
	local age = kb.getInteger("How old are you?", 5, 110, row)
	print("User age : ".. age.. " years old.")
	
	row = getRow(row, 2)		-- if in IDE row = -1, else row = 4
	local height = kb.getFloat("How tall are you?", 0.5, 2.0, row)
	print("User height : ".. height.." metres tall.")
	
	row = getRow(row, 2)		-- if in IDE row = -1, else row = 6
	local likesPython = kb.getBoolean("Do you like Python? (y/n)", row)
	print("User likes Python : "..tostring(likesPython))
	kb.sleep(2)					-- pause 2 secs
	
	
	row = Console.Clear()		-- resets row to -1 / 0
	local title = "What do think of this utility?"
	local options = {"Brilliant", "Not bad", "Could do better", "Rubbish"}
	local choice = kb.menu(title, options, row, Console.WindowWidth)
	print("User thinks this utility is : "..options[choice])
end

function main()
	--[[ Everything runs from here ]]
	testKboard()
	if Console.IDE == "cmd" then	-- running in console / terminal
		io.write("Enter to quit")
		io.read()
	end
end
main()
