Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Users\OU000150\.local\bin\uv"" ""run"" ""SCRIPT_NAME_TO_BE_REPLACED"" """ & WScript.Arguments(0) & """", 0, False 