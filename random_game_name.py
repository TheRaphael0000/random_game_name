import json
import random
import tempfile
import requests
import os
import argparse

pos = {}
URL = r"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"


def create_lookuptable():
    temp_dir = tempfile.gettempdir()
    filename = "steam_applist.json"
    path = os.path.join(temp_dir, filename)

    # download the list
    if not os.path.isfile(path):
        request = requests.get(URL)
        games = request.text
        with open(path, "w", encoding="UTF-8") as f:
            f.write(games)
    # use cached list
    else:
        games = open(path, encoding="UTF-8").read()

    js = json.loads(games)
    apps = js["applist"]["apps"]
    games = [i["name"].lower() for i in apps]

    splited_games = [i.split(" ") for i in games]

    for game in splited_games:
        for i, word in enumerate(game):
            word = word.capitalize()
            if i not in pos:
                pos[i] = []
            pos[i].append(word)


create_lookuptable()


def gen(pos, size):
    name = ""
    for i in range(size):
        name += random.choice(pos[i]) + " "
    return name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate random game name")
    parser.add_argument("-n", "--number", type=int, help="generate n")
    parser.add_argument("-s", "--size", type=int, default="4",
                        help="number of words in the random name")

    args = parser.parse_args()

    if args.number is not None:
        for i in range(args.number):
            name = gen(pos, args.size)
            print(name)
    else:
        while True:
            name = gen(pos, args.size)
            print(name, end="")
            input("")
