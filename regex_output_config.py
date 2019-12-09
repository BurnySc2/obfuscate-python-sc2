import re
import os
from pathlib import Path
from typing import List, Set


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start() : mo.end()]], text)


def find_stuff(file_contents, only_imports: bool = False) -> Set[str]:

    finds: Set[str] = set()
    # Split the following result by spaces, remove commas, to find keywords
    # Remove paranthesis: ()
    """
    from sc2.data import race_gas, race_worker, race_townhalls, ActionResult, Attribute, Race, Difficulty
    """
    imports_pattern1 = "from [\w.]+ import [\w, ]+"
    import1 = re.compile(imports_pattern1)
    for result in import1.findall(file_contents):
        result_split = multiple_replace({",":"", ".":" "}, result)
        finds |= set(result_split.split())

    """
    import sc2 as sc
    import networkx as nx, matplotlib as plt
    """
    imports_pattern2 = "import [\w. ]+ as [\w.]+"
    import2 = re.compile(imports_pattern2)
    for result in import2.findall(file_contents):
        result_split = multiple_replace({",":"", ".":" "}, result)
        finds |= set(result_split.split())

    """
    import random, json, time, math, copy
    """
    imports_pattern3 = "import [\w,. ]+"
    import3 = re.compile(imports_pattern3)
    for result in import3.findall(file_contents):
        result_split = multiple_replace({",":"", ".":" "}, result)
        finds |= set(result_split.split())

    """
    from s2clientprotocol import (
        sc2api_pb2 as sc_pb,
        raw_pb2 as raw_pb,
        data_pb2 as data_pb,
        common_pb2 as common_pb,
        error_pb2 as error_pb
    )
    """
    imports_pattern4 = "[a-z0-9_]+ as [a-z0-9_]+"
    import4 = re.compile(imports_pattern4)
    for result in import4.findall(file_contents):
        result_split = multiple_replace({",":"", ".":" "}, result)
        finds |= set(result_split.split())

    imports_pattern5 = "from \w+ import \("
    import5 = re.compile(imports_pattern5)
    for result in import5.findall(file_contents):
        # Replace paranthesis and comma with emptystring
        result = multiple_replace({"(": "", ")": "", ",": ""}, result)
        finds |= set(result.split())

    if not only_imports:
        # For classes: first result is 'class', second is classname, third is a comma seperated list of inherited classes (remove paranethesis first)
        """
        class GroupsManager:
        class GroupsManager(object):
        class DragonBot(burny_basic_ai.BurnyBasicAI):
        class BurnyBasicAI(General, Frequentactions, Position, Conditions, sc2.BotAI):
        """
        class_pattern = "(class) ([\w]+)(\([\w,.\[\]\s]*\))*:"
        class1 = re.compile(class_pattern)
        for result in class1.findall(file_contents):
            for group in result:
                # Replace paranthesis and comma with emptystring
                group = multiple_replace({"(": "", ")": "", ",": "", ".": " "}, group)
                finds |= set(group.split())

        # Adds default parameters, function names, parameter names
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
        def debug_box2_out(
            self,
            pos: Union[Unit, Point2, Point3],
            half_vertex_length: float = 0.25,
            color: Union[tuple, list, Point3] = None,
        ): # random comment
        def towards_with_random_angle(
            self,
            p: Union[Point2, Point3],
            distance: Union[int, float] = 1,
            max_difference: Union[int, float] = (math.pi / 4),
        ) -> Point2:
        def step_time(self) -> Tuple[float, float, float, float]:
        """
        # function_pattern = '((async )?def [\w]+\(([\s\w\.,:\[\]=\"\*]*)+\))'
        # function_pattern = '((async )?def (.|\s)+?:\s)'
        function_pattern = '((async )?def [\w]+\((.|\s)*?\)( -> )?[\w\[\], \"]*:\s)'
        # function_pattern = '((async )?def [\w]+\((.|\s)*?\):\s)'
        function1 = re.compile(function_pattern)
        for result in function1.findall(file_contents):
            result = result[0]
            # Replace paranthesis and comma with emptystring
            result = multiple_replace({"(": " ", ")": " ", ",": "", "=": " ", ":": ""}, result)
            finds |= set(x for x in result.split() if "[" not in x and "]" not in x and '"' not in x)

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
        enum_class_pattern = "(?:\s+[\w]+ = \d+)"
        enum_class1 = re.compile(enum_class_pattern)
        for result in enum_class1.findall(file_contents):
            finds |= set(x for x in result.split() if x not in {"="})

        # hasattr, getattr, setattr strings
        """
        if not hasattr(self, "opponent_id"):
        if not hasattr(self, "distance_calculation_method"):
        if not hasattr(self, "currentBuildOrder"):
        if not getattr(self, "currentBuildOrder"):
        if not setattr(self, "currentBuildOrder"):
        """
        has_attr_pattern = '(?:not )?(\w{1,3}attr)\((?:[\.\w]+),\s?"?([\w\[\]\(\)]+)"?\)'
        has_attr1 = re.compile(has_attr_pattern)
        for result in has_attr1.findall(file_contents):
            for string in result:
                result_split = multiple_replace({"(": "", ")": "", ",": "", ".": " "}, string)
                finds |= {result_split}

        # Instance variables
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
        class_variables_pattern = '(?:(?:[ \t]*)self.(\w+)(?:[ \w=:\[\]"*,]*)?=)'
        class_variables = re.compile(class_variables_pattern)
        for result in class_variables.findall(file_contents):
            # for string in result:
            result = multiple_replace({"self.": "", "\t": "", " ": "", "=": ""}, result)
            finds |= {result}
        #
        # # all_enums = ["UnitTypeId", "UpgradeId", "AbilityId", "BuffId", "EffectId", "PlayerType", "Difficulty", "Status", "Result", "Alert", "ChatChannel", "Race", "DisplayType", "Alliance", "CloakState", "Attribute", "TargetType", "Target", "ActionResult", "CreateGameError", "Weapon", "ActionChat", "ResponseCreateGame"]
        # # additional_methods = ["parent", "path", "logging", "argparse", "parser", "args", "aiohttp"]
        # # TODO: Stuff that doesnt get picked up

    print(finds)
    return finds


if __name__ == "__main__":
    path = Path(__file__)
    directory = path.parent
    # example_file = directory / "regex_example.py"
    # example_folder = directory / "regex_example"
    bot_folder = directory / "mybot"
    sc2_lib_folder = directory / "sc2"

    found_so_far: Set[str] = set()

    # Search bot for imports
    for dir_name, sub_dir_list, file_list in os.walk(bot_folder):
        for file_name in file_list:
            if not file_name.endswith(".py") or file_name == "opy.py":
                continue
            print(file_name)
            file_path = Path(dir_name) / file_name
            print(file_path, dir_name, file_name)
            # Add filename
            found_so_far.add(os.path.splitext(file_name)[0])
            with open(file_path) as f:
                contents = f.read()
                find_set: Set[str] = find_stuff(contents, only_imports=True)
                found_so_far |= find_set

    # print(found_so_far)
    # with open("output.txt", "w+") as f:
    #     print(sorted(found_so_far))
    #     f.write("\n".join(sorted(found_so_far)))


    # Search sc2 library and find all imports, class names, class variables
    for dir_name, sub_dir_list, file_list in os.walk(sc2_lib_folder):
        for file_name in file_list:
            if not file_name.endswith(".py") or file_name == "opy.py":
                continue
            file_path = Path(dir_name) / file_name
            print(file_path, dir_name, file_name)
            # Add filename
            found_so_far.add(os.path.splitext(file_name)[0])
            with open(file_path) as f:
                contents = f.read()
                find_set: Set[str] = find_stuff(contents)
                found_so_far |= find_set

    other: Set[str] = {"cast_range", "Zerg", "Terran", "Random", "Protoss"}
    found_so_far |= other

    keywords_list_sorted: List[str] = sorted(found_so_far)


    os.makedirs(directory / "tempFolder", exist_ok=True)

    config_path = directory / "opy_config_default.txt"
    config_output_path = directory / "tempFolder" / "opy_config.txt"
    # Load default config
    with open(config_path) as f:
        configContent = f.read()
    # Find where to insert the keywords
    index = configContent.rfind("\'\'\'")
    configContentStart = configContent[:index]
    configContentNew = "\n".join(keywords_list_sorted)
    configContentNewComplete = configContentStart + configContentNew + "\n\'\'\'"
    # Write output config file
    with open(config_output_path, "w+") as f:
        f.write(configContentNewComplete)

    # with open("output.txt", "w+") as f:
    #     print(sorted(found_so_far))
    #     f.write("\n".join(sorted(found_so_far)))

