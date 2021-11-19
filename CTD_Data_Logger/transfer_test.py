import pysftp
import sys


host = "graemattersol.com"
password = "SiliconValleyBank"
username = "hyperkelp"

path = "/MojaveBin/"
localpath = "current_file.py"

with pysftp.Connection(host, username=username, password=password) as sftp:
        sftp.put("current_file.py","MojaveBin/current_file.py")

print("Upload done!")

