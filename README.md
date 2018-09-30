#WORK IN PROGRESS

## This is a repo containing two scripts to obfuscate and compile (and encrypt) a [python-sc2 bot](https://github.com/Dentosal/python-sc2) to .exe

# Installation

- Download the repo

- `pip install -r requirements.txt` or `python -m pip -r requirements.txt`

- In `pyinstaller-script.py` you need to change your StarCraft 2 and PyInstaller path to match the files on your file system
    
    ```
    starcraft2_path = r"C:\games\StarCraft II"
    pyinstaller_path = r"C:\python366_32bit\Scripts\pyinstaller.exe"
    ```

- If you also want to encrypt your code with an encryption key, you have to do one of the following `Preparation for Encryption` (only tested on windows):

## Preparation for Encryption - Variant 1 (700mb)

- You may have to install a fresh installation of python 3.6 32bit

- Install MinGW_w64 by following the instructions [here](https://wiki.python.org/moin/WindowsCompilers#GCC_-_MinGW-w64_.28x86.2C_x64.29)

- Restart your computer

- Run `pip install pycrypt` or `python -m pip install pycrypt`

- Now just run `python pyinstaller-script.py` to create your `run.exe`. Don't forget to change your encryption key in `encryptionkey.txt`.


## Preparation for Encryption - Variant 2 (1.4gb)

- You may have to install a fresh installation of python 3.6 32bit

- Install the [visual studio c++ build tools from here](https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.0_standalone:_Build_Tools_for_Visual_Studio_2017_.28x86.2C_x64.2C_ARM.2C_ARM64.29)

- You may have to restart your computer

- Try `pip install pycrypto` or `python -m pip install pycrypt`

- If that doesn't work and you get the following error:
    
    ```C:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt\inttypes.h(26): error C2061: syntax error: identifier 'intmax_t'```

    edit the file `"C:\Program Files (x86)\Windows Kits\10\Include\10.0.17134.0\ucrt\inttypes.h"` and add a 
    ```
    #define intmax_t long long
    #define uintmax_t unsigned long long
    ```
    before the line of the first error message, which should be line 25 before this line: `typedef struct`
    
    This is described [here](http://www.xavierdupre.fr/app/pymyinstall/helpsphinx/blog/2017/2017-01-03_pycrypto.html) but I copied it in case the site goes down.

- Now try installing pycrypto again

- Now just run `python pyinstaller-script.py` to create your `run.exe`. Don't forget to change your encryption key in `encryptionkey.txt`.

## Obfuscating and compiling an example
- Run `python obfuscate-script.py`

    A folder called `mybot_obfuscated` will be created with the bot files now obfuscated and a copy of `python-sc2/sc2/`
- Run `python pyinstaller-script.py`

    A folder called `mybot_compiled` will be created which has a single `.exe` file that can be run.

- Run `mybot_compiled/run.exe`

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

### I use another library but it keeps obfuscating the function methods and as a result it crashes

Create a new entry of your library name, e.g. `numpy`, and add it to the list of ignore names in `opy_config_default.txt` in the variable `external_modules`. 

### Can't the pyinstaller file be easily extracted?

If not encrypted, yes it can via [python-exe-unpacker](https://github.com/countercept/python-exe-unpacker).
However, it may still take some times to read the code obfuscated by [Opy](https://github.com/QQuick/Opy).

## Issues

- There may be some enums not being taken care of.