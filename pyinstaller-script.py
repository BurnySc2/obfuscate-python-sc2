import os, subprocess, sys

""" Configuration """
dirname = os.path.dirname(__file__)

starcraft2_path = r"C:\games\StarCraft II"
pyinstaller_path = r"C:\python366_32bit\Scripts\pyinstaller.exe"
bot_folder_path = os.path.join(dirname, "mybot_obfuscated")
run_file_path = os.path.join(dirname, "mybot_obfuscated/run.py")
output_folder_path = os.path.join(dirname, "mybot_compiled")


def build_pyinstaller_arguments(pyinstaller_path, starcraft2_path, python_sc2_path, run_file_path, output_folder_path, ecryption_key_path) -> list:
    """ Returns a list of subprocess.Popen(LIST) arguments """
    arguments = []

    if os.path.isfile(pyinstaller_path):
        arguments.append(pyinstaller_path)
    else:
        print("PyInstaller not found, using default pyinstaller argument: pyinstaller")
        arguments.append("pyinstaller")

    arguments.append("--onefile")

    sc2_dlls = ["Support64\icuin52.dll", "Support64\icuuc52.dll", "Support64\icudt52.dll"]
    for sc2_dll in sc2_dlls:
        dll_path = os.path.join(starcraft2_path, sc2_dll)
        arguments.append("--add-binary")
        arguments.append(dll_path + ";.")

    arguments.append("--add-data")
    arguments.append(python_sc2_path + ";sc2")

    # Add paths that may be encrypted during the packing process
    arguments.append("--paths")
    arguments.append(bot_folder_path)

    arguments.append("--clean")
    arguments.append("--noconfirm")

    # Encryption using the --key=mykey pyinstaller parameter. Checks if pycrypto is installed
    try:
        encryption_key = ""
        import pycrypt
        if os.path.isfile(ecryption_key_path):
            with open(ecryption_key_path) as f:
                # Remove possibly unwanted newline, tab or space characters, as they also might be invalid characters
                encryption_key = f.read().strip(" \n\t")
        if encryption_key != "":
            arguments.append("--key")
            arguments.append(encryption_key)
    except ImportError:
        print("Pycrypto not detected. Skipping encryption")

    arguments.append("--distpath")
    arguments.append(output_folder_path)

    arguments.append(run_file_path)
    print("Pyinstaller Arguments: {}".format(arguments))
    print("Exact command line call: {}".format(" ".join(arguments)))
    return arguments



if __name__ == "__main__":
    python_sc2_path = os.path.join(dirname, "sc2")
    ecryption_key_path = os.path.join(dirname, "encryptionkey.txt")

    # Create the .exe file
    pyinstaller_arguments = build_pyinstaller_arguments(pyinstaller_path, starcraft2_path, python_sc2_path, run_file_path, output_folder_path, ecryption_key_path)

    process = subprocess.Popen(pyinstaller_arguments, stdout=subprocess.PIPE)
    result = process.communicate()

    print("Success.")

