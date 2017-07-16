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

import ini



## ============================ F U N C T I O N ============================ #
## integer main(string[])
##
## TITLE:       Main
## DESCRIPTION: Application entry point.
##
## PARAMETER: list of command-line arguments, starting with the script name.
##
## RETURNS: Integer exit code; handed back to the operating system.
def main(args):
    argc = len(args)
    if argc < 5:
        raise Exception('Insufficient number of arguments provided:\n%s' %
            '\n'.join(args) + '\n\nExiting...')
    from os import path, sep
    args[1] = args[1].rstrip().rstrip(sep)
    args[2] = args[2].rstrip().rstrip(sep)
    if path.isdir(args[1]) == False:
        raise Exception('Dependency source directory is inaccessible or ' +
            'does not exist: ' + args[1])
    assetDir = path.join(args[1], 'assets', args[4])
    libsDir = path.join(args[1], 'lib' + args[3], args[4])
    dirsToMake = []
    srcDepsToCopy = []
    dstDepsToCopy = []
    try:
        settings = ini.parse(assetDir + '.ini')
        for key in settings:
            filePath = path.join(args[1], 'assets', args[4], key)
            if path.isfile(filePath) == False:
                raise Exception('Asset INI section "' + key + '" does ' +
                    'not correspond to an accessible file in the assets ' +
                    'directory for target "' + args[4] + '"')
            copyKey = settings[key]['copy']
            if copyKey == '0':
                continue
            if copyKey != '1':
                raise Exception('Asset INI property "Copy" in section "' +
                    key + '" has an invalid value of "' + copyKey + '"; ' +
                    'must be either 0 or 1')
            # Otherwise copyKey must be 1
            if 'outputpath' in settings[key]:
                outpathKey = settings[key]['outputpath']
                if outpathKey.startswith('/') == False:
                    raise Exception('Asset INI property "OutputPath" in ' +
                        'section "' + key + '" has an invalid value of "' +
                        copyKey + '"; must begin with a forward slash')
                if outpathKey.endswith('/'):
                    raise Exception('Asset INI property "OutputPath" in ' +
                        'section "' + key + '" has an invalid value of "' +
                        copyKey + '"; cannot be a directory')
                outpathKey = outpathKey.lstrip('/')
                outpath = outpathKey.replace('/', sep)
                if '/' in outpathKey:
                    dir = path.dirname(outpath)
                    dirsToMake += [path.join(args[2], dir)]
                file = path.join(args[2], outpath)
                dstDepsToCopy += [file]
            else:
                dstDepsToCopy += [path.join(args[2], key)]
            srcDepsToCopy += [filePath]
        from os import listdir
        libs = listdir(libsDir)
        for lib in libs:
            if path.isfile(path.join(libsDir, lib)) == False:
                continue
            dstDepsToCopy += [path.join(args[2], lib)]
            srcDepsToCopy += [path.join(libsDir, lib)]
        # Perform the copy operation
        from os import makedirs
        for dir in dirsToMake:
            if path.exists(dir):
                continue
            makedirs(dir)
        i = 0
        fileCount = len(srcDepsToCopy)
        from shutil import copy2
        from os import stat
        while i < fileCount:
            src = srcDepsToCopy[i]
            dst = dstDepsToCopy[i]
            if path.exists(dst):
                srcMtime = stat(src).st_mtime_ns
                dstMtime = stat(dst).st_mtime_ns
                if srcMtime <= dstMtime:
                    i += 1
                    continue
            copy2(src, dst)
            i += 1
    except Exception as ex:
        from sys import stderr
        print(ex, file=stderr)
        return -3



## =========================== B O O T S T R A P =========================== #
## Application bootstrapper, guarding against code execution upon import.
if __name__ == '__main__':
    try:
        from sys import argv, exit
        exit(main(argv))
    except Exception as ex:
        raise ex
        return -2
    except:
        from sys import exc_info
        print('Rogue exception:', exc_info()[0])
        return -1
    return 0
