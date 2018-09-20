import os, subprocess, sys

""" Configuration """
dirname = os.path.dirname(__file__)

starcraft2_path = r"C:\games\StarCraft II"
init_file_path = os.path.join(dirname, "mybot_obfuscated/__init__.py")
bot_file_path = os.path.join(dirname, "mybot_obfuscated/CreepyBot.py")
run_file_path = os.path.join(dirname, "mybot_obfuscated/run.py")
output_folder_path = os.path.join(dirname, "mybot_compiled")



def build_pyinstaller_arguments(starcraft2_path, python_sc2_path, run_file_path, output_folder_path) -> list:
    """ Returns a list of subprocess.Popen(LIST) arguments """
    arguments = []
    arguments.append("pyinstaller")
    arguments.append("--onefile")

    sc2_dlls = ["Support64\icuin52.dll", "Support64\icuuc52.dll", "Support64\icudt52.dll"]
    for sc2_dll in sc2_dlls:
        dll_path = os.path.join(starcraft2_path, sc2_dll)
        arguments.append("--add-binary")
        arguments.append(dll_path + ";.")

    arguments.append("--add-data")
    arguments.append(python_sc2_path + ";sc2")

    arguments.append("--add-data")
    arguments.append(bot_file_path + ";.")

    arguments.append("--add-data")
    arguments.append(init_file_path + ";.")

    arguments.append("--clean")
    arguments.append("--noconfirm")

    arguments.append("--distpath")
    arguments.append(output_folder_path)

    arguments.append(run_file_path)
    print("Pyinstaller Arguments: {}".format(arguments))
    print("Exact command line call: {}".format(" ".join(arguments)))
    return arguments



if __name__ == "__main__":
    python_sc2_path = os.path.join(dirname, "sc2")

    # Create the .exe file
    pyinstaller_arguments = build_pyinstaller_arguments(starcraft2_path, python_sc2_path, run_file_path, output_folder_path)

    process = subprocess.Popen(pyinstaller_arguments, stdout=subprocess.PIPE)
    result = process.communicate()

    print("Success.")

