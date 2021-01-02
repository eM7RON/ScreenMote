#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import multiprocessing
import sys
import time

import paramiko

from common import constants as c
from common import utils


if __name__ == "__main__":

    print("###########################")
    print("# OKR-PI Power Management #")
    print("###########################")
    print("Ctrl + c to exit at any time.")

    while 1:
        command = utils.key_selection_input(["reboot", "shutdown", "exit"])
        confirmation = utils.confirm_input()
        if confirmation:
            break

    if command == "exit":
        sys.exit()
    command = "sudo " + command + " now"

    n_cpu = max(1, multiprocessing.cpu_count() - 1)

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
                utils.toggle_power, ((ipv4, password, command) for ipv4 in ipv4s)
            )
            pool.close()
            pool.join()
        except (ValueError, paramiko.ssh_exception.AuthenticationException):
            print("Incorrect password. Please try again.")
        else:
            break

    status = sorted(status, key=lambda x: "success" in x, reverse=True)
    print(*status, sep="\n", end="")
