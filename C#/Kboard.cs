/*
kboard static class returns string, integer, float, boolean and menu choices.
Use:

int row = Kboard.Clear();
string name = Kboard.GetString("What is your name?", true, 1, 10, row);
int age = Kboard.GetInteger("How old are you", 5, 110, row);
double height = Kboard.GetRealNumber("How tall are you?", 0.5, 2.0, row);
bool likesPython = Kboard.GetBoolean("Do you like C#? (y/n)", row);

List<string> options = new List<string> {"Brilliant", "Not bad", "Could do better", "Rubbish"};
int choice =Kboard.Menu("What do think of this utility?", options, row)
*/
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading;

namespace KBoard
{
    internal class Kboard
    {
        public static int Delay = 2000;
        public static int Clear()
        {
            /// Clears the Console (Allows calls from other classes not involved with UI) ///
            Console.Clear();
            return 0;
        }
        private static void ClearInputField(int row)
        {
            /// use SetCursorPos to delete a line of text ///
            if (row >= 0)
            {
                Console.SetCursorPosition(0, row); // left, top 0 based
                Console.Write("".PadRight(Console.WindowWidth - 1));
                Console.SetCursorPosition(0, row);
            }
        }
        private static void ErrorMessage(int row, string errorType, string userInput,  double minValue = 0, double maxValue = 0)
        {
            /// Display error message to the user for <delay> seconds ///
            if (row < 0) row = 0;
            string message = "Just pressing the Enter key or spacebar doesn't work"; // default for "noinput"
            if (errorType == "string")
                message = $"Try entering text between {minValue} and {maxValue} characters";
            else if (errorType == "bool")
                message = "Only anything starting with y or n is accepted";
            else if (errorType == "nan")
                message = $"Try entering a number - {userInput} does not cut it";
            else if (errorType == "notint")
                message = $"Try entering a whole number - {userInput} does not cut it";
            else if (errorType == "range")
                message = $"Try a number from {minValue} to {maxValue}";
            else if (errorType == "intconversion")
                message = $"Try entering a whole number: {userInput} cannot be converted...";
            else if (errorType == "realconversion")
                message = $"Try entering a decimal number: {userInput} cannot be converted...";

            message = $">>> {message} <<<";
            ClearInputField(row);           // clear current line
            Console.Write(message);         // write message
            Thread.Sleep(Delay);            // pause 2 seconds
            ClearInputField(row);           // clear current line
        }
        public static bool GetBoolean(string prompt, int row = -1)
        {
            /// gets a boolean (yes/no) type entry from the user
            string userInput = ProcessInput(prompt, 1, 3, "bool", row);
            return Convert.ToBoolean(userInput);
        }
        public static double GetRealNumber(string prompt, double min, double max, int row = -1)
        {
            /// gets a float / double from the user
            string userInput = ProcessInput(prompt, min, max, "real", row);
            return Convert.ToDouble(userInput);
        }
        public static int GetInteger(string prompt, double min, double max, int row = -1)
        {
            /// Public Method: gets an integer from the user ///
            string userInput = ProcessInput(prompt, min, max, "int", row);
            return Convert.ToInt32(userInput);
        }
        public static string GetString(string prompt, bool withTitle, int min, int max, int row = -1)
        {
            /// Public Method: gets a string from the user ///
            string userInput = ProcessInput(prompt, min, max, dataType:"string", row);
            if (withTitle)
            {
                TextInfo textInfo = new CultureInfo("en-UK", false).TextInfo;
                userInput = textInfo.ToTitleCase(userInput);
            }
            return userInput;
        }
        public static string Input(string prompt, string ending = "_")
        {
            /// Get keyboard input from user (requires Enter) same as Python ///
            Console.Write($"{prompt}{ending}");
            return Console.ReadLine();
        }
        public static int Menu(string title, List<string> textLines, int row = -1)
        {
            /// displays a menu using the text in 'title', and a list of menu items (string)
            /// This menu will re-draw until user enters correct data
            if (title.Length % 2 == 1) title += " ";
            int rows = -1;
            if (row >= 0) rows = row + textLines.Count + 4;
            int maxLen = title.Length;
            foreach(string line in textLines)
            {
                if(line.Length > maxLen + 9)
                    maxLen = line.Length + 9;
            }
            maxLen += 28;
            if (maxLen > Console.WindowWidth - 2)
                maxLen = Console.WindowWidth - 2;
            if (maxLen % 2 == 1)
                maxLen++;

            string filler = new string(' ', (maxLen - title.Length) / 2);
            Print($"╔{new string('═', maxLen)}╗");
            Print($"║{filler}{title}{filler}║");                     // print title
            Print($"╠{new string('═', maxLen)}╣");
            for (int i = 0; i < textLines.Count; i++)
            {
                if (i < 9)  Print($"║     {i + 1}) {textLines[i].PadRight(maxLen - 8)}║");  // print menu options 5 spaces
                else        Print($"║    {i + 1}) {textLines[i].PadRight(maxLen - 8)}║");   // print menu options 4 spaces
            }
            //Print(new string('═', Console.WindowWidth - 1));
            Print($"╚{new string('═', maxLen)}╝");
            int userInput = GetInteger($"Type the number of your choice (1 to {textLines.Count})",  1, textLines.Count, rows);
            return userInput - 1;
        }
        public static int Print(string text = "")
        {
            /// Replicates Python / Lua print() and returns no of lines printed ///
            Console.WriteLine(text);
            int numLines = text.Count(x => x == '\n') + 1;
            return numLines;
        }
        public static void Sleep(int delay)
        {
            /// replicates Python time.sleep() in seconds ///
            if (delay < 100) delay *= 1000;
            Thread.Sleep(delay);
        }
        private static string ProcessInput(string prompt, double min, double max, string dataType, int row)
        {
            /// validate input, raise error messages until input is valid  ///
            bool valid = false;
            string userInput = "";
            while (!valid)
            {
                ClearInputField(row);
                userInput = Input(prompt);
                if (dataType == "string")
                {
                    if (userInput.Length == 0 && min > 0) ErrorMessage(row, "noinput", userInput);
                    else if (userInput.Length > max) ErrorMessage(row, "string", userInput, min, max);
                    else valid = true;
                }
                else //integer, float, bool
                {
                    if (userInput.Length == 0)                                      // just Enter pressed
                        ErrorMessage(row, "noinput", userInput);
                    else
                    {
                        if (dataType == "bool")
                        {
                            if (userInput.Substring(0, 1).ToLower() == "y")
                            {
                                userInput = "true";
                                valid = true;
                            }
                            else if (userInput.Substring(0, 1).ToLower() == "n")
                            {
                                userInput = "false";
                                valid = true;
                            }
                            else  ErrorMessage(row, "bool", userInput);
                        }
                        if (dataType == "int" || dataType == "real")                // integer / float / double
                        {
                            if (double.TryParse(userInput, out double conversion))  // is a number!
                            {
                                if (conversion >= min && conversion <= max)         // within range!
                                {
                                    if (dataType == "int")                          // check if int
                                    {
                                        if (int.TryParse(userInput, out int intconversion))
                                        {
                                            valid = true;                           // userInput can be converted to int
                                        }
                                        else ErrorMessage(row, "notint", userInput);// real number supplied
                                    }
                                    else valid = true;                              // userInput can be converted to float/double/decimal
                                }
                                else ErrorMessage(row, "range", userInput, min, max);// out of range
                            }
                            else ErrorMessage(row, "nan", userInput);               // not a number
                        }
                    }
                }
            }
            return userInput; //string can be converted to bool, int or float
        }
    }
}
