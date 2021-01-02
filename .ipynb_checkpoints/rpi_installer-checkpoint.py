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

    print("Finding hosts...")
    host_data = utils.read_local_host_data(c.LOCAL_HOST_DATA_PATH)
    host_data = utils.resolve_ipv4s(host_data)
    ipv4s = list(map(lambda x: x["ipv4"], host_data))
    assert all(ipv4s), "MissingHostError: Not all hosts have been found"
    print("Hosts found...")

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
