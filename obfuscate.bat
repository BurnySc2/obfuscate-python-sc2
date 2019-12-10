::timeout 1

:: Updates the list of function names and imports from sc2/ folder, these names will then be ignored and not obfuscated
python regex_output_config.py

::timeout 1

:: Copy bot folder to target temporary folder
robocopy mybot tempFolder /E

:: Remove previously obfuscated bot
RD /Q /S mybot_obfuscated

:: Obfuscate using opy.py
python opy.py tempFolder mybot_obfuscated tempFolder/opy_config.txt

:: Create .exe file in mybot_compiled
python pyinstaller-script.py

:: Copy the sc2/ folder the obfuscated directory
robocopy sc2 mybot_obfuscated/sc2 /E
