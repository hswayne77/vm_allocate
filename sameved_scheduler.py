#!/usr/bin/env python

import subprocess
import os,sys


def SAMEVEDFilter(session, host_refs, req_specs):
    """ filter avail hosts """
    hosts = {}
    for host_ref in host_refs:
        host_free_mem = float(session.xapi.host.compute_free_memory(host_ref))
        if req_specs['mem'] > host_free_mem:
            print "Removing the host=%s,free_mem=%s(VM specs: %s)" % (host_ref, host_free_mem, req_specs['mem'])
            host_refs.remove(host_ref)
        else:
            hosts[host_ref] = host_free_mem

    # return all the filtered hosts sorted by free-memory (big->small)
    filtered_host_ref = [host_ref for host_ref,free_mem in sorted(hosts.items(), key=lambda (k,v):(v,k), reverse=True)]
    print "filtered result=%s" % filtered_host_ref
    return filtered_host_ref


def FindMaxAvailMemHost(session=None):
    """ return the most free memory host to launch via `(host,free_mem)` tuple. """
    host_free_mem = {}
    for hostname,ip in xenservers.iteritems():
         cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py free_mem")
         #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
         #(stdout, stderr) = proc.communicate()
         host_ref = session.xapi.host.get_by_name_label(hostname)[0]
         #host_free_mem[host_ref] = stdout.strip()
         host_free_mem[host_ref] = float(os.popen(cmd).read().strip()) # memory(bytes)
    filtered_host_ref = [host_ref for host_ref,free_mem in sorted(host_free_mem.items(),key=lambda (k,v):(v,k),reverse=True)]
    print "[FindMaxAvailMemHost] %s" % sorted(host_free_mem.items(),key=lambda (k,v):(v,k),reverse=True)
    return filtered_host_ref[0]

def FindNextPeriodMinAvgLoadHost(session=None):
    next_loadavg = {}
    for hostname, ip in xenservers.iteritems():
        cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py next_loadavg")
        #cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py now_and_next_loadavg")
        #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #(stdout, stderr) = proc.communicate()
        #print "next_loadavg=%s" % os.popen(cmd).read().strip()
        host_ref = session.xapi.host.get_by_name_label(hostname)[0]
        next_loadavg[host_ref] = os.popen(cmd,'r',65536).read().strip()
        print "hostRef=%s, hostname=%s, next_load=%s" % (host_ref, hostname, next_loadavg[host_ref])
    filtered_host_ref = [ref for ref,load in sorted(next_loadavg.items(),key=lambda (k,v):(v,k))]
    return filtered_host_ref[0]

if __name__ == "__main__":
    # the following is your testing code.
    print FindMaxAvailMemHost()
    print FindNextPeriodMinAvgLoadHost()
