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
if UNIX:
    os.chdir(os.path.expanduser("~/.jim"))
HELP = """help
  -> prints this help string.
log {calories} [weight (kg)]
  -> associates the current date and time with the calorie count and weight provided.
read
  -> displays all past data in a pretty format.
reset
  -> resets all data."""
INDENT = 4
FP = "database.json"

# initialise colorama
colorama.init(convert=not UNIX)

def pretty(text: str, error: bool = False, override: str = None):
    print(((Colour.RED if error else Colour.GREEN) if override == None else override) + text + Colour.RESET)

def arg_check(min: int, max: int):
    if len(args) < min + 1:
        pretty("too little args, buddy.", error=True)
        exit(1)
    elif len(args) > max + 1:
        pretty("too many args mate.", error=True)
        exit(1)

def parse_types(num: int, halt: int, ty: type) -> tuple:
    vals = []
    x = 0
    for a in args[1:]:
        if x == num:
            break
        try:
            vals.append(ty(a))
        except:
            if x == halt:
                vals.append(None)
                break
            c = "'"
            pretty(f"all arguments must be {str(ty).split(c)[1]} values, pal!", error=True)
            exit(1)
        x += 1
    for x in range(num-len(vals)):
        vals.append(None)
    return tuple(vals)

args = sys.argv[1:]
if len(args) == 0:
    pretty("no arguments provided.", error=True)
else:
    if args[0][0:2].strip("-") + args[0][2:].lower() in ["help", "h", "assistance-please"]:
        print(HELP)
    elif args[0] == "log":
        arg_check(1, 2)
        # everyone loves spaghetti
        calories, weight = parse_types(2, 2, int)
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
        ugh = False # excellent variable names!!!!
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
        cals_total = 0
        cals_num = 0
        wts_last = 0
        wts_first = 0
        for d in data.copy():
            if changeitup.get(d["date"]) == None:
                changeitup[d["date"]] = []
            wts_last = d["weight"] if d["weight"] > 0 else 0
            if data[0] == d:
                wts_first = d["weight"]
            if wts_first == 0 and d["weight"] > 0:
                wts_first = d["weight"]
            cals_num += 1
            cals_total += d["calories"]
            changeitup[d["date"]].append(d)
            cals_total
            changeitup[d["date"]][-1].pop("date")
        for date, logs in changeitup.items():
            pretty(f"-> {date}", False, Colour.LIGHTMAGENTA_EX + Funk.BRIGHT)
            for l in logs:
                pretty(f"  Calories: {l['calories']} - Weight: {l['weight']} - Time: {l['time']}", False, Colour.LIGHTCYAN_EX)
            print() # another nl
        pretty("Average calorie intake:", False, Colour.CYAN)
        pretty(f" ---===+ {round(cals_total/cals_num)} +===---")
        neg = wts_first-wts_last < 0
        pretty(f"You have {'lost' if not neg else 'gained'}:", False, Colour.CYAN)
        pretty(f" {' ' if neg else ''}-=+ {(wts_first-wts_last)*(-1 if neg else 1)}kg +=-")
        print() # another?!
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
    elif args[0] == "remove":
        arg_check(1, 2)
        date, time = parse_types(2, 2, str)
        if not os.path.exists(FP):
            pretty("cannot find database to remove from!!!", True)
            exit(1)
        else:
            data = json.load(open(FP, "r"))
        p = 0
        found = False
        for d in data.copy():
            if d["date"] == date:
                if time == None:
                    data.pop(p)
                    p -= 1
                    found = True
                elif d["time"] == time:
                    data.pop(p)
                    found = True
                    break
            p += 1
        if not found:
            pretty("couldn't find the log with that date and time, soz!", True)
            exit(1)
        else:
            json.dump(data, open(FP, "w"))
            pretty("successfully removed the log.")
    else:
        pretty(f"{args[0]}?! thats not a valid argument, bro.", error=True)
