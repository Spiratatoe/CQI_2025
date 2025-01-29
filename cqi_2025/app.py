import logging
import json
from flask import Flask, request, jsonify
import numpy as np

from util import *

# global variables
counter = 0
op_start = 0
bomb_placed_coord = [0,0]
bomb_counter = 3
last_wall_placed = [0,0]
started = False
did_i_go_up = True
no_of_walls = 0 

json_start_string =""
start_dict = {}
color_dict={}


app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"




@app.route("/start", methods=["POST"])
def start_game():
    global json_start_string
    global start_dict
    global color_dict

    app.logger.info("Start game")
    data = request.json
    app.logger.info(data)
    json_start_string = data
    start_dict = json_start_string
    is_offense = start_dict["is_offense"]
    background = hex_to_rgb(start_dict["element_types_color"]["background"])
    wall = hex_to_rgb(start_dict["element_types_color"]["wall"])
    offense_player = hex_to_rgb(start_dict["element_types_color"]["offense_player"])
    goal = hex_to_rgb(start_dict["element_types_color"]["goal"])
    large_vision = hex_to_rgb(start_dict["element_types_color"]["large_vision"])
    timebomb = hex_to_rgb(start_dict["element_types_color"]["timebomb"])
    timebomb_second_round = hex_to_rgb(start_dict["element_types_color"]["timebomb_second_round"])
    timebomb_third_round = hex_to_rgb(start_dict["element_types_color"]["timebomb_third_round"])
    color_dict = {
    "background": background,
    "wall": wall,
    "offense_player": offense_player,
    "goal": goal,
    "timebomb": timebomb,
    "large_vision": large_vision,
    "timebomb_second_round": timebomb_second_round,
    "timebomb_third_round": timebomb_third_round,
}
    return "", 200




@app.route("/next_move", methods=["POST"])
def next_move():
    data = request.json
    app.logger.info(data)
    # Process the map and determine the next move
    # You can add your logic here
    
    if data.get("is_offense"):
        return jsonify({"move": "left"})  # Example move
    else:
        global counter
        global no_of_walls
        counter += 1

        # call the json_base64_to_nparray()
        map = json_base64_to_nparray(data)

        # run to get coordinate function which returns an x & y of the player
        global color_dict
        # app.logger.info(color_dict['offense_player'])
        atk_color = color_dict['offense_player']
        coords = find_coord(map, atk_color[0], atk_color[1],atk_color[2])

        # check if we can bomb 
        global bomb_placed_coord
        global bomb_counter
        bc_1 = color_dict['timebomb']
        bc_2 = color_dict['timebomb_second_round']
        bc_3 = color_dict['timebomb_third_round']
        app.logger.info("my bounds:")
        app.logger.info(len(map[1]))
        app.logger.info(len(map))
        app.logger.info("my x coord:")
        app.logger.info(bomb_placed_coord[0])
        app.logger.info("my y coord:")
        app.logger.info(bomb_placed_coord[1])
        tile = map[bomb_placed_coord[1]][bomb_placed_coord[0]] # map is inversed 
        is_b1 = color_check(tile, bc_1[0], bc_1[1], bc_1[2])
        is_b2 = color_check(tile, bc_2[0], bc_2[1], bc_2[2])
        is_b3 = color_check(tile, bc_3[0], bc_3[1], bc_3[2])


        # check if bomb in coord
        if( is_b1 or is_b2 or is_b3 ): # no more bomb 
            if(bomb_counter == 0):
                x_max = len(map[1]) 
                y_max = len(map) 
                if(coords[0] + 3 < x_max - 1):
                    x_coord = coords[0] + 3
                    y_coord = coords[1]
                    bomb_placed_coord = [x_coord, y_coord]
                    bomb_counter = 3
                    return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
                elif(coords[0] + 3 < y_max-1):
                    x_coord = coords[0]
                    y_coord = coords[1] + 3
                    bomb_placed_coord = [x_coord, y_coord]
                    bomb_counter = 3
                    return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
                elif(coords[1] - 3 > 0):
                    x_coord = coords[0]
                    y_coord = coords[1] - 3
                    bomb_placed_coord = [x_coord, y_coord]
                    bomb_counter = 3
                    return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
            
        # if we cant bomb place walls 
        bomb_counter -= 1

        # use the three way bait strategy 

        # how many walls left to place 

        # diagonal 
        # find end point 
        goal_col = color_dict['goal']
        end_pt_coord = find_coord(map, goal_col[0], goal_col[1], goal_col[2]) # returns a x,y 
        app.logger.info("my end pt is here coord:")
        app.logger.info(end_pt_coord[0])
        app.logger.info(end_pt_coord[1])
        end_pt_tile = map[end_pt_coord[1]][end_pt_coord[0]] # map is inversed so map[y][x]

        # alternate from diagonal up and down 
        # and check if at border 
        min_y = 0 
        max_y = len(map)
        

        # check last wall placed
        # block them at the last second
        # check to the left 
        # we do bounces of two because we want to block before they get there
        end_pt_tile_left = map[end_pt_coord[1]][end_pt_coord[0] - 2] # x minus two is to the left 
        to_left = color_check(end_pt_tile_left,atk_color[0],atk_color[1],atk_color[2])
        if(not to_left):
            # block
            app.logger.info("we trying to do a left block")
            no_of_walls += 1
            return jsonify({"x": end_pt_coord[0]-1, "y": end_pt_coord[1], "element": "wall"})

        # check up 
        if(end_pt_coord[1] - 2 > -1): # if we not already at the top, if we are bigger than or equal to zero we are good 
            end_pt_tile_up = map[end_pt_coord[1] - 2][end_pt_coord[0] ] # y minus one is the top
            at_top = color_check(end_pt_tile_up,atk_color[0],atk_color[1],atk_color[2])
            if(not at_top):
                # block
                app.logger.info("we trying to do a top block")
                no_of_walls += 1
                return jsonify({"x": end_pt_coord[0], "y": end_pt_coord[1] - 1, "element": "wall"})

        # check down 
        if(end_pt_coord[1] + 2 < max_y ): # if we not already maximum y, y must not be bigger than max y - 1 because index at 0 
            end_pt_tile_down = map[end_pt_coord[1] + 2 ][end_pt_coord[0]] # y plus one is the bot
            at_bot = color_check(end_pt_tile_down,atk_color[0],atk_color[1],atk_color[2])
            if(not at_bot):
                # block
                app.logger.info("we trying to do a bottom block")
                no_of_walls += 1
                return jsonify({"x": end_pt_coord[0], "y": end_pt_coord[1]+1, "element": "wall"})


        # did we reach our max walls 
        # our max is 28 since we need to block to entries 
        # no_of_walls = sum(x.count([0,0,0]) for x in map)
        

        if(no_of_walls > 27):
            return jsonify({"x": 0, "y": 0, "element": "skip"})
        # if y is higher than goal that means we now place a y lower goal 
        # if we dont have to block an entry we do diagonal walls 
        global last_wall_placed # starts at [0,0]
        global started
        global did_i_go_up
        if(started == False):
            if(end_pt_coord[1] - 1 > 0): # don't block the sides 
                last_wall_placed[0] = end_pt_coord[0]-1 # go left in x by 1
                last_wall_placed[1] = end_pt_coord[1]-1 # go up in y by 1
                started = True
                no_of_walls += 1
                return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
            elif(end_pt_coord[1] - 1 > -1): # start one away from the side 
                #it means 
                last_wall_placed[0] = end_pt_coord[0]-1 # go left in x by 1
                last_wall_placed[1] = end_pt_coord[1]-1 # go up in y by 1
                started = True
                no_of_walls += 1
                return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
            else:
                # we started at the top so we cant put any above
                last_wall_placed[0] = end_pt_coord[0] - 1 # go left in x by 1
                last_wall_placed[1] = end_pt_coord[1] + 1 # go down in y by 1
                started = True
                no_of_walls += 1
                return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
        else:
            # no longer first move so we have a history of placed 
            # first check whether we can go up, down or both 

            if(last_wall_placed[1] > end_pt_coord[1]): # if we went downwards in y last turn go up this turn, we go up in x 
                # check if we can do an up move
                # since we always start with an up move, doing a new one means decrease in x 
                difference_in_x = end_pt_coord[0] - last_wall_placed[0] + 1# we add 1 because new layer

                new_x = end_pt_coord[0] - difference_in_x # new layer in x
                if(new_x == 0):
                    return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "skip"})
                new_y = end_pt_coord[1] - difference_in_x # new layer of y 
                if(new_y - 1 > 0): # is there still at least a one gap, we can place
                    last_wall_placed[0] = new_x # go left in x by 1
                    last_wall_placed[1] = new_y # go up in y by 1
                    no_of_walls += 1
                    return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
                else:
                    # we can't place anymore up so continue down
                    new_y = end_pt_coord[1] + difference_in_x # new layer of y but downwards and x is already changed
                    if(new_y < max_y - 1):
                        last_wall_placed[0] = new_x # go left in x by 1
                        last_wall_placed[1] = new_y # go up in y by 1
                        no_of_walls += 1
                        return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
            else:
                # else if we didnt go down in y, go down in y 
                difference_in_x = end_pt_coord[0] - last_wall_placed[0] # we dont add 1 because we need to go down first
                new_x = end_pt_coord[0] - difference_in_x # new layer in x
                if(new_x == 0):
                    return jsonify({"x": 0, "y": 0, "element": "skip"})
                new_y = end_pt_coord[1] + difference_in_x # new layer of y but downwards
                if(new_y < max_y -1 ):
                    last_wall_placed[0] = new_x # go left in x by 1
                    last_wall_placed[1] = new_y # go up in y by 1
                    no_of_walls += 1
                    return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})
                else:
                    #we cant go any lower move upwards
                    difference_in_x = end_pt_coord[0] - last_wall_placed[0] + 1 # we need to add 1 now
                    new_x = end_pt_coord[0] - difference_in_x # new layer in x
                    if(new_x == 0):
                        return jsonify({"x": 0, "y": 0, "element": "skip"})
                    new_y = end_pt_coord[1] - difference_in_x # new layer of y but upwards
                    if(new_y - 1 > 0): # is there still at least a one gap, we can place
                        last_wall_placed[0] = new_x # go left in x by 1
                        last_wall_placed[1] = new_y # go up in y by 1
                        no_of_walls += 1
                        return jsonify({"x": last_wall_placed[0], "y": last_wall_placed[1], "element": "wall"})


            #dont forget to save 2 walls for blocking entry
        return jsonify({"x": 0, "y": 0, "element": "skip"})




        

        # # Bombing
        # # write  to bomb only after all walls placed for now
        # if(counter < 30):
        #     # take the list x : [0] while y : [1]
        #     # first logic is to place walls in front of player so x + 1
        #     x_coord = coords[0] + 1
        #     # where y is that of the attackers 
        #     y_coord = coords[1]
        #     return jsonify({"x": x_coord, "y": y_coord, "element": "wall"})  # Example defense action

        # else: # quick bombing logic 
        #     x_max = len(map)
        #     y_max = len(map[1])
        #     if(coords[0] + 3 < x_max):
        #         x_coord = coords[0] + 3
        #         y_coord = coords[1]
        #         return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
        #     elif(coords[1] + 3 < y_max):
        #         x_coord = coords[0]
        #         y_coord = coords[1] + 3
        #         return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
        #     elif(coords[1] - 3 > 0):
        #         x_coord = coords[0]
        #         y_coord = coords[1] - 3
        #         return jsonify({"x": x_coord, "y": y_coord, "element": "timebomb"})
            

            





@app.route("/end_game", methods=["POST"])
def end_game():
    # Shut down the bot
    # You can add your logic here
    return "", 200



if __name__ == "__main__":
    print("test build")
    app.run(host="0.0.0.0", port=5000)