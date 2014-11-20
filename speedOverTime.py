import subprocess
import time
import sys
import MonitorThread
import TestConfig
import ZfsApi

TestConfig.permissions_check()

subprocess.check_call(['zfs', 'list', '-t', 'filesystem', '-o', 'name'])

result = raw_input("Track which filesystem? ")

if not ZfsApi.fs_exists(result):
    print("Filesystem does not exist, exiting")
    sys.exit(1)

mt = MonitorThread.MonitorThread(result)
mt.start()

while True:
    time.sleep(500)

