import glob
import os
import platform
import shutil
import subprocess
import sys
import tarfile

import googleapiclient

from common import constants as c
from common import utils


if __name__ == "__main__":

    if len(sys.argv) > 2:
        print("incorrect number of argumnets")
        sys.exit()
    if "--compress" in sys.argv:
        compress = True
    else:
        compress = False

    builds_directory = "builds"

    dependency_origin = os.path.abspath(googleapiclient.__file__)
    dependency_origin = dependency_origin.split("googleapiclient")[0]
    dependency_origin = glob.glob(
        os.path.join(dependency_origin, "google_api_python_client-*.dist-info")
    )[0]

    dist_dir = "ScreenMote" + platform.system()[:3] + platform.architecture()[0][:-3]
    dependency_destination = os.path.join(
        dist_dir, os.path.split(dependency_origin)[-1]
    )
    dist_path = os.path.join(builds_directory, dist_dir)

    # delete old build directories
    for x in ["build", "dist", "main", dist_dir, dist_path]:
        try:
            shutil.rmtree(x)
        except FileNotFoundError:
            print(f"no previous versions of {x} found")

    # run pyinstaller to construct the .exe

    if platform.system() == "Linux":
        python_version = "python3"
    else:
        python_version = "python"
    subprocess.call(
        f'{python_version} -m PyInstaller -w --icon="{c.ICON_ICO_PATH}" main.py',
        shell=True,
        stderr=subprocess.STDOUT,
    )

    # tidy up
    shutil.move(os.path.join("dist", "main"), os.getcwd())
    os.rename("main", dist_dir)
    for x in ["build", "dist"]:
        try:
            shutil.rmtree(x)
        except FileNotFoundError:
            print(f"no previous versions of {x} found")
    os.remove("main.spec")

    shutil.copytree(dependency_origin, dependency_destination)
    shutil.copytree("gfx", os.path.join(dist_dir, "gfx"))
    shutil.copytree("data", os.path.join(dist_dir, "data"))

    if not os.path.exists(dist_path):
        shutil.move(dist_dir, builds_directory)

    if compress:
        shutil.make_archive(dist_path, "bztar", dist_path)
        shutil.rmtree(dist_path)

    print("done!")
