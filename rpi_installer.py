#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import multiprocessing

import paramiko

from common import constants as c
from common import utils


def install(args):
    ipv4, password = args
    ext_status = []
    ssh_client = utils.establish_connection(ipv4, password)
    status = (
        utils.send_file(ssh_client, ipv4, c.VIEWER_LOCAL_PATH, c.VIEWER_REMOTE_PATH)
        + " viewer.py"
    )
    ext_status.append(status)
    status = (
        utils.send_file(ssh_client, ipv4, c.DEPLOY_LOCAL_PATH, c.DEPLOY_REMOTE_PATH)
        + " deploy.py"
    )
    ext_status.append(status)
    return ext_status


if __name__ == "__main__":

    n_cpu = max(1, multiprocessing.cpu_count() - 1)
    pool = multiprocessing.Pool(n_cpu)

    print(f"STATIC_IPV4S = {c.STATIC_IPV4S}")

    if c.STATIC_IPV4S:
        print("Loading hosts...")
        hosts = utils.read_local_host_data(r"data/hosts.txt")
    else:
        print("Finding hosts...")
        try:
            ipv4s = utils.ipv4s_from_local_mac_file()
        except:
            n_hosts = utils.enumerate_mac_file()
            names = (f"{c.HOST_NAME_TEMPLATE}{str(n).zfill(2)}" for n in range(n_hosts))
            pool = multiprocessing.Pool(n_cpu)
            ipv4s = pool.map(utils.ipv4_from_name, names)
            pool.close()
            pool.join()
        finally:
            assert all(ipv4s), "MissingHostError: Cannot connect to hosts"
            print("Ipv4s found")
    while 1:
        try:
            password = getpass.getpass(f"[sudo] password for {c.USERNAME}: ")
            pool = multiprocessing.Pool(n_cpu)
            status = pool.map(install, ((ipv4, password) for ipv4 in ipv4s))
            pool.close()
            pool.join()
        except paramiko.ssh_exception.AuthenticationException:
            print("Incorrect password. Please try again.")
        else:
            break

    status = list(status)
    status = utils.flatten(status)
    status = sorted(status, key=lambda x: "success" in x, reverse=True)
    print(*status, sep="\n", end="")
