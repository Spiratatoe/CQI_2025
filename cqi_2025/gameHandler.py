from attack import attackMode
from defense import defenseMode
from util import *
import json


json_start_string = '{    "is_offense": true,    "max_moves": 200,    "element_types_color": {        "background": "#FFFFFF",        "wall": "#000000",        "offense_player": "#FF0000",        "goal": "#FFD700",        "large_vision": "#4CBB17",        "timebomb": "#0099CC",        "timebomb_second_round": "#006699",        "timebomb_third_round": "#003366"    }}'

start_dict = json.loads(json_start_string)
is_offense = start_dict["is_offense"]
background = hex_to_rgb(start_dict["element_types_color"]["background"])
wall = hex_to_rgb(start_dict["element_types_color"]["wall"])
offense_player = hex_to_rgb(start_dict["element_types_color"]["offense_player"])
goal = hex_to_rgb(start_dict["element_types_color"]["goal"])
timebomb = hex_to_rgb(start_dict["element_types_color"]["timebomb"])
timebomb_second_round = hex_to_rgb(start_dict["element_types_color"]["timebomb_second_round"])
timebomb_third_round = hex_to_rgb(start_dict["element_types_color"]["timebomb_third_round"])

color_dict = {
    "background": background,
    "wall": wall,
    "offense_player": offense_player,
    "goal": goal,
    "timebomb": timebomb,
    "timebomb_second_round": timebomb_second_round,
    "timebomb_third_round": timebomb_third_round,     
}

if is_offense:
    attackMode(color_dict)
else:
    defenseMode(color_dict)    
    