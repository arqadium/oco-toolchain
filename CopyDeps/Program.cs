using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace CopyDeps
{
    public class Program
    {
        static int Main(string[] args)
        {
            Console.WriteLine();
            Console.WriteLine("Project Dependency Copying Utility");
            Console.WriteLine("Part of the OCo Working Set Toolchain");
            Console.WriteLine("Copyright (C) 2017 Trinity Software, LLC");
            Console.WriteLine();

            int invalid = ValidateArgs(args);

            if(invalid != 0) { Console.Read(); return invalid; }

            args[0].TrimEnd('\\');
            args[1].TrimEnd('\\');

            string assetDir = args[0] + "\\Assets\\" + args[3];
            string libsDir = args[0] + "\\Libraries\\" + args[2] + "\\" +
                args[3];
            var dirsToMake = new List<string>();
            var filesToCopyFrom = new List<string>();
            var filesToCopyTo = new List<string>();

            try
            {
                var assetSettings = ParseINI(assetDir + ".ini");
                ICollection<string> setKeys = assetSettings.Keys;

                foreach(string key in setKeys)
                {
                    // Ensure the current section corresponds to a valid file
                    string filePath = assetDir + "\\" + key;
                    if(!File.Exists(filePath))
                    {
                        throw new Exception("Section name '" + key + "' " +
                            "does not correspond to an accessible file in " +
                            "the assets directory for the current target");
                    }

                    var sec = assetSettings[key];
                    string badOP = "Invalid value in OutputPath property " +
                        "of section '" + key + "'; ";

                    // If we're not going to copy the file, move on to the
                    // next section
                    if(sec["copy"] == "0")
                    {
                        continue;
                    }
                    // Validate the property's value (it's not zero, so...)
                    else if(sec["copy"] != "1")
                    {
                        throw new Exception("Invalid value in Copy property" +
                            " of section '" + key + "'; must be 0 or 1");
                    }

                    // Validate the output path, and make sure any directories
                    // it specifies are queued for creation
                    if(sec.Keys.Contains("outputpath"))
                    {
                        if(!sec["outputpath"].StartsWith("\\"))
                        {
                            throw new Exception(badOP + "path must begin " +
                                "with a backslash");
                        }

                        if(sec["outputpath"].EndsWith("\\"))
                        {
                            throw new Exception(badOP + "path cannot be a " +
                                "directory");
                        }

                        string relPath = sec["outputpath"].TrimStart('\\');
                        
                        if(relPath.Where(x => x == '\\').Count() > 0)
                        {
                            string[] tmp = relPath.Split('\\');
                            string dir = String.Join("\\", tmp.Take(tmp.Length
                                - 1).ToArray());

                            dirsToMake.Add(args[1] + "\\" + dir);
                        }
                        
                        // Set location to copy file to
                        filesToCopyTo.Add(args[1] + "\\" + relPath);
                    }
                    else
                    {
                        // Set location to copy file to
                        filesToCopyTo.Add(args[1] + "\\" + key);
                    }

                    // Queue the file source for copying in the next phase
                    filesToCopyFrom.Add(filePath);
                }

                var libs = Directory.GetFiles(libsDir);

                foreach(string lib in libs)
                {
                    string[] tmp = lib.Split('\\');
                    string libName = tmp.Reverse().Take(1).ToArray()[0];
                    filesToCopyTo.Add(args[1] + "\\" + libName);
                    filesToCopyFrom.Add(lib);
                }

                foreach(string dir in dirsToMake)
                {
                    Console.WriteLine(dir);
                    Directory.CreateDirectory(dir);
                }

                for(int i = 0; i < filesToCopyFrom.Count; i++)
                {
                    File.Copy(filesToCopyFrom[i], filesToCopyTo[i], true);
                }

            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine(ex.StackTrace);

                Console.Read();
                return -4;
            }

            Console.WriteLine("Dependency copy completed successfully.");

            Console.Read();
            return 0;
        }

        static int ValidateArgs(string[] args)
        {
            if(args.Length < 4)
            {
                Console.WriteLine("Insufficient number of arguments " +
                    "provided: " + String.Join("\n", args) + "\nExiting...");

                return -1;
            }
            
            if(!Directory.Exists(args[0]))
            {
                Console.WriteLine("The project dependencies directory '" +
                    args[0] + "' does not exist or is inaccessible.\n" +
                    "Exiting...");

                return -2;
            }
            
            if(!Regex.Match(args[2].ToLower(), "^(arm|x64|x86)$").Success)
            {
                Console.WriteLine("The project target architecture '" +
                    args[2] + "' is invalid; must be ARM, x64, or x86.\n" +
                    "Exiting...");

                return -3;
            }

            if(!Regex.Match(args[3].ToLower(), "^(debug|release)$").Success)
            {
                Console.WriteLine("The project target configuration" +
                    args[3] +  " is invalid; must be Debug or Release.\n" +
                    "Exiting...");
            }

            return 0;
        }

        static Dictionary<string, Dictionary<string, string>>
            ParseINI(string filePath)
        {
            string[] iniLines = File.ReadAllLines(filePath).Where(x =>
                !String.IsNullOrEmpty(x) && !x.StartsWith(";")).ToArray();
            string[] badLines = new string[0];
            string curSection = "";
            var ret = new Dictionary<string, Dictionary<string, string>>();

            foreach (string line in iniLines)
            {
                if (line.StartsWith("["))
                {
                    string name = line.TrimStart('[').TrimEnd(']');

                    ret.Add(name, new Dictionary<string, string>());
                    curSection = name;
                }
                else if (line.Contains('='))
                {
                    string[] kv = line.Split("=".ToCharArray(), 2);
                    string key = kv[0].ToLower();

                    if(ret.Keys.Contains(key))
                    {
                        badLines[badLines.Length] = line;

                        continue;
                    }

                    ret[curSection].Add(key, kv[1]);
                }
                else
                {
                    badLines[badLines.Length] = line;
                }
            }

            if (badLines.Length > 0)
            {
                throw new Exception("Parsing failed due to malformed syntax" +
                    "; the following lines were found to be invalid:\n" +
                    String.Join("\n", badLines) + "\n");
            }

            return ret;
        }
    }
}
