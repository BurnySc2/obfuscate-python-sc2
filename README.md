#WORK IN PROGRESS

## This is a repo containing two scripts to obfuscate and compile a [python-sc2 bot](https://github.com/Dentosal/python-sc2) to .exe

# Installation

- Download the repo
- `pip install -r requirements.txt`

## Obfuscating and compiling an example
- `python obfuscate-script.py`

    A folder called `mybot_obfuscated` will be created with the bot files now obfuscated and a copy of `python-sc2/sc2/`
- `python pyinstaller-script.py`

    A folder called `mybot_compiled` will be created which has a single `.exe` file that can be run.

- run `mybot_compiled/run.exe`

## How does it perform obfuscation?

It parses your bot file(s) and the `python-sc2/sc2` files for class names, function names and parameter names, enums and imports aswell as a few variable names from the `python-sc2/sc2` files, so that you can still call `self.state.units` for example.

All those names will be put in the config file, prepared for the [Opy](https://github.com/QQuick/Opy) script to run.

Opy creates a new folder with files obfuscated.

Then it copies the original `python-sc2/sc2` files over the obfuscated ones, as those do not need to be obfuscated. Obfuscation of those files results in errors.

## How does it compile to an `.exe`?

It uses pyinstaller with a command similar to

`pyinstaller --onefile --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icuin52.dll;." --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icuuc52.dll;." --add-binary="C:\Program Files (x86)\StarCraft II\Support64\icudt52.dll;." --add-data="python-sc2\sc2;sc2" --clean --distpath="mybot_compiled" example_bot.py`

## Issues

- At the current state, the compiled [ladder bot](https://github.com/Hannessa/python-sc2-ladderbot) does not properly start with the ladder manager.
- There may be some enums not being taken care of.