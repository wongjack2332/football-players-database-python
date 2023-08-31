import pandas as pd
import parse
import time
import re

from databaseutils import *


def player_entry(player_dict, card_type, *args):
    keys = list(player_dict.keys())
    index = f"{len(keys)+1:04d}"
    row = [card_type, *args]
    if len(row) != 12:
        print("incorrect amount of attributes")
        return
    if row in list(player_dict.values()):
        print("player already exists")
        return
    player_dict[index] = row


def player_entry_mode():
    message = """Add Player - [type] [lastname] [firstname] [team] [spe] [pas] [sho] [tac] [con] [gk] [phy] [hea]
    
    *** separated by 1 space ***
    
    ':q' to quit entry mode"""
    print(message)
    while True:
        expression = input("Enter player: ")
        if expression.strip() == ":q":
            break
        if expression.strip() == ":s":
            parse.dict_to_csv(players_dict, fields)
            continue
        expression = expression.strip().split()
        for i, v in enumerate(expression):
            expression[i] = int(v) if v.isdigit() else v.lower()
        card_type = "standard" if expression[0] == "x" else expression[0]
        player_entry(players_dict, card_type, *expression[1:])


def player_search_mode():

    while True:
        command = input("enter command: ").strip().lower()
        match command:
            case ":all":
                print(df)
            case ":q":
                print("quit")
                time.sleep(0.5)
                return
            case _:
                command_dict = parse_search_command(command)
                if command_dict == -1:
                    continue
                result = player_search(df, **command_dict)
                print(result)


def get_mode():
    message = "n - entry mode\ns - seach mode\nq - quit"
    while True:
        mode = input("enter mode: ").strip().lower()

        match mode:
            case "s":
                player_search_mode()
            case "n":
                player_entry_mode()
            case "q":
                print("quit")
                break
            case "h":
                print(message)
            case _:
                print("invalid mode")


fields, players_dict = parse.csv_to_dict()
df = pd.DataFrame.from_dict(players_dict, columns=fields[1:], orient="index")
get_mode()
parse.dict_to_csv(players_dict, fields)
