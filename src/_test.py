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
## void vermodCheck(string, integer[], integer)
##
## TITLE:       VersionMod Checker
## DESCRIPTION: Checks the output of VersionMod for correctness.
##
## PARAMETER: Path to the sample file to inspect.
## PARAMETER: A 4-member ordered list of integers containing the correct
##            version numbers
def vermodCheck(filePath, versions, testNum):
    import colour
    exPrefix = colour.red('FAILURE') + ', Test #' + str(testNum) + ': '
    if len(versions) != 4:
        raise Exception(exPrefix + 'Versions list is of the wrong size!')
    vMajor = str(versions[0])
    vMinor = str(versions[1])
    vRelease = str(versions[2])
    vBuild = str(versions[3])
    vString = vMajor + '.' + vMinor + '.' + vRelease + '.' + vBuild
    f = open(filePath, 'r')
    text = f.read()
    from re import search
    if(search('_VERSION_STRING "' + vString + '"', text) == None
    or search('_VERSION_MAJOR\\s+' + vMajor, text) == None
    or search('_VERSION_MINOR\\s+' + vMinor, text) == None
    or search('_VERSION_RELEASE\\s+' + vRelease, text) == None
    or search('_VERSION_BUILD\\s+' + vBuild, text) == None):
        raise Exception(exPrefix + 'One or more definitions were missing ' +
            'or invalid.')
    print(colour.green('SUCCESS') + ', Test #' + str(testNum))



## ============================ F U N C T I O N ============================ #
## void main(string[])
##
## TITLE:       Main
## DESCRIPTION: Application entry point
##
## PARAMETER: list of command-line arguments, starting with the script name.
##
## RETURNS: Integer exit code; handed back to the operating system.
def main(args):
    # Define our test suite source files
    from os import mkdir, path
    sampleSrcPath = path.join('test', 'sample.h')
    testDirPath = path.join('build', 'test')
    sampleDstPath = path.join(testDirPath, 'sample.h')
    # Make our test suite's directories
    from shutil import copy2, rmtree
    try:
        rmtree('build')
    except:
        pass
    mkdir('build', 0o755)
    mkdir(testDirPath, 0o755)
    # Copy over our test suite sources
    copy2(sampleSrcPath, testDirPath)
    # Execute the tests!
    # Suite A: VersionMod script
    vermodCheck(sampleDstPath, [1, 1, 1, 1], 1)
    import versionmod
    versionmod.main(['versionmod.py', 'increment', 'major', sampleDstPath])
    vermodCheck(sampleDstPath, [2, 0, 0, 0], 2)
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    vermodCheck(sampleDstPath, [2, 0, 0, 3], 3)
    versionmod.main(['versionmod.py', 'increment', 'release', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    vermodCheck(sampleDstPath, [2, 0, 1, 2], 4)
    versionmod.main(['versionmod.py', 'increment', 'minor', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'release', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'release', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'release', sampleDstPath])
    versionmod.main(['versionmod.py', 'increment', 'build', sampleDstPath])
    vermodCheck(sampleDstPath, [2, 1, 3, 1], 5)
    versionmod.main(['versionmod.py', 'increment', 'major', sampleDstPath])
    vermodCheck(sampleDstPath, [3, 0, 0, 0], 6)
    import colour
    print(colour.green('versionmod.py has passed testing.'))
    # Suite B: CopyDeps script
    exprefix = colour.red('FAILURE') + ', Test #7: '
    from os import getcwd, listdir, path
    srcDir = path.join(getcwd(), 'test', 'deps')
    dstDir = path.join(getcwd(), 'build', 'test')
    import copydeps
    if(copydeps.main(['copydeps.py', srcDir, dstDir, '64', 'release'])
    != 0):
        raise Exception(exprefix + 'CopyDeps program failed testing.')
    assets = listdir(path.join(srcDir, 'assets', 'release'))
    for asset in assets:
        if path.isfile(asset) == False:
            continue
        bname = path.basename(asset)
        if path.isfile(path.join(dstDir, bname)) == False:
            raise Exception(exprefix + 'Asset file "' + bname + '" was ' +
                'not copied into the destination directory.')
    libs = listdir(path.join(srcDir, 'lib64', 'release'))
    for lib in libs:
        if path.isfile(lib) == False:
            continue
        bname = path.basename(lib)
        if path.isfile(path.join(dstDir, bname)) == False:
            raise Exception(exprefix + 'Library file "' + bname + '" was' +
                ' not copied into the destination directory.')
    print(colour.green('copydeps.py has passed testing.') + '\n...')
    print(colour.green('All tests have passed.') + ' Exiting...')



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
        print('Rogue exception:', sys.exc_info()[0])
        return -1
    return 0
