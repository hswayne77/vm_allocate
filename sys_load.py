#!/usr/bin/env python

import subprocess

xenservers = ['10.115.16.28', '10.115.16.29', '10.115.16.30']

def PoolwideSysload():
    loads = []
    for server in xenservers:
         cmd = "ssh %s '%s'" % (server,"~/monitor/host_monitor.py avg_load")
         proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
         (stdout, stderr) = proc.communicate()
         loads.append(stdout.strip())
         #loads.append(os.popen(cmd,'r',65536).read().strip())
    return loads

if __name__ == "__main__":
    for i in range(1,100):
        print PoolwideSysload()
