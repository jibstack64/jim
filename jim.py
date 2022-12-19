# a calorie and weight logger (source: https://github.com/jibstack64/jim)
# vvv
# just a little script i made for my personal gymventures, i don't recommend
# using it if you're serious

# import required libraries
from colorama import Fore as Colour
from colorama import Style as Funk
import datetime
import colorama
import json
import sys
import os

UNIX = os.name != "nt"
HELP = """help
  -> prints this help string.
log {calories} [weight (kg)]
  -> associates the current date and time with the calorie count and weight provided.
read
  -> displays all past data in a pretty format.
reset
  -> resets all data."""
INDENT = 4
FP = "~/.jim/database.json" if UNIX else "database.json"

# initialise colorama
colorama.init(convert=not UNIX)

def pretty(text: str, error: bool = False, override: str = None):
    print(((Colour.RED if error else Colour.GREEN) if override == None else override) + text + Colour.RESET)

args = sys.argv[1:]
if len(args) == 0:
    pretty("no arguments provided.", error=True)
else:
    if args[0][0:2].strip("-") + args[0][2:].lower() in ["help", "h", "assistance-please"]:
        print(HELP)
    elif args[0] == "log":
        # everyone loves spaghetti
        if len(args) < 2:
            pretty("too little args for logging, buddy.", error=True)
        elif len(args) > 3:
            pretty("too many args mate.", error=True)
        else:
            calories = None
            weight = None if len(args) > 2 else 0
            try:
                calories = int(args[1])
                if len(args) > 2:
                    weight = int(args[2])
            except:
                # lazy lmao
                pretty(f"{'calories are a' if weight == None else 'weight is a' if calories == None else 'the values required are'} linear, integer value(s), pal.", error=True)
                exit(1)
            if os.path.exists(FP):
                data = json.load(open(FP, "r"))
            else:
                data = []
            data.append({
                "date": datetime.datetime.now().strftime("%m/%d/%Y"),
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "calories": calories,
                "weight": weight
            })
            # WRITE IT (with suitable aggression)
            json.dump(data, open(FP, "w"), indent=INDENT)
            pretty("done.")
    elif args[0] == "read":
        # load it in
        ugh = False
        if os.path.exists(FP):
            data = json.load(open(FP, "r"))
            if data == []:
                ugh = True
        else:
            ugh = True
        if ugh:
            pretty("no data to read :)", error=True)
            exit(1)
        changeitup = {}
        print() # nl
        for d in data.copy():
            if changeitup.get(d["date"]) == None:
                changeitup[d["date"]] = []
            changeitup[d["date"]].append(d)
            changeitup[d["date"]][-1].pop("date")
        for date, logs in changeitup.items():
            pretty(f"-> {date}", False, Colour.LIGHTMAGENTA_EX + Funk.BRIGHT)
            for l in logs:
                pretty(f"  Calories: {l['calories']} - Weight: {l['weight']} - Time: {l['time']}", False, Colour.LIGHTCYAN_EX)
            print() # another nl
    elif args[0] == "reset":
        try:
            data = json.load(open(FP, "r"))
        except:
            pretty("no database to reset :/", True)
            exit(1)
        if len(data) == 0:
            pretty("the database is empty :/", True)
            exit(1)
        json.dump([], open(FP, "w"), indent=INDENT)
        pretty(f"nooO!!! {len(data)} logs gone, you must feel horrible!")
    else:
        pretty(f"{args[0]}?! thats not a valid argument, bro.", error=True)