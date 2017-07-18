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

from colour import color
from subprocess import run, PIPE
import glob, ini, os, platform, sys



_prefix = color('[\u00D4\u00C7\u00F4]', fg='white', style='bold')
_actions = {
    'asm':   color(fg='green',                s='Assembling') + '      ',
    'c':     color(fg='cyan',                 s='Compiling') + '       ',
    'cxx':   color(fg='blue',                 s='Compiling') + '       ',
    'd':     color(fg='magenta',              s='Compiling') + '       ',
    'gfx':   color(fg='yellow',               s='Transmogrifying') + ' ',
    'conv':  color(fg='yellow', style='bold', s='Converting') + '      ',
    'link':  color(fg='red',                  s='Linking') + '         ',
    'lint':  color(fg='white',                s='Linting') + '         ',
    'clean': color(fg='white', style='bold', s='Cleaning') + ' '
}
_heads = {
    'start': color('Compilation started', fg='blue', style='bold+underline'),
    'pass':  color('Compilation passed', fg='green', style='bold+underline'),
    'fail':  color('Compilation failed', fg='red', style='bold+underline')
}
_is64bit = platform.machine().endswith('64')

## ============================ F U N C T I O N ============================ #
## void pprint(string)
##
## TITLE:       Pretty-print
## DESCRIPTION: Print a string with our vendor prefix attached and formatted.
##
## PARAMETER: The string to print after our vendor prefix (optional).
def pprint(s=None, action=None, head=None):
    if head != None and head in _heads:
        print(_prefix + ' ' + _heads[head])
    elif not s:
        print(_prefix)
    elif action != None and action in _actions:
        print(_prefix + ' ' + _actions[action] +
            color(s, fg='black', style='bold') + '...')
    else:
        print(_prefix + ' ' + s)



## ============================ F U N C T I O N ============================ #
## string[] getSources(string, string)
##
## TITLE:       Get Sources
## DESCRIPTION: Gets a list of source files for a given project.
##
## PARAMETER: Directory where the source code is located.
## PARAMETER: Language of files to search for.
##
## RETURNS: The list of source files as pathnames.
def getSources(srcDir, lang):
    files = []
    if lang == 'c':
        files += glob.glob(os.path.join(srcDir, '**', '*.c'),
            recursive=True)
    elif lang == 'c++':
        files += glob.glob(os.path.join(srcDir, '**', '*.cc'),
            recursive=True)
        files += glob.glob(os.path.join(srcDir, '**', '*.cpp'),
            recursive=True)
        files += glob.glob(os.path.join(srcDir, '**', '*.cxx'),
            recursive=True)
        files += glob.glob(os.path.join(srcDir, '**', '*.c++'),
            recursive=True)
    elif lang == 'asm':
        files += glob.glob(os.path.join(srcDir, '**', '*.s'), recursive=True)
        files += glob.glob(os.path.join(srcDir, '**', '*.asm'),
            recursive=True)
    elif lang == 'd':
        files += glob.glob(os.path.join(srcDir, '**', '*.d'), recursive=True)
    else:
        raise Exception('Invalid source language requested: \u2018' + lang +
            '\u2019')
    return files



## ============================ F U N C T I O N ============================ #
## void compile(string, string)
##
## TITLE:       Compile Source
## DESCRIPTION: Compiles a single source file into a single object code file.
##
## PARAMETER: Path to the given source file.
## PARAMETER: Language of file to compile.
##
## RETURNS: The list of source files as pathnames.
def compile(source, lang, srcDir, incDir, outName, outDir, debug=False):
    flags = [
        '-fPIC',
        '-c'
    ]
    tool = 'gcc'
    act = 'c'
    if sys.platform == 'win32':
        return
    if lang.startswith('c'):
        flags += ['-iquote', incDir]
    if lang == 'c':
        flags += [
            '-mtune=generic',
            '-mfpmath=sse',
            '-x',
            'c',
            '-std=c11'
        ]
    elif lang == 'c++':
        tool = 'g++'
        act = 'cxx'
        flags += [
            '-mtune=generic',
            '-mfpmath=sse',
            '-x',
            'c++',
            '-std=c++14'
        ]
    elif lang == 'd':
        tool = 'dmd'
        act = 'd'
        flags += ['-color']
    if sys.platform.startswith('linux'):
        if lang == 'd':
            if _is64bit:
                flags += ['-m64']
            else:
                flags += ['-m32']
        else:
            flags += ['-DLINUX=1']
            if _is64bit:
                flags += ['-m64', '-march=sandybridge', '-mavx', '-DARCH=64']
            else:
                flags += ['-m32', '-march=pentium4', '-DARCH=32']
    else:
        raise Exception('Unsupported UNIX-like platform')
    if debug:
        if lang == 'd':
            flags += ['-w', '-profile', '-boundscheck=on', '-mcpu=native',
                '-gc', '-debug', '-v']
        else:
            flags += ['-UNDEBUG']
    else:
        if lang == 'd':
            flags += ['-release', '-boundscheck=off', '-wi']
        else:
            flags += ['-DNDEBUG=1']
    pprint(source, action=act)
    outputFlag = ' -o '
    if lang == 'd':
        outputFlag = ' -of='
    run(tool + ' ' + ' '.join(flags) + outputFlag + os.path.join(outDir,
        'code', outName, source.replace(srcDir + os.sep, '').replace(os.sep,
        '+')) + '.o ' + source, shell=True, check=True, stdout=PIPE)



## ============================ F U N C T I O N ============================ #
## void buildExec(string, string, string[], string, string)
##
## TITLE:       Build Executable
## DESCRIPTION: Builds a standalone executable from source.
##
## PARAMETER: Directory where the source code is located.
## PARAMETER: Directory for the compiler to search for local includes.
## PARAMETER: List of internal libraries to link against.
## PARAMETER: List of languages to account for in the build.
## PARAMETER: The name of the output, not including prefixes or extensions.
## PARAMETER: Directory where the build process takes place.
## PARAMETER: Build type to create: either 'debug' or 'release'
def buildExec(srcDir, incDir, libs, langs, outName, outDir, type):
    for lang in langs:
        sources = getSources(srcDir, lang)
        for source in sources:
            compile(source, lang, srcDir, incDir, outName, outDir,
                type == 'debug')
    libflags = ''
    for lib in libs:
        libflags += ' -l ' + lib
    ofiles = ' '.join(glob.glob(os.path.join(outDir, 'code', outName, '*.o')))
    pprint(outName, action='link')
    linkerStart = 'g++ -L '
    outputFlag = ' -o '
    if 'd' in langs:
        linkerStart = 'dmd -L-rpath='
        outputFlag = ' -of='
    run(linkerStart + outDir + libflags + outputFlag + os.path.join(outDir,
        outName) + ' ' + ofiles, shell=True, check=True, stdout=PIPE)



## ============================ F U N C T I O N ============================ #
## void buildShared(string, string, string[], string, string)
##
## TITLE:       Build Shared Library
## DESCRIPTION: Builds a shared library (.so/.dll) from source.
##
## PARAMETER: Directory where the source code is located.
## PARAMETER: Directory for the compiler to search for local includes.
## PARAMETER: List of internal libraries to link against.
## PARAMETER: List of languages to account for in the build.
## PARAMETER: The name of the output, not including prefixes or extensions.
## PARAMETER: Directory where the build process takes place.
## PARAMETER: Build type to create: either 'debug' or 'release'
def buildShared(srcDir, incDir, libs, langs, outName, outDir, type):
    for lang in langs:
        sources = getSources(srcDir, lang)
        for source in sources:
            compile(source, lang, srcDir, incDir, outName, outDir,
                type == 'debug')
    libflags = ''
    for lib in libs:
        libflags += ' -l ' + lib
    ofiles = ' '.join(glob.glob(os.path.join(outDir, 'code', outName, '*.o')))
    pprint(outName, action='link')
    linkerStart = 'g++ -L '
    outputFlag = ' -o '
    if 'd' in langs:
        linkerStart = 'dmd -L-rpath='
        outputFlag = ' -of='
    run(linkerStart + outDir + libflags + outputFlag + os.path.join(outDir,
        'lib' + outName) + '.so -shared ' + ofiles, shell=True, check=True,
        stdout=PIPE)



## ============================ F U N C T I O N ============================ #
## void buildStatic(string, string, string[], string, string)
##
## TITLE:       Build Static Library
## DESCRIPTION: Builds a static library (.a/.lib) from source.
##
## PARAMETER: Directory where the source code is located.
## PARAMETER: Directory for the compiler to search for local includes.
## PARAMETER: List of internal libraries to link against.
## PARAMETER: List of languages to account for in the build.
## PARAMETER: The name of the output, not including prefixes or extensions.
## PARAMETER: Directory where the build process takes place.
## PARAMETER: Build type to create: either 'debug' or 'release'
def buildStatic(srcDir, incDir, libs, langs, outName, outDir, type):
    for lang in langs:
        sources = getSources(srcDir, lang)
        for source in sources:
            compile(source, lang, srcDir, incDir, outName, outDir,
                type == 'debug')
    libflags = ''
    for lib in libs:
        libflags += ' -l ' + lib
    ofiles = ' '.join(glob.glob(os.path.join(outDir, 'code', outName, '*.o')))
    pprint(outName, action='link')
    if 'd' in langs:
        raise Exception('Cannot yet build static library from D source.')
    run('g++ -L ' + outDir + libflags + ' -o ' + os.path.join(outDir,
        'lib' + outName) + '.a -static ' + ofiles, shell=True, check=True,
        stdout=PIPE)



def projectInit(projDir):
    # Ensure INIs all exist
    projectIniPath = os.path.join(projDir, 'project.ini')
    if os.path.isfile(projectIniPath) == False:
        raise Exception('\u2018' + projectIniPath + '\u2019 is inaccessible.')
    assetsIniPath = os.path.join(projDir, 'assets.ini')
    if os.path.isfile(assetsIniPath) == False:
        raise Exception('\u2018' + assetsIniPath + '\u2019 is inaccessible.')
    # Parse all of the INIs
    projectIni = ini.parse(projectIniPath)
    assetsIni = ini.parse(assetsIniPath)
    # Ensure schema is supported
    if(int(projectIni['']['version']) > 0
    or int(assetsIni['']['version']) > 0):
        raise Exception('One or more INI schemas in \u2018' + projDir +
            '\u2019 are unsupported')
    srcDir = os.path.join(projDir, projectIni['source']['sourcedir'])
    incDir = os.path.join(projDir, projectIni['source']['includedir'])
    # Get applicable languages
    _langs = projectIni['source']['langs']
    langs = []
    if ',' in _langs:
        langs += _langs.split(',')
    else:
        langs = [_langs]
    return (projectIni, assetsIni, srcDir, incDir, langs)



## ============================ F U N C T I O N ============================ #
## integer build(string)
##
## TITLE:       Build Project
## DESCRIPTION: Builds a single project from source.
##
## PARAMETER: Directory where the project is located.
## PARAMETER: Type of project to compile; may be 'debug' or 'release'.
def build(projDir, type):
    _init = projectInit(projDir)
    projectIni = _init[0]
    assetsIni = _init[1]
    srcDir = _init[2]
    incDir = _init[3]
    langs = _init[4]
    # Set up output file strings
    outName = projectIni['output']['name']
    outDir = os.path.join(os.getcwd(), projectIni['output']['path'])
    codeDir = os.path.join(outDir, 'code', outName)
    if not os.path.exists(codeDir):
        os.makedirs(codeDir)
    # Set up library names for linker
    libs = []
    if 'depends' in projectIni['']:
        if ',' in projectIni['']['depends']:
            libs += projectIni['']['depends'].split(',')
        else:
            libs = [projectIni['']['depends']]
    # Build the project
    if(projectIni['output']['type'] == 'executable'):
        buildExec(srcDir, incDir, libs, langs, outName, outDir, type)
    elif(projectIni['output']['type'] == 'shared'):
        buildShared(srcDir, incDir, libs, langs, outName, outDir, type)
    elif(projectIni['output']['type'] == 'static'):
        buildStatic(srcDir, incDir, libs, langs, outName, outDir, type)
    else:
        raise Exception('Invalid output type for project')



## ============================ F U N C T I O N ============================ #
## integer which(string)
##
## TITLE:       Which Executable
## DESCRIPTION: Checks for the location of executable on the system.
##
## PARAMETER: Name of the binary to check for.
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None



## ============================ F U N C T I O N ============================ #
## integer lint(string)
##
## TITLE:       Lint Project
## DESCRIPTION: Lints/formats all of the code in a given project. Currently
##              supports C code using lint, C++ code using clang-format, and
##              D code using dscanner.
##
## PARAMETER: Directory where the project is located.
def lint(projDir):
    _init = projectInit(projDir)
    projectIni = _init[0]
    srcDir = _init[2]
    langs = _init[4]
    progs = []
    if 'cxx' in langs or 'c' in langs:
        progs += ['clang-format']
        if os.name == 'nt':
            progs[-1] += '.exe'
    if 'd' in langs:
        progs += ['dscanner']
        if os.name == 'nt':
            progs[-1] += '.exe'
    for prog in progs:
        if which(prog) == None:
            raise Exception('Linting program "' + prog + '" is missing')
    for lang in langs:
        sources = getSources(srcDir, lang)
        for source in sources:
            pprint(source, action='lint')
            if lang == 'd':
                run('dfmt ' + source, shell=True, check=True, stdout=PIPE)
            else:
                run('clang-format -style=file ' + source, shell=True,
                    check=True, stdout=PIPE)



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
    if os.name == 'nt':
        from locale import getpreferredencoding
        if getpreferredencoding() != 'cp65001':
            from subprocess import run, PIPE
            run('chcp 65001', shell=True, check=True, stdout=PIPE)
            print('Changed the codepage to UTF-8. Please rerun this script.')
            return 0
    pprint()
    pprint('Arqadium Build Tool')
    pprint('Part of the \u00D4\u00C7\u00F4 Working Set Toolchain')
    pprint('Copyright \u00A9 2017 Arqadium. All rights reserved.')
    pprint()
    argc = len(args)
    if argc < 3:
        raise Exception('Insufficient arguments provided')
    if os.path.isfile(args[1]) == False:
        raise Exception('Provided INI file is inaccessible')
    mainIni = ini.parse(args[1])
    if int(mainIni['']['version']) > 0:
        raise Exception('Future INI schema version found; not supported')
    if args[2] == 'lint':
        for key in mainIni['projects']:
            lint(mainIni['projects'][key])
        return 0
    from re import fullmatch
    if fullmatch(r'debug|release', args[2]) == None:
        raise Exception('Provided build type is invalid')
    pprint(head='start')
    try:
        for key in mainIni['projects']:
            build(mainIni['projects'][key], args[2])
    except Exception as ex:
        pprint('Exception in build: ' + color('{0}'.format(ex), style='bold'))
        pprint(head='fail')
        raise ex
        return -3
    pprint(head='pass')



## =========================== B O O T S T R A P =========================== ##
## Application bootstrapper, guarding against code execution upon import.
if __name__ == '__main__':
    try:
        from sys import argv, exit
        main(argv)
    except Exception as ex:
        raise ex
    except:
        from sys import exc_info
        print('Rogue exception:', exc_info()[0])
