#!/usr/bin/python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import json

def log(log):
  print log

def parse(buglist, commits):
  with open(buglist) as data_file:    
    bugs = json.load(data_file)['bugs']

  with open(commits, "r") as lines:
    record = dict({})
    co = ''
    bug = ''
    for line in lines:
      line = line.strip().lower();
      if line.startswith('commit'):
        co = line.split(' ')[1]
        bug = ''
      elif line.startswith('bug'):
        bug = line.split(' ')[1]
        found = False
        for b in bugs:
          if bug == str(b['id']):
            record[bug] = {'commit': co, 'summary': b['summary'], 'app': set()}
            found = True
            b['checked'] = True
            break
        if found == False:
          bug = ''
          co = ''
      elif line.startswith(':') and co != '' and bug != '':
        token = line.split('/')
        filepath = token[0].split('\t')[-1]
        if (filepath == 'tv_apps' or filepath == 'apps'):
          filepath = token[1]
        record[bug]['app'].add(filepath)

  for bid in sorted(record.iterkeys()):
    modules = ', '.join(s for s in record[bid]['app'])
    log('Bug ' + bid + ' - ' + record[bid]['summary'])
    log('  commit: ' + record[bid]['commit'])
    log('  app: ' + modules + '\n')

  # some bugs may not in the commits, print them out
  for b in bugs:
    if (b.has_key('checked') == False):
      log(str(b['id']))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: parse.py <buglist> <commits>"
        exit(0)
    parse(sys.argv[1], sys.argv[2])
