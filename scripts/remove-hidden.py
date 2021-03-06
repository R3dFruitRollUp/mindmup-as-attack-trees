#!/usr/bin/env python
from __future__ import print_function
from mindmup_as_attack_trees import *

import sys,json
import re
from collections import OrderedDict
import math
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('mupin', nargs='?', help="the mindmup file that will be processed -- transforming and augmenting the JSON")
args = parser.parse_args()

import ipdb
def info(type, value, tb):
	ipdb.pm()

sys.excepthook = info

levels_count = dict()
nodes_lookup = dict()
fixups_queue = list()
objective_node = None

if args.mupin is None:
	fd_in=sys.stdin
else:
	fd_in=open(args.mupin, 'r')

data = json.load(fd_in)

if args.mupin is None:
	fd_out = sys.stdout
else:
	fd_in.close()
	fd_out=open(args.mupin,'w')

nodes_context=list()

if 'id' in data and data['id'] == 'root':
	#version 2 mindmup
	root_node = data['ideas']['1']
else:
	root_node = data

def remove_hidden(node):
	for child in get_node_children(node):
		if get_node_title(child) == '.hidden':
			remove_child(node, child)
	return

apply_each_node(root_node, remove_hidden)

str = json.dumps(data, indent=2, sort_keys=True)
str = re.sub(r'\s+$', '', str, 0, re.M)
str = re.sub(r'\s+$', '', str, flags=re.M)

fd_out.write(str)

if len(sys.argv) >= 1:
	fd_out.close()

