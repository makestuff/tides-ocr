#!/usr/bin/python3

# Output tidal information for Tuesday nights

import datetime
import json
import sys
from pathlib import Path
from month_util import *

# Parse the timestamps in the JSON file
def from_str(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%MZ").replace(tzinfo=datetime.timezone.utc)

# Render in local-time (i.e UTC in winter, BST in summer)
def get_time(dt, dst):
    if dst:
        hour = 1 + dt.hour
        hour = hour if hour < 24 else 0
        return f"{hour:02d}{dt.minute:02d}*"
    else:
        return f"{dt.hour:02d}{dt.minute:02d}"

# Get the name of the previous month
def prev_month(month):
    month = 12 if month == 1 else month - 1
    return MONTHS[month]

# Output the info for one Tuesday
def render(year, month, day, dest, week, summary, file):
    last_week = DAYS[month] - day < 7
    if summary:
        day = get_ord(day)
        pad = " " if len(day) == 3 else ""
        if week == 1:
            print(f"[b]{MONTHS[month]} {year}:[/b]")
        print(f"    {pad}{day}: {dest}")
        if last_week:
            print()
    else:
        if week == 1:
            print(f'<newsletter name="{MONTHS[month]} {year}" prev="1234">', file=file)
            print(f'    <section name="Club News" anchor="club-news">', file=file)
            print(f'        <section name="Celebrating achievements" anchor="achievements">', file=file)
            print(f'            <text>', file=file)
            print(f'                [list]', file=file)
            print(f'                    [*] Blah.', file=file)
            print(f'                [/list]', file=file)
            print(f'            </text>', file=file)
            print(f'        </section>', file=file)
            print(f'    </section>', file=file)
            print(f'    <section name="Upcoming Events" anchor="upcoming-events">', file=file)
            print(f'        <section name="Blah" anchor="blah">', file=file)
            print(f'            <text>', file=file)
            print(f'                Blah.', file=file)
            print(f'            </text>', file=file)
            print(f'        </section>', file=file)
            print(f'    </section>', file=file)
            print(f'    <section name="{MONTHS[month]} Club Sessions" anchor="club-sessions">', file=file)
            print(f'        <text>', file=file)
            print(f'            [b]Please[/b] volunteer to be Duty Officer for the days marked "[color=red][b]???[/b][/color]" below. Sign up [url=https://towerhamletscanoeclub.co.uk/forum/viewtopic.php?f=44&amp;t=5639]here[/url] ([color=red][b]FIXME![/b][/color]). If it\'s your first time, you will get support from a more experienced person.', file=file)
            print(f'        </text>', file=file)

        print(f'        <section name="{MONTHS[month][:3]} {get_ord(day)}" anchor="club-{day}">', file=file)
        print(f'            <text>', file=file)
        print(f'                [list]', file=file)
        print(f'                    [*] Discover: [color=red][b]???[/b][/color], Explore: [color=red][b]???[/b][/color], Duty Officer: [color=red][b]???[/b][/color].', file=file)
        if week == 2:
            print(f'                    [*] {MONTHS[month]} BBQ, hosted by [color=red][b]???[/b][/color] and [color=red][b]???[/b][/color]!', file=file)

        print(f'                    [*] {dest}', file=file)
        print(f'                [/list]', file=file)
        if last_week:
            print(file=file)
            print(file=file)
            print(f'                * These times are in BST.', file=file)
        print(f'            </text>', file=file)
        print(f'        </section>', file=file)
        if last_week:
            print(f'    </section>', file=file)
            print(f'    <section name="{prev_month(month)} Events" anchor="last-month">', file=file)
            print(f'        <section name="{prev_month(month)[:3]} 1st: Blah" anchor="blah">', file=file)
            print(f'            <text>', file=file)
            print(f'                Blah.', file=file)
            print(f'            </text>', file=file)
            print(f'        </section>', file=file)
            print(f'    </section>', file=file)
            print(f'</newsletter>', file=file)

# Output info for all Tuesday club nights
def print_tuesdays(london_bridge, year, month, mode, file):
    if mode == "s":
        summary = True
    elif mode == "d":
        summary = False
    else:
        usage(sys.argv[0])
    i = 0
    dt, dst, id, h = london_bridge[0]
    this_month = dt.month
    this_week = 1
    while True:
        while dt.weekday() != 1:
            i = i + 1
            if i == len(london_bridge):
                return
            dt, dst, id, h = london_bridge[i]
        delta = 19 if dst else 20
        dt_only = dt.date()
        ret_time = datetime.datetime.combine(dt_only, datetime.time(delta), tzinfo=datetime.timezone.utc)
        while dt < ret_time:
            old_dt = dt
            old_id = id
            old_h = h
            i = i + 1
            if i == len(london_bridge):
                return
            dt, dst, id, h = london_bridge[i]
        dest = "Greenwich" if old_id == "LW" else "Westminster"
        if dt_only.month != this_month:
            this_month = dt_only.month
            this_week = 1
        if month == 0 or dt_only.month == month:
            render(
                year, dt_only.month, dt_only.day,
                f"{old_id} {get_time(old_dt, dst)}({old_h}m), {id} {get_time(dt, dst)}({h}m): {dest}",
                this_week,
                summary,
                file
            )
        this_week = this_week + 1
        while dt.weekday() == 1:
            i = i + 1
            if i == len(london_bridge):
                return
            dt, dst, id, h = london_bridge[i]

# Read tide times from JSON file for London Bridge (see https://github.com/makestuff/tides-ocr)
def get_tides(file_name):
    with open(file_name) as f:
        all = json.load(f)
    year = all["year"]
    data = all["data"][6]
    loc = data["location"]
    tides = data["tides"]
    return [(from_str(i["ts"]), i["dst"], i["id"], i["h"]) for i in tides], year, loc

# Print usage info and quit
def usage(n):
    print(f"Synopsis: {n} <json-file> <s|d> [<month>]")
    sys.exit(1)

# Call with file-name and s|d representing summary|detail. E.g ./tides.py 2022.json d
# The 2022.json file was generated by https://github.com/makestuff/tides-ocr:
# pdf2json.py 2022 1-3 0-6 48  # use 2022 PDF, all phases, extract data, 48 pages
#
if len(sys.argv) == 4:
    month = int(sys.argv[3])
elif len(sys.argv) == 3:
    month = 0
else:
    usage(sys.argv[0])
london_bridge, year, _ = get_tides(sys.argv[1])
mode = sys.argv[2]
if month and mode=="d":
    xml_file = f"{year}{month:02}.xml"
    if Path(xml_file).is_file():
        print(f"Output file {xml_file} already exists!")
        sys.exit(1)
    with open(xml_file, "w") as f:
        print_tuesdays(london_bridge, year, month, mode, f)
    print(f"Template XML written to {xml_file}")
else:
    print_tuesdays(london_bridge, year, month, mode, sys.stdout)
