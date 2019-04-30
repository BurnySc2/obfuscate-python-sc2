import subprocess
import os, subprocess, re, shutil

""" Configuration """
dirname = os.path.dirname(__file__)

python_sc2_sc2_path = os.path.join(dirname, "sc2")
inputFolder = os.path.join(dirname, "mybot")
outputFolder = os.path.join(dirname, "mybot_obfuscated")
opyFilePath = os.path.join(dirname, "opy.py")
configDefaultPath = os.path.join(dirname, "opy_config_default.txt")
tempFolder = os.path.join(dirname, "tempFolder")

verbose = True



def build_obfuscate_config(input_folder, config_path, config_output_path):
    """ Checks all .py files in input_folder for imports, function names and class names and then adds them to the config file from config_path (in the plain_names variable) """
    import re

    """
    from sc2.data import race_gas, race_worker, race_townhalls, ActionResult, Attribute, Race, Difficulty
    from sc2.ids.unit_typeid import (
        BARRACKS,
        COMMANDCENTER,
    )
    """
    imports_pattern1 = "(from) ([\w.]+) (import) (\()?((\n[ \t])?([\w, ]+))+(\s\))?"
    import1 = re.compile(imports_pattern1)
    """
    import sc2 as sc
    import networkx as nx, matplotlib as plt
    """
    imports_pattern2 = "(import) (([\w. ]+) (as) ([\w.]+),?)+"
    import2 = re.compile(imports_pattern2)
    """
    import random, json, time, math, copy
    """
    imports_pattern3 = "(import) ([\w,. ]+)"
    import3 = re.compile(imports_pattern3)
    """
    from s2clientprotocol import (
        sc2api_pb2 as sc_pb,
        raw_pb2 as raw_pb,
        data_pb2 as data_pb,
        common_pb2 as common_pb,
        error_pb2 as error_pb
    )
    """
    imports_pattern4 = "([a-z0-9_]+) (as) ([a-z0-9_]+)"
    import4 = re.compile(imports_pattern4)
    imports_pattern5 = "from (\w+) import \("
    import5 = re.compile(imports_pattern5)

    """
    class GroupsManager:
    class GroupsManager(object):    
    class DragonBot(burny_basic_ai.BurnyBasicAI):    
    class BurnyBasicAI(General, Frequentactions, Position, Conditions, sc2.BotAI):
    """
    class_pattern = "(class) ([\w]+)(\([\w,.\[\]\s]*\))*:"
    class1 = re.compile(class_pattern)

    """
    def createNewGroup(self, groupType: str) -> IdleGroup2:
    def unassignReinforcements(self, bot: BotAI, group: IdleGroup, units: Union[Units, Unit, Set[int], int]=None, disbandGroupWhenEmpty: bool=True):
    def findStealableUnits(self, bot: BotAI, group: Union[IdleGroup, str]=None, returnTags=False) -> Union[Units, Set[int]]:
    async def updateAllGroups(self, bot: BotAI):
    def warp_in(self, unit, placement, *args, **kwargs):
    def attack(self, *args, **kwargs):    
    async def get_available_abilities(self, units: Union[List[Unit], Units], ignore_resource_requirements=False) -> List[List[AbilityId]]:
    def closest(self, ps: Union["Units", List["Point2"], Set["Point2"]]) -> Union["Unit", "Pointlike"]:
    def empty_func():
    def towards(
        self, p: Union["Unit", "Pointlike"], distance: Union[int, float] = 1, limit: bool = False
    ) -> "Pointlike":
    """
    # function_pattern = "(async )?(def) ([\w]+)\(([\w:,.=\[\]\"* ]+)\)([->\[\],\w\" ]+)*:"
    # function_pattern = "(async )?def ([\w]+)\((?:self ?,)? *([\*,:\[\]=\"\w ]*)\)"
    function_pattern = "(async )?def ([\w]+)\(([\s\n]+)?(?:self ?,)? *([\*,:\[\]=\"\w ]*)([\s\n]+)?\)"
    function1 = re.compile(function_pattern)

    # All enums from sc2/ids/*.py
    """
    class UnitTypeId(enum.Enum):
        NOTAUNIT = 0
        SYSTEM_SNAPSHOT_DUMMY = 1
        BALL = 2
        STEREOSCOPICOPTIONSUNIT = 3
        COLOSSUS = 4
    class UpgradeId(enum.Enum):
        TERRANINFANTRYWEAPONSLEVEL1 = 7
        TERRANINFANTRYWEAPONSLEVEL2 = 8
        TERRANINFANTRYWEAPONSLEVEL3 = 9
        SS_INTERCEPTOR = 1035
    """
    enum_class_pattern = "(?:([A-Z_0-9]+) = \d+)"
    enum_class1 = re.compile(enum_class_pattern)



    # All enums from sc2/data.py
    all_enums = ["UnitTypeId", "UpgradeId", "AbilityId", "BuffId", "EffectId", "PlayerType", "Difficulty", "Status", "Result", "Alert", "ChatChannel", "Race", "DisplayType", "Alliance", "CloakState", "Attribute", "TargetType", "Target", "ActionResult", "CreateGameError", "Weapon", "ActionChat", "ResponseCreateGame"]
    additional_methods = ["parent", "path", "logging", "argparse", "parser", "args", "aiohttp"]
    enums_pattern1 = "({})\.(\w+)".format("|".join(all_enums + additional_methods))
    enums1 = re.compile(enums_pattern1)

    """
    Race(self._game_info.player_races[self.enemy_id])
    """
    enums_pattern2 = "(?:{})\(([\w\.\[\]\(\)]+)\)".format("|".join(all_enums))
    enums2 = re.compile(enums_pattern2)

    """
    self._proto = proto       
    self.players = [Player.from_proto(p) for p in proto.player_info]
    self.map_size = Size.from_proto(proto.start_raw.map_size)
    self.pathing_grid: PixelMap = PixelMap(proto.start_raw.pathing_grid)
    self.terrain_height: PixelMap = PixelMap(proto.start_raw.terrain_height)
    self.placement_grid: PixelMap = PixelMap(proto.start_raw.placement_grid)
    self.playable_area = Rect.from_proto(proto.start_raw.playable_area)
    self.map_ramps: List[Ramp] = self._find_ramps()
    self.player_races: Dict[int, "Race"] = {p.player_id: p.race_actual or p.race_requested for p in proto.player_info}
    self.start_locations: List[Point2] = [Point2.from_proto(sl) for sl in proto.start_raw.start_locations]
    self.player_start_location: Point2 = None # Filled later by BotAI._prepare_first_step
    """
    sc2_init_variables_pattern = "(?:[ \t]+)?self.(\w+)(?:[: \w,\[\]\"]+)?="
    sc2_init_variables = re.compile(sc2_init_variables_pattern)

    """    
    if not hasattr(self, "currentBuildOrder"):        
    if not getattr(self, "currentBuildOrder"):
    if not setattr(self, "currentBuildOrder"):
    hasattr(self.currentBuildOrder, "attackUnits")
    """
    attr_pattern = "(?:not )?(\w{1,3}attr)\((?:[\.\w]+),\s?\"?([\w\[\]\(\)]+)\"?\)"
    attr1 = re.compile(attr_pattern)



    from typing import List, Set, Tuple
    def stripAndSplit(string: str) -> List[str]:
        string = string
        for replaceStr in "->:=[]()":
            string = string.replace(replaceStr, "")
        string = string.replace(" ", ",")
        string = string.split(",")
        return string

    def addResult(mySet: Set[str], result: List[Tuple[str]], isFunction=False):
        for match in result:
            if isinstance(match, str):
                # match = [match]
                mySet.add(match)
                continue
            for indexWord, wordOrWords in enumerate(match):
                for index, keyword in enumerate(stripAndSplit(wordOrWords)):
                    # dont include commented out code
                    if index == 0 and "#" in keyword:
                        break
                    # dont include function arguments
                    if isFunction and indexWord >= 2:
                        # Add function parameter names
                        if wordOrWords.count(" ") + wordOrWords.count("=") == 0:
                            mySet.add(wordOrWords)
                        else:
                            keywords = stripAndSplit(wordOrWords.replace("=", ",").replace(" ", "").replace(":", ","))
                            for word in keywords:
                                mySet.add(word)
                        print("Breaking function: {}".format(match))
                        break
                    if keyword not in mySet and keyword != "":
                        mySet.add(keyword)


    keywordsSet = set()
    for dirName, subdirList, fileList in os.walk(input_folder):
        for fileName in fileList:
            if not fileName.endswith(".py") or fileName == "opy.py":
                continue
            filePath = os.path.join(dirName, fileName)
            keywordsSetInThisFile = {fileName.rstrip(".py")}
            with open(filePath) as f:
                print(f"Checking file {filePath}")
                text = f.read()
                import1Result = re.findall(import1, text)
                import2Result = re.findall(import2, text)
                import3Result = re.findall(import3, text)
                import4Result = re.findall(import4, text)
                import5Result = re.findall(import5, text)
                class1Result = re.findall(class1, text)
                function1Result = re.findall(function1, text)
                enums1Result = re.findall(enums1, text)
                enums2Result = re.findall(enums2, text)
                attr1Result = re.findall(attr1, text)
                results = [import1Result, import2Result, import3Result, import4Result, import5Result, class1Result, enums1Result, enums2Result, attr1Result]
                if dirName.endswith("sc2"):
                    sc2_init_variablesResult = re.findall(sc2_init_variables, text)
                    results.append(sc2_init_variablesResult)
                if "_id.py" in filePath or "unit_typeid.py" in filePath:
                    enum_class1Result = re.findall(enum_class1, text)
                    print(results)
                    results.append(enum_class1Result)
                for result in results:
                    if result == import4Result:
                        pass
                    addResult(keywordsSetInThisFile, result)
                for result in [function1Result]:
                    addResult(keywordsSetInThisFile, result, isFunction=True)
            if verbose:
                print("Keywords found in file {}: \n{}".format(filePath, sorted(list(keywordsSetInThisFile))))
            keywordsSet |= keywordsSetInThisFile

    keywordsListSorted = sorted(list(keywordsSet))


    configContent = ""
    with open(config_path) as f:
        configContent = f.read()
    index = configContent.rfind("\'\'\'")
    configContentStart = configContent[:index]
    configContentNew = "\n".join(keywordsListSorted)
    configContentNewComplete = configContentStart + configContentNew + "\n\'\'\'"
    with open(config_output_path, "w+") as f:
        f.write(configContentNewComplete)

    return keywordsSet



if __name__ == "__main__":

    # To be able to copy folders to existing folders, shutil.copytree doesnt work as expected
    from distutils.dir_util import copy_tree

    # Copy the bot files to the temp folder
    copy_tree(inputFolder, tempFolder)

    # Copy python-sc2/sc2 folder to bot subfolder
    temp_sc2_path = os.path.join(tempFolder, "sc2")
    copy_tree(python_sc2_sc2_path, temp_sc2_path)

    # Parse the bot and python-sc2 files for class names, function names and parameters, enums (UnitTypeId, AbilityId etc.), and the python-sc2/sc2 variable names
    configOutput = os.path.join(tempFolder, "opy_config.txt")
    build_obfuscate_config(
        tempFolder,
        configDefaultPath,
        configOutput
    )

    # Copy the opy.py file
    temp_opy_path = os.path.join(tempFolder, "opy.py")
    shutil.copy(opyFilePath, temp_opy_path)
    import time
    time.sleep(0.1)

    # Use opy.py to convert the files to output folder
    args = ["python", temp_opy_path, tempFolder, outputFolder, configOutput]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=inputFolder)
    result = process.communicate()
    if verbose:
        print(result[0])
    time.sleep(0.1)

    # Copy the original python-sc2/sc2 folder to output folder
    output_sc2_path = os.path.join(outputFolder, "sc2")
    copy_tree(python_sc2_sc2_path, output_sc2_path)

    if verbose:
        print("Success.")




