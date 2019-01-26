#!/usr/bin/env python

import json
import os
import re
import sys


def show_usage():
    print('Wrong number of arguments!\nUsage: ./psplibconverter.py smfilename')


def extract_val(lines, line_prefix, exception_msg, sep=':'):
    for line in lines:
        if line.strip().startswith(line_prefix):
            return int(re.sub('\D', '', line.split(sep)[1]))
    raise Exception(exception_msg)


def index_of_line_starting_with(prefix, lines):
    ctr = 0
    for line in lines:
        if line.startswith(prefix):
            return ctr
        ctr += 1
    raise Exception('No line starting with prefix: ' + prefix + ' found in list!')


def extract_adj_mx(lines):
    global adjMx
    ix = index_of_line_starting_with('PRECEDENCE RELATIONS:', lines)
    adjMx = [[0 for i in range(njobs)] for j in range(njobs)]
    for line in lines[ix + 2:ix + 2 + njobs]:
        parts = line.split()
        j = int(parts[0])
        succs = parts[3:]
        for succ in succs:
            adjMx[j - 1][int(succ) - 1] = 1
    return adjMx


def extract_job_attributes(lines):
    ix = index_of_line_starting_with('REQUESTS/DURATIONS:', lines)
    durations = [0 for i in range(njobs)]
    demands = [[0 for r in range(njobs)] for j in range(nres)]
    for line in lines[ix + 3:ix + 3 + njobs]:
        parts = line.split()
        j = int(parts[0])
        durations[j - 1] = int(parts[2])
        for r in range(nres):
            demands[r][j - 1] = int(parts[3 + r])
    return durations, demands


def extract_resource_capacities(lines):
    ix = index_of_line_starting_with('RESOURCEAVAILABILITIES', lines)
    return list(map(lambda capstr: int(capstr), lines[ix + 2].split()))


def compute_revenue_function(durations, adj_mx, demands, capacities):
    return None


def parse_lines(lines):
    global njobs, nperiods, nres
    njobs = extract_val(lines, 'jobs (incl. supersource/sink', 'Unable to extract number of jobs!')
    nperiods = extract_val(lines, 'horizon', 'Unable to extract number of time periods!')
    nres = extract_val(lines, '- renewable', 'Unable to extract number of resources!')
    durations, demands = extract_job_attributes(lines)
    capacities = extract_resource_capacities(lines)
    adj_mx = extract_adj_mx(lines)
    data = {
        'numjobs': njobs,
        'numperiods': nperiods,
        'numresources': nres,
        'durations': durations,
        'demands': demands,
        'capacities': capacities,
        'adjacencyMatrix': adj_mx,
        'kappa': 0.5,
        'zmax': list(map(lambda cap: round(cap * 0.5), capacities)),
        'u': compute_revenue_function(durations, adj_mx, demands, capacities)
    }
    return data


def write_data_to_gams_file(data, instname):
    with open(instname + '.gms', 'w') as fp:
        ostr = 'sets\n'
        ostr += 'j /j1*j' + str(data['numjobs']) + '/\n'
        ostr += 't /t1*t' + str(data['numperiods']) + '/\n'
        ostr += 'r /r1*r' + str(data['numresources']) + '/;\n'
        ostr += 'alias(j,i);\nalias(t,tau);\n'
        ostr += 'sets\n'
        ostr += 'pred(i,j);\n'
        ostr += 'parameters\n'
        ostr += 'zmax(r) //\n'
        ostr += 'kappa(r)\ncapacities(r)\ndurations(j)\nu(t)\nefts(j)\nlfts(j)\n'
        ostr += 'demands(j,r)\nseedsol(j);\n'
        ostr += 'execute_unload \'' + instname + '.gdx\' '
        fp.write(ostr)


def sm_to_object(smfilename):
    with open(smfilename, 'r') as fp:
        return parse_lines(fp.readlines())


def convert_file(smfilename):
    instname = os.path.splitext(os.path.basename(smfilename))[0]
    data = sm_to_object(smfilename)
    with open(instname + '.json', 'w') as jsonfp:
        jsonfp.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    write_data_to_gams_file(data, instname)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        show_usage()
    else:
        convert_file(sys.argv[1])
