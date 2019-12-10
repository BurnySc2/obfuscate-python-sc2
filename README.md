#WORK IN PROGRESS

## This is a repo containing two scripts to obfuscate and compile (and encrypt) a [python-sc2 bot](https://github.com/BurnySc2/python-sc2) to .exe

# Installation

- Download the repo

- `pip install -r requirements.txt` or `python -m pip -r requirements.txt`

## Obfuscating and compiling

- Change your encryption key in `encryptionkey.txt` (not tested if this step works properly)

- Run the obfuscate.bat or the commands in it

## How does it perform obfuscation?

It parses your bot file(s) and the `python-sc2/sc2` files for class names, function names and parameter names, enums and imports aswell as a few variable names from the `python-sc2/sc2` files, so that you can still call `self.state.units` for example. All of those found names will be added to the `opy_config_default.txt` file in the `plain_names` variable.

Now the script runs [Opy](https://github.com/QQuick/Opy).

Opy creates a new folder with files obfuscated.

Then it copies the original `python-sc2/sc2` files over the obfuscated ones, as those do not need to be obfuscated. Obfuscating the `python-sc2/sc2` files would result in errors.

## How does it compile to an `.exe`?

It uses pyinstaller with a command similar to

`pyinstaller --onefile --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icuin52.dll;." --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icuuc52.dll;." --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icudt52.dll;." --add-data="python-sc2\sc2;sc2" --clean --distpath="mybot_compiled" example_bot.py`

Thanks to AiSee to figuring this one out!

## FAQ

### Why is the .exe file so big?

I included all the scipy .dll files which are about 30mb big. The resulting bot should be around 50mb.

### I use another library but it keeps obfuscating the function methods and as a result it crashes

Create a new entry of your library name, e.g. `numpy`, and add it to the list of ignore names in `opy_config_default.txt` in the variable `external_modules`. 

### Can't the pyinstaller file be easily extracted?

If not encrypted, yes it can via [python-exe-unpacker](https://github.com/countercept/python-exe-unpacker) and then decompiled using [uncompyle6](https://pypi.org/project/uncompyle6/).
However, it may still take some times to read the code obfuscated by [Opy](https://github.com/QQuick/Opy).

## Issues

- Does not work with the class `__slots__` magic method

- Does not work with f strings

- There may be some variables of the python-sc2 library not being taken care of, especially variables from protobuf, e.g. unit._proto.movement_speed. Just add these variables to `plain_names` in opy_config_default.txt
