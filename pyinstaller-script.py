import os, subprocess, sys
from pathlib import Path

""" Configuration """
folder_path = Path(__file__).parent

scipy_dlls_path = Path(sys.executable).parent / "Lib" / "site-packages" / "scipy" / ".libs"
dll_path = Path("dlls")
python_executable_path = "python"
bot_folder_path = folder_path / "mybot_obfuscated"
run_file_path = folder_path / "mybot_obfuscated/run.py"
output_folder_path = folder_path / "mybot_compiled"
python_sc2_path = folder_path / "sc2"
ecryption_key_path = folder_path / "encryptionkey.txt"


def build_pyinstaller_arguments(python_executable_path, starcraft2_path, python_sc2_path, run_file_path, output_folder_path, ecryption_key_path) -> list:
    """ Returns a list of subprocess.Popen(LIST) arguments """
    arguments = []

    arguments.append(python_executable_path)

    # Disable asserts, does not seem to work anymore?
    # arguments.append("-OO")

    arguments.append("-m")
    arguments.append("PyInstaller")

    arguments.append("--onefile")

    sc2_dlls = ["icuin52.dll", "icuuc52.dll", "icudt52.dll"]
    for sc2_dll in sc2_dlls:
        dll_path = os.path.join(starcraft2_path, sc2_dll)
        arguments.append("--add-binary")
        arguments.append(f"{dll_path};.")

    arguments.append("--add-data")
    arguments.append(f"{python_sc2_path};sc2")

    # Add scipy dlls
    for dll_path in scipy_dlls_path.iterdir():
        arguments.append("--add-binary")
        arguments.append(f"{dll_path};.")

    # Add paths that may be encrypted during the packing process
    arguments.append("--paths")
    arguments.append(f"{bot_folder_path}")

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
    arguments.append(f"{output_folder_path}")

    arguments.append(f"{run_file_path}")

    assert all(isinstance(i, str) for i in arguments)

    print("Pyinstaller Arguments: {}".format(arguments))
    print("Exact command line call: {}".format(" ".join(arguments)))
    return arguments



if __name__ == "__main__":

    # Create the .exe file
    pyinstaller_arguments = build_pyinstaller_arguments(python_executable_path, dll_path, python_sc2_path, run_file_path, output_folder_path, ecryption_key_path)

    os.makedirs(output_folder_path, exist_ok=True)

    process = subprocess.Popen(pyinstaller_arguments, stdout=subprocess.PIPE)
    result = process.communicate()

    print("Success.")

