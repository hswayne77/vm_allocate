#!/usr/bin/env python

import subprocess
import os,sys




def SAMEVEDFilter(session, host_refs, req_specs):
    """ filter avail hosts to meets the user rquirement. """
    for host_ref in host_refs:
        host_free_mem = float(session.xapi.host.compute_free_memory(host_ref))
        if req_specs['mem'] > host_free_mem:
            print "Removing the host=%s,free_mem=%s(VM specs: %s)" % (host_ref, host_free_mem, req_specs['mem'])
            host_refs.remove(host_ref)
    return host_refs 

def FirstFit(session, req_specs):
    """ random select the filtered hosts. """
    host_refs = session.xapi.host.get_all()
    filtered_host_refs = SAMEVEDFilter(session, host_refs, req_specs)
    if not filtered_host_refs: # if no any hosts can allocate vms,
       return None             # we return None here.
    import random
    return filtered_host_refs[random.randint(0,len(filtered_host_refs)-1)]


def BestFit(session, req_specs):
    """ choose the current load is the smallest one."""
    host_loadavg = {}
    for hostname, ip in xenservers.iteritems():
        cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py loadavg")
        host_ref = session.xapi.host.get_by_name_label(hostname)[0]
        host_loadavg[host_ref] = float(os.popen(cmd).read().strip())
    # sorted by loadavg(small->big)    
    sorted_host_ref = [host_ref for host_ref,loadavg in sorted(host_loadavg.iteritems(),key=lambda (k,v):(v,k))]
    filtered_host_ref = SAMEVEDFilter(session, sorted_host_ref, req_specs)
    return filtered_host_ref[0] 

def FindMaxAvailMemHost(session, req_specs):
    """ return the most free memory host to launch via `(host,free_mem)` tuple. """
    host_free_mem = {}
    for hostname,ip in xenservers.iteritems():
        cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py free_mem")
        #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        #(stdout, stderr) = proc.communicate()
        #host_free_mem[host] = stdout.strip()
        host_ref = session.xapi.host.get_by_name_label(hostname)[0]
        host_free_mem[host_ref] = float(os.popen(cmd).read().strip()) # memory(bytes)
    # sorted by free memory(big->small)
    sorted_host_ref = [host_ref for host_ref,free_mem in sorted(host_free_mem.items(),key=lambda (k,v):(v,k),reverse=True)]
    print "[FindMaxAvailMemHost] %s" % sorted(host_free_mem.items(),key=lambda (k,v):(v,k),reverse=True)
    # filtering
    filtered_host_ref = SAMEVEDFilter(session, sorted_host_ref, req_specs)
    return filtered_host_ref[0] 

def FindNextPeriodMinAvgLoadHost(session, req_specs):
    next_loadavg = {}
    for hostname, ip in xenservers.iteritems():
        cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py next_loadavg")
        #cmd = "ssh %s '%s'" % (ip,"~/monitor/host_monitor.py now_and_next_loadavg")
        host_ref = session.xapi.host.get_by_name_label(hostname)[0]
        next_loadavg[host_ref] = os.popen(cmd,'r',65536).read().strip()
        #print "hostRef=%s, hostname=%s, next_load=%s" % (host_ref, hostname, next_loadavg[host_ref])
    # sort by load(small to big)
    sorted_host_ref = [ref for ref,load in sorted(next_loadavg.items(),key=lambda (k,v):(v,k))]
    # filtering
    filtered_host_ref = SAMEVEDFilter(session, sorted_host_ref, req_specs)
    return filtered_host_ref[0]

if __name__ == "__main__":
    # the following is your testing code.
    print FindMaxAvailMemHost()
    print FindNextPeriodMinAvgLoadHost()
