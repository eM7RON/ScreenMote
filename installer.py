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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, destination)
