#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import getpass
import multiprocessing
import sqlite3
import sys
import time
import uuid

import paramiko

from common import constants as c
from common import utils


def update_assets(arg):
    ipv4, password, names, assets, slide_times, delete = arg
    ssh_client = utils.establish_connection(ipv4, password)
    command = construct_command(names, assets, slide_times, delete)
    ext_status = utils.send_command(
        ssh_client, ipv4, password, command, sudo_required=False
    )
    return ext_status


def construct_command(names, assets, times, delete):
    args = " ".join(" ".join(tup) for tup in zip(names, assets, times))
    command = f"python3 /home/pi/deploy_assets.py {delete} {args}"
    return command


def is_asset(asset):
    return asset.startswith("https://docs.google.com/presentation/")


def augment_asset(asset):
    asset = asset.split("/pub?")
    address, queries = asset
    start, loop, delay = queries.split("&")
    queries = "&".join([loop, start, delay])
    asset = address + "/pub?" + queries
    return asset


if __name__ == "__main__":

    print("############################")
    print("#   OKR-PI Asset Updater   #")
    print("############################")
    print("Ctrl + c to exit at any time.")

    while 1:
        print("Do you want to keep the current assets?")
        delete = utils.key_selection_input(["keep", "delete", "exit"])
        confirmation = utils.confirm_input()
        if confirmation:
            break

    if delete == "exit":
        sys.exit()
    else:
        delete = {"keep": True, "delete": False}[delete]

    while 1:
        print("Do you want to paste in new assets or load from assets.txt?")
        command = utils.key_selection_input(["paste", "load", "exit"])
        confirmation = utils.confirm_input()
        if confirmation:
            break

    if command == "exit":
        sys.exit()
    elif command == "load":
        with open(c.LOCAL_ASSET_DATA_PATH, "r") as f:
            assets = f.read().split("\n")
        if not isinstance(assets, list):
            assets = list(assets)
        names, n_slides, assets = utils.unzip((asset.split(" ") for asset in assets))
    else:
        names, assets, n_slides = [], [], []
        while 1:
            while 1:
                asset = input("Add an asset:\n")
                if is_asset(asset):
                    break
                else:
                    print("This is an invalid asset")
            assets.append(asset)
            while 1:
                name = input("Give your asset a name:\n")
                confirmation = utils.confirm_input()
                if confirmation:
                    break
            names.append(name)
            while 1:
                n_slide = input("How many slides?\n")
                if n_slide.isnumeric():
                    n_slide = n_slide
                    confirmation = utils.confirm_input()
                    if confirmation:
                        break
                print("Invalid number")
            n_slides.append(n_slide)
            print("Have all assets been added?")
            confirmation = utils.confirm_input()
            if confirmation:
                break
    if not isinstance(assets, list):
        assets = [assets]
    assets = list(set(assets))
    slide_times = []
    for i in range(len(assets)):
        sec_per_slide = round(float(assets[i].split("delayms=")[1]) / 1000)
        slide_times.append(str(int(sec_per_slide * int(n_slides[i]))))

    assets = [f'"{asset}"' for asset in assets]

    if len(assets) == 1:
        names.append(names[0] + "_copy")
        assets.append(augment_asset(list(assets)[0]))
        slide_times.append(slide_times[0])

    n_cpu = max(1, multiprocessing.cpu_count() - 1)

    pool = multiprocessing.Pool(n_cpu)

    print("Finding hosts...")
    host_data = utils.read_local_host_data(c.LOCAL_HOST_DATA_PATH)
    host_data = utils.resolve_ipv4s(host_data)
    ipv4s = list(map(lambda x: x["ipv4"], host_data))
    assert all(ipv4s), "MissingHostError: Not all hosts have been found"
    print("Hosts found...")

    host_range = set(range(utils.enumerate_hosts_from_local_data()))

    while 1:
        screen_numbers = input('Which screens? (numbers or "all" accepted)\n')
        screen_number = screen_numbers.strip()
        valid_input = screen_numbers == "all" or utils.is_all_int(screen_numbers)
        if valid_input:
            if screen_numbers == "all":
                screen_numbers = host_range
                break
            else:
                screen_numbers = set(int(n) for n in screen_numbers.split(" "))
                if all(True if n in host_range else False for n in screen_numbers):
                    break
                else:
                    print("Numbers do not correspond to screens")
        else:
            print("Input not understood")

    ipv4s = [
        host["ipv4"] for host in host_data if int(host["name"][-2:]) in screen_numbers
    ]

    while 1:
        try:
            password = getpass.getpass(f"[sudo] password for {c.USERNAME}: ")
            pool = multiprocessing.Pool(n_cpu)
            status = pool.map(
                update_assets,
                (
                    (ipv4, password, names, assets, slide_times, delete)
                    for ipv4 in ipv4s
                ),
            )
            pool.close()
            pool.join()
        except paramiko.ssh_exception.AuthenticationException:
            print("Incorrect password. Please try again.")
        else:
            break

    status = sorted(status, key=lambda x: "success" in x, reverse=True)
    print(*status, sep="\n", end="")
