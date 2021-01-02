import os

from PyQt5.QtGui import QIcon

cwd = os.getcwd()
data_dir = "data"

if cwd == "ScreenMoteInstall":
    data_dir = os.path.join("..", "data")

USERNAME = "pi"
HOST_NAME_TEMPLATE = "okr-pi-"
STATIC_IPV4S = False
VIEWER_LOCAL_PATH = os.path.join(data_dir, "viewer.py")
VIEWER_REMOTE_PATH = r"/home/pi/screenly/viewer.py"
CONFIG_LOCAL_PATH = os.path.join(data_dir, "config.txt")
CONFIG_REMOTE_PATH = r"/boot/config.txt"
DATABASE_PATH = r"/home/pi/.screenly/screenly.db"
DEPLOY_LOCAL_PATH = os.path.join(data_dir, "deploy_assets.py")
DEPLOY_REMOTE_PATH = r"deploy_assets.py"
MAC_FILE_PATH = os.path.join(data_dir, "macs.txt")
HOST_FILE_PATH = os.path.join(data_dir, "ipv4s.txt")
LOCAL_HOST_DATA_PATH = os.path.join(data_dir, "host_data.csv")
LOCAL_ASSET_DATA_PATH = os.path.join(data_dir, "assets.txt")

DEFAULT_CREDS_PATH = os.path.join(data_dir, "client_secrets.json")
GOOGLE_SHEET_NAME = "host_data"
GDRIVE_PW_FILE_ID = "1vXBoxq-KEPvQgF12uyaJ3K9Jv1lOwrxk"

VALID_COLOR = "#c4df9b"  # Green
WARNING_COLOR = "#fff79a"  # Yellow
INVALID_COLOR = "#f6989d"  # Red
VALID_COLOR_MAP = {True: VALID_COLOR, False: INVALID_COLOR}
ICON_SVG_PATH = os.path.join(os.path.split(__file__)[0], "..", "gfx", "icon.svg")
ICON_ICO_PATH = os.path.join(os.path.split(__file__)[0], "..", "gfx", "icon.ico")
ICON = QIcon(ICON_SVG_PATH)
