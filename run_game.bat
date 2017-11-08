del "%~dp00_stn.log" /F /Q
del "%~dp01_Settler.log" /F /Q

halite.exe -d "360 240" "python MyBot.py" "python MyBot_Origional.py"
