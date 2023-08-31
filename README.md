# footballdb
football players database
- this is a python app that:
    - allows creation of new players with attributes
    - allows search for existing players
- all player data is stored in player.csv.

## CLI
run CLI app by typing `python cli.py` in directory terminal
modes:
q - quit
n - new player
s - search player
h - help

### new player mode
- ALL ATTRIBUTES MUST NOT CONTAIN SPACES
[card_type] [lastname] [firstname] [team] [spe] [pas] [sho] [tac] [con] [gk] [phy] [hea]

### search mode
[name] (firstname + lastname) #[attribute] [value]

## GUI
run by `python gui.py`
- don't click the red button

# dependencies
- python3.10+
- pandas
- customtkinter
- pillow(PIL fork)
- windows 11
