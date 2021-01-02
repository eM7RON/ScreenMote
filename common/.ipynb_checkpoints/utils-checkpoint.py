#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import hashlib
import io
import multiprocessing
import re
import socket
import subprocess
import time

import gspread
import keyboard
import paramiko

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials

from common import constants as c


def get_google_drive_password_hash():
    """
    Returns the password hash stored on the google drive
    """
    scope = r"https://www.googleapis.com/auth/drive"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        c.DEFAULT_CREDS_PATH, scope
    )
    service = build("drive", "v3", credentials=credentials)
    request = service.files().get_media(fileId=c.GDRIVE_PW_FILE_ID)
    fh = io.BytesIO()
    MediaIoBaseDownload(fd=fh, request=request).next_chunk()
    fh.seek(0)
    return fh.read().decode("utf8")


def isipv4(ipv4):
    if is_regex_match_ipv4(ipv4):
        try:
            socket.inet_aton(ipv4)
            return True
        except:
            pass


def is_regex_match_ipv4(ipv4):
    return bool(
        re.match(
            "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            ipv4,
        )
    )


def is_regex_match_mac(mac):
    return bool(
        re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower())
    )


def open_google_sheet(sheet_name, credentials_path):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return data


def hash_password(password, func="sha256"):
    return getattr(hashlib, func)(password.encode("utf-8")).hexdigest()


def augment_url(url):
    url = url.split("/pub?")
    address, queries = url
    start, loop, delay = queries.split("&")
    queries = "&".join([loop, start, delay])
    url = address + "/pub?" + queries
    return url


def flatten(alist):
    return [item for sublist in alist for item in sublist]


def unzip(nested_iterable):
    return map(list, zip(*(nested_iterable)))


def group(iterable, n):
    range_n = range(n)
    ret = [[] for _ in range_n]
    for i in range(0, len(iterable), n):
        for j in range_n:
            ret[j].append(iterable[i + j])
    return ret


def ipv4_from_mac(mac):
    try:
        ipv4 = ipv4s_from_local_mac_file()
    except:
        n_hosts = enumerate_hosts_from_local_data()
        names = (f"{c.HOST_NAME_TEMPLATE}{str(n).zfill(2)}" for n in range(n_hosts))
        pool = multiprocessing.Pool(n_cpu)
        ipv4s = pool.map(ipv4_from_name, names)
        pool.close()
        pool.join()


def mac_to_ipv4_windows(mac):
    mac = mac.replace(":", "-").lower()
    cmd = f'arp -a | findstr "{mac}" '
    returned_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    time.sleep(1)
    parse = str(returned_output).split(" ", 1)
    ipv4 = parse[1].split(" ")[1]
    return ipv4


def get_ipv4(host):
    try:
        ipv4 = mac_to_ipv4_windows(host["mac"])
    except:
        ipv4 = ipv4_from_name(host["name"])
    return ipv4


def resolve_ipv4s(host_data):
    for host in host_data:
        if not isipv4(host["ipv4"]):
            host["ipv4"] = get_ipv4(host)
    return host_data


def ipv4_from_name(name):
    start_time = time.time()
    search_time = 0
    while search_time < 10:
        try:
            ipv4 = socket.gethostbyname(name)
        except:
            search_time = time.time() - start_time
        else:
            return ipv4


def read_local_host_data(path):
    host_data = []
    with open(c.LOCAL_HOST_DATA_PATH, newline="") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=","))
        for row in reader[1:]:
            host = {
                "name": f"{c.HOST_NAME_TEMPLATE}{str(int(row[0]) - 1).zfill(2)}",
                "mac": row[1],
                "ipv4": row[2],
                "enabled": None,
            }
            host_data.append(host)
    return host_data


def ipv4s_from_local_host_data():
    host_data = read_local_host_data(c.LOCAL_HOST_DATA_PATH)
    host_data = resolve_ipv4s(host_data)
    return list(map(lambda x: x["ipv4"], host_data))


def enumerate_hosts_from_local_data():
    host_data = read_local_host_data(c.LOCAL_HOST_DATA_PATH)
    n_hosts = len(host_data)
    return n_hosts


def establish_connection(host, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=c.USERNAME, password=password)
    return ssh_client


def composite_commands(commands):
    commands = [s.replace("sudo ", "")]
    return "sudo " + "; ".join(commands)


def send_command(ssh_client, host, password, command, sudo_required):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=sudo_required)
    except (Exception, paramiko.ssh_exception.AuthenticationException):
        time.sleep(1)
        ext_status = f"{host} fail"
    else:
        time.sleep(1)
        if sudo_required:
            stdin.write(password + "\n")
        stdin.flush()
        ext_status = f"{host} success"
    finally:
        ssh_client.close()
        return ext_status


def toggle_power(args):
    ipv4, password, command = args
    print(args)
    ssh_client = establish_connection(ipv4, password)
    ext_status = send_command(ssh_client, ipv4, password, command, sudo_required=True)
    return ext_status


def sudo_send_file(ssh_client, ipv4, password, local_path, remote_path):
    stdin, stdout, stderr = ssh_client.exec_command("sudo su")
    time.sleep(0.3)
    try:
        stdin.write(password + "\n")
    except (Exception, paramiko.ssh_exception.AuthenticationException):
        ext_status = f"{ipv4} fail"
    else:
        send_file(ssh_client, ipv4, local_path, remote_path)
        stdin.flush()
        ext_status = f"{ipv4} success"
    finally:
        ssh_client.close()
        return ext_status


def send_file(ssh_client, ipv4, local_path, remote_path):
    ftp_client = ssh_client.open_sftp()
    try:
        ftp_client.put(local_path, remote_path)
    except Exception as e:
        ext_status = f"{ipv4} fail"
    else:
        ext_status = f"{ipv4} success"
    finally:
        ftp_client.close()
        return ext_status


def typed_selection_input(options):
    prompt = " | ".join(options) + "?: "
    prompt = prompt[0].upper() + prompt[1:]
    valid_command = False
    while 1:
        command = input(prompt)
        valid_command = command.lower() in options
        if valid_command:
            break
    flush_input()
    return command


def flush_input():
    try:
        import sys, termios

        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except ImportError:
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()


def is_all_int(input_):
    return all(x.isnumeric() for x in input_.strip().split(" "))


def confirm_input():
    options = {"y": True, "n": False}
    print("Do you want to continue? [Y/n]")
    valid_command = False
    while 1:
        confirmation = keyboard.read_key().lower()
        valid_command = confirmation in options
        if valid_command:
            break
    flush_input()
    print(confirmation)
    confirmation = options[confirmation]
    return confirmation


def key_selection_input(options):
    prompt = []
    idx = range(1, len(options) + 1)
    for n in idx:
        prompt.append(f"{n}) {options[n - 1]}")
    prompt = "\n".join(prompt) + "\n"
    print(prompt, end="")
    idx = set([str(n) for n in idx])
    valid_command = False
    while 1:
        command = keyboard.read_key()
        valid_command = command in idx
        if valid_command:
            break
    flush_input()
    command = options[int(command) - 1]
    print(command)
    return command


def position_next_window(prev_, next_):
    """
    Sets the position of the next_ window to the position of prev_ window
    whilst preserving the geometry of the next_ window
    """
    w = next_.geometry().width()
    h = next_.geometry().height()
    x = round(prev_.geometry().x() + prev_.geometry().width() / 2 - w / 2)
    y = round(prev_.geometry().y() + prev_.geometry().height() / 2 - h / 2)
    next_.setGeometry(x, y, w, h)
