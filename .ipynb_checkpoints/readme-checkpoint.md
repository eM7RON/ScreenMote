# ScreenMote
This software offers remote management of multiple Raspberry Pis running Screenly-OSE. Exclusively, it is designed for working with Google Slides assets and will require modification to work with other types of assets. 

It basically provides a GUI for sending SSH commands to multiple Raspberry Pis.

It was built to be used for my own purposes but may be useful to anyone with the same needs.

### Requirements

Raspberry Pis should be either version 3B or 3B+  
Windows/Linux (Mac untested)  
Python 3  

#### Python environment

Untill a docker container is setup run commands:

`pip install paramiko`  
`pip install keyboard` 
`pip install pyqt5`  
`pip install gspread`  
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`  
`pip install oauth2client`  

On Linux it may be preferable to use `pip3` if this accesses python3 version of pip

`sudo apt install python3-pyqt5`  
may be required on linux if facing "Could not load the Qt platform plugin "xcb"" problem

#### Raspberry Pi setup

Download Screenly-OSE Sprint 10.1 release found here https://github.com/Screenly/screenly-ose/releases/tag/v0.18.3

We recommend flashing onto a micro SD card using BalenaEtcher.

Enable SSH on the Rasberry Pis by creating a file named `SSH` in the main directory.

Power up the Pis and change their names on the network using the format 'okr_pi_##' where `##` is a two digit number (leading zeros) in [0, 99]. Each Pi should have a unique number and thus name. Also note down each Pi's mac address and/or IPV4 address (if able to make static on network). These may also be learned later on by accessing the gateway or router. It is recommended that the SSH passwords of the Pis are changed from the default. The Raspberry Pis should share the same SSH password.

To work, a json file (named client_secrets.json) containing secret keys from a Google Cloud account with Drive, Sheets and Docs APIs enabled should be placed in the data directory.

The Google Cloud account should have a Google Sheets file named `host_data` (located at `MyDrive/OKRs/host_data`) with columns `#`, `Mac` and `IPV4` which denote a number (en of unique namnes we added earlier), mac address and IPV4 address. IPV4 entries may contain `None` if the IPV4 addresses are not static on the network. When IPV4s are not static the software will attempt to autonomously find the Raspberry Pis on the network by looking for mac addresses and then unique names. This feature is currently only available on Windows.

A Google Docs file at `MyDrive/OKRs/pw` should contain a sha256 hash of the Raspberry Pi's SSH password.

The Python scripts with the prefix `rpi` are standalone scripts designed to be run from a command line window or terminal. 
rpi_installer.py should be run to install some python scripts on the Raspberry Pis in order to allow updates to be sent and ScreenMote to work.

To create a standalone app, run `python constructor.py --compress`

The compress argument may be used to create a tar.bz2 otherwise it may be omitted.

The resulting build will be placed in the `builds` directory.

A build will be unique to a Platform and bit version i.e. building on Windows 32 bit will not produce an app for a Linux distribution or Windows 64 bit. 


<div>Icons made by <a href="https://www.flaticon.com/authors/roundicons" title="Roundicons">Roundicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
