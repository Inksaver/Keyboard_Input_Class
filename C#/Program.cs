using System.Collections.Generic;

namespace KBoard
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int row = Kboard.Clear();   // row 0
            string name = Kboard.GetString(prompt:"What is your name?", withTitle:true, min:1, max:10, row:row);
            Kboard.Print($"User name : {name} <- See how I used a capital letter!");

            row += 2;                   // row
            int age = Kboard.GetInteger("How old are you", 5, 110, row);
            Kboard.Print($"User age : {age} years old");

            row += 2;
            double height = Kboard.GetRealNumber("How tall are you?", 0.5, 2.0, row);
            Kboard.Print($"User height : {height} metres tall");
            row += 2;
            bool likesPython = Kboard.GetBoolean("Do you like Python? (y/n)", row);
            Kboard.Print($"User likes Python : {likesPython}");
            Kboard.Sleep(2);

            row = Kboard.Clear();
            string title = "What do think of this utility?";
            List<string> options = new List<string> { "Brilliant", "Not bad", "Could do better", "Rubbish" };
            int choice = Kboard.Menu(title, options, row);
            Kboard.Print($"User thinks this utility is : {options[choice]}");
            Kboard.Input("Press Enter to quit", "...");
        }
    }
}
