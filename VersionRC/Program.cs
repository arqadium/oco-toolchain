using System;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

namespace VersionRC
{
    class Program
    {
        static int Main(string[] args)
        {
            Console.WriteLine();
            Console.WriteLine("RC-based Project Version Autoincrementer");
            Console.WriteLine("Part of the OCo Working Set Toolchain");
            Console.WriteLine("Copyright (C) 2017 Trinity Software, LLC");
            Console.WriteLine();
            
            if(args.Length < 1 || !args[0].EndsWith(".rc"))
            {
                Console.WriteLine("ERROR: No RC file specified. Exiting...");
                
                return 1;
            }
            
            string inText = File.ReadAllText(args[0],
                Encoding.ASCII);
            string outText = inText;
            Regex exp = new Regex(
                "Version\",(\\s*)\"([0-9]+)\\.([0-9]+)\\.([0-9]+)(\\-([0-9]+))?"
                );

            MatchCollection matches = exp.Matches(inText);

            foreach(Match match in matches)
            {
                string replText = "";

                if(match.Groups[5].Value == ""
                || match.Groups[5].Value == "-0")
                {
                    replText = "Version\"," + match.Groups[1].Value + "\"" +
                        match.Groups[2].Value + "." + match.Groups[3].Value +
                        "." + match.Groups[4].Value + "-1";
                }
                else
                {
                    ulong ver = Convert.ToUInt64(match.Groups[6].Value) + 1;

                    replText = "Version\"," + match.Groups[1].Value + "\"" +
                        match.Groups[2].Value + "." + match.Groups[3].Value +
                        "." + match.Groups[4].Value + "-" + ver.ToString();
                }

                outText = Regex.Replace(outText, match.Groups[0].Value,
                    replText);
            }

            File.WriteAllText(args[0], outText, Encoding.ASCII);
            Console.WriteLine("Updated build number.");

            return 0;
        }
    }
}
