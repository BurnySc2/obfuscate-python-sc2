::"C:\python366_32bit\python.exe" -m pip install sc2 --upgrade
::"C:\python366_32bit\python.exe" -m pip install pycrypt --upgrade
::"C:\python366_32bit\python.exe" -m pip install pyinstaller --upgrade

::timeout 1

:: Updates the list of functions and imports from sc2/ folder
python regex_output_config.py

::timeout 1

robocopy mybot tempFolder /E

:: Remove previously obfuscated bot
RD /Q /S mybot_obfuscated

python opy.py tempFolder mybot_obfuscated tempFolder/opy_config.txt

python pyinstaller-script.py

robocopy sc2 mybot_obfuscated/sc2 /E
