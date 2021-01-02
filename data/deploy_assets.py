#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script is designed to be placed on raspberry pis 3B/3B+ which have Screenly-OSE installed and 
activated remotely by running the 'update_assets.py' in the scripts directory in a local Python 
environment. The activated script basically updates Screenly's SQL database with assets which have 
been placed in the assets.txt file in the local data directory. Assets in this file should be written
in the format: 
<asset name> <number of slides> <asset URL>
An asset should be the URL of a published Google slides slide show. The slide should have both
"Start slideshow as soon as the player loads" and "Restart the slideshow after the last slide"
enabled.
"""

import datetime
import itertools
import sqlite3
import sys
import time
import uuid


def group(iterable, n):
    range_n = range(n)
    ret = [[] for _ in range_n]
    for i in range(0, len(iterable), n):
        for j in range_n:
            ret[j].append(iterable[i + j])
    return ret


def main():

    delete = sys.argv[1]
    names, assets, display_times = group(sys.argv[2:], 3)

    db = sqlite3.connect(r"/home/pi/.screenly/screenly.db")

    if delete:
        db.execute("DELETE FROM assets")
        db.commit()

    start_time = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    end_time = r"9999-07-17 15:06:15"

    for name, asset, display_time in zip(names, assets, display_times):
        values = (
            uuid.uuid4().hex,
            name,
            asset,
            None,
            start_time,
            end_time,
            display_time,
            "webpage",
            1,
            0,
            0,
            0,
            0,
        )
        db.execute(
            "INSERT INTO assets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values
        )
    db.commit()


if __name__ == "__main__":
    main()
