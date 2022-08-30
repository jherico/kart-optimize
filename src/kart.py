# python3

import json
import logging
import sys
import time
import os

logging.basicConfig(format="%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def gen_combos():
    jsonchardata = open("public/mk8dxchars.json")
    jsonbodydata = open("public/mk8dxbodies.json")
    jsontiredata = open("public/mk8dxtires.json")
    jsonwingdata = open("public/mk8dxgliders.json")
    chardata = json.loads(jsonchardata.read())
    bodydata = json.loads(jsonbodydata.read())
    tiredata = json.loads(jsontiredata.read())
    wingdata = json.loads(jsonwingdata.read())
    legalstats = {'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'}
    combinations = []
    if sys.argv.count("-verbose") != 0:
        for char in chardata:
            for body in bodydata:
                for tire in tiredata:
                    for wing in wingdata:
                        x = {'A': char["A"] + ", " + body["A"] + ", " + tire["A"] + ", " + wing["A"], 'B': 0,
                             'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0}
                        for stat in legalstats:
                            x[stat] = float(
                                char[stat]) + float(body[stat]) + float(tire[stat]) + float(wing[stat])
                        print(x["A"])
                        combinations.append(x)
    else:
        for char in chardata:
            for body in bodydata:
                for tire in tiredata:
                    for wing in wingdata:
                        x = {'A': char["A"] + ", " + body["A"] + ", " + tire["A"] + ", " + wing["A"], 'B': 0,
                             'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0}
                        for stat in legalstats:
                            x[stat] = float(
                                char[stat]) + float(body[stat]) + float(tire[stat]) + float(wing[stat])
                        combinations.append(x)
    logging.info(f"Finished generating {len(combinations)} combinations")
    #print("Finished generating " + str(len(combinations)) + " combinations")
    return combinations

COMBOS_PATH = "public/combos.json"
COMBOS_DATA = {}

if not os.path.isfile(COMBOS_PATH):
    COMBOS_DATA = gen_combos()
    with open(COMBOS_PATH, "w") as text_file:
        text_file.write(json.dumps(COMBOS_DATA))
else:
    with open(COMBOS_PATH, "r") as text_file:
        COMBOS_DATA = json.loads(text_file.read())


def pareto_optimize(combinations, wantedstats):
    frontier = []
    start = time.time_ns()
    if sys.argv.count("-verbose") != 0:
        for x in combinations:
            fail = False
            for y in combinations:
                ydominates = True
                xdominates = True
                for requirement in wantedstats:
                    print(x["A"] + "'s " + requirement +
                          " stat is " + str(x[requirement]))
                    print(y["A"] + "'s " + requirement +
                          " stat is " + str(y[requirement]))
                    if x[requirement] > y[requirement]:
                        ydominates = False
                        print(x["A"] + " is not dominated by " + y["A"] + " because " +
                              x["A"] + " has a higher " + requirement + " stat.")
                    if x[requirement] < y[requirement]:
                        xdominates = False
                        print(y["A"] + " is not dominated by " + x["A"] + " because " +
                              y["A"] + " has a higher " + requirement + " stat.")
                if ydominates and not xdominates:
                    fail = True
                    break
            if not fail:
                print(x["A"] + " is on the Pareto Frontier.")
                frontier.append(x)
    else:
        i = 0
        for x in combinations:
            if i % 100 == 0:
                logging.info(f"Checking {i} {x['A']}")
            i += 1
            fail = False
            for y in combinations:
                ydominates = True
                xdominates = True
                for requirement in wantedstats:
                    if x[requirement] > y[requirement]:
                        ydominates = False
                        break
                    if x[requirement] < y[requirement]:
                        xdominates = False
                if ydominates and not xdominates:
                    fail = True
                    break
            if not fail:
                frontier.append(x)
    tasktime = time.time_ns() - start
    logging.info(f"{tasktime / (1000 * 1000)}")
    return frontier


# print('Stats: B Land Speed C Anti-G Speed D Water Speed E Gliding Speed F Accel')
# print('G Weight H Land Handling I Anti-G Handling J Water Handling K Gliding Handling')
# print('L Traction M M-turbo')
# print('Type the letter of every stat you want to optimize (seperated by commas), then press Enter.')


if __name__ == "__main__":
    print("Hello!")
    result = pareto_optimize(COMBOS_DATA, ["B"])
    #logging.info(f"{json.dumps(result, indent=2)}")
