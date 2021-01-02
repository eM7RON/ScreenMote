import os
import platform
import sys
import tarfile


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("incorrect number of arguments")
        sys.ext()
    install_location = sys.argv[1]
    os_id = platform.system()[:3]
    n_bits = platform.architecture()[0][:-3]
    version = "ScreenMote" + os_id + n_bits
    source = os.path.join("builds", version + ".tar.bz2")
    destination = os.path.join(install_location, version)
    with tarfile.open(source, "r:bz2") as tar:
        tar.extractall(destination)
