#!/usr/bin/env python3
# -*- coding: utf-8; mode: Python; indent-tabs-mode: nil; indent-width: 4; -*-
#
# OCO WORKING SET TOOLCHAIN
# Copyright (C) 2017 Arqadium. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# version 2.0.  If a copy of the MPL was not distributed with this file, then
# you can obtain one at <http://mozilla.org/MPL/2.0/>.
#



## ============================ F U N C T I O N ============================ #
## integer parseINI(string)
##
## TITLE:       INI Parser
## DESCRIPTION: A basic read-only INI parser function that creates a jagged
##              dictionary of sections and their key/value pairs.
##
## PARAMETER: The INI file to open and parse. This function does not check for
##            its existence!
##
## RETURNS: A dict<string, dict<string, string>> containing the INI's data.
def parse(fileName):
    from os import linesep
    f = open(fileName, 'r')
    iniLines = f.read(0x7FFFFFFF).split('\n')
    f.close
    badLines = []
    curSect = '' # Must be blank, for sectionless key/value pairs at the top
    ret = {'': {}}
    from re import fullmatch
    for line in iniLines:
        if fullmatch(r'\s*[#;][^$]*', line) != None:
            continue
        if fullmatch(r'\s*', line) != None:
            continue
        if line.startswith('['):
            name = line.lstrip('[').rstrip(']').lower()
            ret[name] = {}
            curSect = name
        elif '=' in line:
            pair = line.split('=', 1)
            key = pair[0].lower()
            if key in ret[curSect]:
                badLines[len(badLines)] = line
                continue
            ret[curSect][key] = pair[1]
        else:
            badLines[len(badLines)] = line
    if len(badLines) > 0:
        raise Exception('Parsing failed due to malformed syntax; the ' +
            'following lines were found to be invalid:\n' + '\n'.join(badLines)
            + '\n')
    return ret
