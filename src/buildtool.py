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
from subprocess import CalledProcessError, run, PIPE
import glob, ini, os, platform, re, shutil, sys

VSPATH = ''
LDLIBPATH = ''
if os.name == 'nt':
    VSPATH = os.path.join(os.getenv('PROGRAMFILES(X86)',
        os.environ['PROGRAMFILES']), 'Microsoft Visual Studio', '2017')
else:
    _LDLIBPATH = os.getenv('LD_LIBRARY_PATH', [])
    if _LDLIBPATH != []:
        LDLIBPATH = _LDLIBPATH[:-1].split(':')

def getMSVCPath():
    if os.name != 'nt':
        return ''
    ret = VSPATH
    ver = None
    for version in ['Enterprise', 'Professional', 'Community']:
        tmp = os.path.join(ret, version)
        if os.path.exists(tmp):
            ret = tmp
            break
    ret = os.path.join(ret, 'VC\\Tools\\MSVC')
    if os.path.isdir(ret):
        ret = os.path.join(ret, os.listdir(ret)[0])
    return ret

D_INSTALL_DIRS = [
    'C:\\Program Files\\DMD\\dmd2',
    'C:\\Program Files (x86)\\DMD\\dmd2',
    'C:\\DMD\\dmd2'
]

def getDPath():
    if os.name == 'nt':
        for dir in D_INSTALL_DIRS:
            if os.path.isdir(dir):
                return dir
        # No common installation directories exist
        return None
    # else: not Windows
    return '/usr/bin'

def pfspec(unix, nt):
    if os.name == 'nt':
        return nt
    return unix

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

PREFIX = color('[\u00D4\u00C7\u00F4]', fg='white', style='bold')
ACTIONS = {
    'asm':   color(fg='green',                s='Assembling') + '      ',
    'c':     color(fg='cyan',                 s='Compiling') + '       ',
    'c++':   color(fg='blue',                 s='Compiling') + '       ',
    'd':     color(fg='magenta',              s='Compiling') + '       ',
    'gfx':   color(fg='yellow',               s='Transmogrifying') + ' ',
    'conv':  color(fg='yellow', style='bold', s='Converting') + '      ',
    'link':  color(fg='red',                  s='Linking') + '         ',
    'lint':  color(fg='black', style='bold',  s='Linting') + '         '
}
HEADS = {
    'prep':  color('Preparing the build tool', fg='blue',
        style='bold+underline'),
    'start': color('Compilation started', fg='blue',
        style='bold+underline'),
    'pass':  color('Compilation passed', fg='green',
        style='bold+underline'),
    'fail':  color('Compilation failed', fg='red', style='bold+underline')
}
STARTUP = [
    '',
    'Arqadium Build Tool',
    'Part of the \u00D4\u00C7\u00F4 Working Set Toolchain',
    'Copyright \u00A9 2017 Arqadium. All rights reserved.',
    ''
]
DEBUG = sys.argv[2].startswith('debug')
IS64BIT = platform.machine().endswith('64')
TARGET = 'x64' if IS64BIT else 'x86' # x86, x64, arm, arm64
if sys.argv[2].endswith('64'):
    TARGET = 'x64'
elif sys.argv[2].endswith('32'):
    TARGET = 'x86'
WINARCH = 'X64' if IS64BIT else 'X86'
D_PATH = getDPath()
MSVCPATH = getMSVCPath()
MSVCBIN = MSVCPATH + '\\bin\\Host' + WINARCH + '\\' + TARGET
KITSPATH = 'C:\\Program Files (x86)\\Windows Kits\\10'
OBJEXT = pfspec('.o', '.obj')
CC = 'gcc'
CXX = CC
DC = 'dmd'
LINK = 'g++ -fuse-ld=gold'
AR = 'ar'
RES = 'test' # Dummy UNIX commands
RC = 'test'
GCC_VER = '0.0.0'
if os.name != 'nt':
    compl = run('gcc -dumpversion', shell=True, check=True, stdout=PIPE)
    GCC_VER = compl.stdout.decode().replace('\n', '')
LIBDIRS = pfspec([
    '/usr/lib/gcc/x86_64-pc-linux-gnu/' + GCC_VER
] + LDLIBPATH, [
    KITSPATH + '\\lib\\10.0.10586.0',
    MSVCPATH + '\\lib\\' + WINARCH,
    KITSPATH + '\\lib\\10.0.10586.0\\ucrt\\' + TARGET,
    KITSPATH + '\\lib\\10.0.10586.0\\um\\' + TARGET,
])
LIBS = pfspec([
    'gcc_s',
    'c',
    'gcc_s',
    'stdc++',
    'm',
    'gcc_s',
    'c',
    'gcc_s'
], [
    'kernel32',
    'user32',
    'gdi32',
    'winspool',
    'comdlg32',
    'advapi32',
    'shell32',
    'ole32',
    'oleaut32',
    'uuid',
    'odbc32',
    'odbccp32',
    'legacy_stdio_definitions'
])
INCDIRS = pfspec([], [
    MSVCPATH + '\\include',
    KITSPATH + '\\include\\10.0.10586.0\\shared',
    KITSPATH + '\\include\\10.0.10586.0\\ucrt',
    KITSPATH + '\\include\\10.0.10586.0\\um',
    '.\\deps\\include'
])
CFLAGS = [
    '-c',
    '-fPIC',
    '-mtune=generic',
    '-mfpmath=sse',
    '-x',
    'c',
    '-std=c11',
    '-pipe'
]
CPPFLAGS = [
    '-c',
    '-fPIC',
    '-mtune=generic',
    '-mfpmath=sse',
    '-x',
    'c++',
    '-std=c++14',
    '-pipe'
]
COUTFLAG = '-o'
CINCFLAG = '-iquote'
DFLAGS = [
    '-color',
    '-c'
]
DOUTFLAG = '-od='
DINCFLAG = '-I='
LINKFLAGS = []
LINKOUTFLAG = '-o'
LINKDIRFLAG = '-L'
LINKWINFLAG = pfspec('', '/IMPLIB:')
LINKLIBFLAG = '-l'
APPEXT = ''
SHAREDEXT = '.so'
STATICEXT = '.a'
BOOST_SUF = ''
RE_ISCPP = re.compile(r'\.((c|h)(pp|xx|\+\+)|cc|hh)$')
RE_ISSRC = re.compile(r'[\w_\-\.]+\.((c|h)(pp|xx|\+\+)?|cc|hh)|di?')
if os.name == 'nt':
    CC = MSVCBIN + '\\cl.exe'
    CXX = CC
    DC += '.exe'
    LINK = MSVCBIN + '\\link.exe'
    AR = MSVCBIN + '\\lib.exe'
    RES = MSVCBIN + '\\windres.exe'
    RC = KITSPATH + '\\bin\\' + TARGET + '\\rc.exe'
    APPEXT = '.exe'
    SHAREDEXT = '.dll'
    STATICEXT = '.lib'
    if D_PATH != None:
        # Append lib dirs
        tmp = [
            D_PATH + '\\windows\\lib'
        ]
        if IS64BIT:
            tmp += [
                D_PATH + '\\windows\\lib64'
            ]
        LIBDIRS += tmp
        # Append libs
        tmp = [
            'comctl32',
            'gdi32',
            'glu32',
            'opengl32',
            'rpcrt4',
            'version',
            'wininet',
            'winmm',
            'ws2_32',
            'wsock32'
        ]
        if IS64BIT:
            tmp += [
                'phobos64' if TARGET == 'x64' else 'phobos'
            ]
        LIBS += tmp
    CFLAGS = [
        '/bigobj',
        '/c',
        '/GF',
        '/nologo',
        '/Za',
        '/std:c++14',
        '/EHsc'
    ]
    COUTFLAG = '/Fo'
    CINCFLAG = '/I'
    LINKOUTFLAG = '/OUT:'
    LINKDIRFLAG = '/LIBPATH:'
    LINKLIBFLAG = '/DEFAULTLIB:'
    LINKFLAGS = ['/CGTHREADS:8', '/DYNAMICBASE', '/LARGEADDRESSAWARE',
        '/NOLOGO', '/NODEFAULTLIB:libcmt']
    if TARGET == 'x86':
        CFLAGS += ['/arch:SSE2', '/DARCH=32']
        LINKFLAGS += ['/MACHINE:X86']
    elif TARGET == 'x64':
        CFLAGS += ['/arch:AVX', '/DARCH=64']
        LINKFLAGS += ['/MACHINE:X64']
    if DEBUG:
        BOOST_SUF = '-vc141-mt-gd-1_64'
        CFLAGS += ['/Od', '/W3', '/UNDEBUG']
        LINKFLAGS += ['/DEBUG', '/OPT:NOREF', '/SUBSYSTEM:CONSOLE']
        
    else:
        BOOST_SUF = '-vc141-mt-1_64'
        CFLAGS += ['/GLdwy', '/O2t', '/w', '/DNDEBUG=1']
        LINKFLAGS += ['/RELEASE', '/OPT:REF', '/SUBSYSTEM:WINDOWS']
    CPPFLAGS = CFLAGS[:]
else: # UNIX
    if TARGET == 'x64':
        CFLAGS += ['-m64', '-march=sandybridge', '-mavx', '-DARCH=64']
        CPPFLAGS += ['-m64', '-march=sandybridge', '-mavx', '-DARCH=64']
    elif TARGET == 'x86':
        CFLAGS += ['-m32', '-march=pentium4', '-DARCH=32']
        CPPFLAGS += ['-m32', '-march=pentium4', '-DARCH=32']
    if DEBUG:
        CFLAGS += ['-UNDEBUG']
        CPPFLAGS += ['-UNDEBUG']
    else:
        CFLAGS += ['-DNDEBUG=1']
        CPPFLAGS += ['-DNDEBUG=1']
    if which(DC) != None:
        LIBS += ['phobos2']
# Both NT and UNIX
if DEBUG:
    DFLAGS += ['-debug', '-g', '-gs', '-boundscheck=on', '-w']
else:
    DFLAGS += ['-boundscheck=off', '-O', '-release', '-wi']
if TARGET == 'x86':
    DFLAGS += ['-m32', '-mcpu=baseline']
elif TARGET == 'x64':
    DFLAGS += ['-m64', '-mcpu=avx']

def pprint(s=None, action=None, head=None):
    if head != None and head in HEADS:
        print(PREFIX + ' ' + HEADS[head])
    elif not s:
        print(PREFIX)
    elif action != None and action in ACTIONS:
        print(PREFIX + ' ' + ACTIONS[action] +
            color(s, fg='black', style='bold') + '...')
    else:
        print(PREFIX + ' ' + s)

def usingUTF8():
    if os.name == 'nt':
        if sys.stdout.encoding != 'cp65001':
            run('chcp 65001', shell=True, check=True, stdout=PIPE)
            return False
    return True

def getSources(srcDir, langs, headers=False):
    # Gather all applicable file extensions
    exts = []
    if 'c' in langs:
        exts += ['c']
        if headers:
            exts += ['h']
    if 'c++' in langs:
        exts += ['cc', 'cpp', 'cxx', 'c++']
        if headers:
            if 'c' not in langs:
                exts += ['h']
            exts += ['hh', 'hpp', 'hxx', 'h++']
    if 'd' in langs:
        exts += ['d']
        if headers:
            exts += ['di']
    globBegin = os.path.join('.', srcDir, '**', '*.')
    # Do the globbing
    files = []
    for ext in exts:
        files += glob.glob(globBegin + ext, recursive=True)
    return files

def projectInit(projDir):
    # Ensure INIs all exist
    projectIniPath = os.path.join(projDir, 'project.ini')
    if os.path.isfile(projectIniPath) == False:
        raise Exception('\u2018' + projectIniPath + '\u2019 is inaccessible.')
    assetsIniPath = os.path.join(projDir, 'assets.ini')
    if os.path.isfile(assetsIniPath) == False:
        raise Exception('\u2018' + assetsIniPath + '\u2019 is inaccessible.')
    # Parse all of the INIs
    #print('Project INI...')
    projectIni = ini.parse(projectIniPath)
    #print('Assets INI...')
    assetsIni = ini.parse(assetsIniPath)
    #print('Done.')
    # Ensure schema is supported
    if(int(projectIni['']['version']) > 0
    or int(assetsIni['']['version']) > 0):
        raise Exception('One or more INI schemas in \u2018' + projDir +
            '\u2019 are unsupported')
    srcDir = projectIni['source']['sourcedir']
    incDir = projectIni['source']['includedir']
    # Get applicable languages
    _langs = projectIni['source']['langs']
    langs = []
    if ',' in _langs:
        langs += _langs.split(',')
    else:
        langs = [_langs]
    return (projectIni, assetsIni, srcDir, incDir, langs)

def lint(projectIni, srcDir):
    binSuffix = ''
    if os.name == 'nt':
        binSuffix = '.exe'
    _srcDir = os.path.join(srcDir, projectIni['']['name'],
        projectIni['source']['sourcedir'])
    if which('clang-format' + binSuffix) != None:
        sources = getSources(_srcDir, ['c', 'c++'], True)
        for source in sources:
            pprint(source, action='lint')
            run('clang-format' + binSuffix + ' -i -style=file ' + source,
                shell=True, check=True, stdout=PIPE)
    if which('dfmt' + binSuffix) != None:
        sources = getSources(srcDir, ['d'], True)
        for source in sources:
            pprint(source, action='lint')
            run('dfmt' + binSuffix + ' ' + source, shell=True, check=True,
                stdout=PIPE)

def main(args):
    # UTF-8 is off on Windows by default
    if not usingUTF8(): # This fixes it if it's off, though
        print('Changed the codepage to UTF-8. Please rerun this script.')
        return 0
    for line in STARTUP:
        pprint(line)
    argc = len(args) # Save CPU
    if argc < 3:
        raise Exception('Insufficient arguments provided')
    if not os.path.isfile(args[1]):
        raise Exception('Provided INI file is inaccessible')
    # The solution config file
    mainIni = ini.parse(args[1])
    if int(mainIni['']['version']) > 0:
        # v0 is the latest, as far as we know
        raise Exception('Future INI schema version found; not supported')
    # Either debug/release (w/ optional architecture), or we're linting
    if re.fullmatch(r'((debug|release)(32|64)?)|lint', args[2]) == None:
        raise Exception('Provided build type is invalid')
    pprint(head='prep')
    # Get the project list, ordered for dependency satisfaction
    projectNames = mainIni['']['order'].lower().split(',')
    i = 0
    projectCt = len(projectNames) # Save CPU
    taskName = 'build'
    projects = {}
    # Get settings for all the projects
    while i < projectCt:
        project = projectInit(mainIni['projects'][projectNames[i]])
        data = {
            projectNames[i]: {
                'projIni': project[0],
                'assetIni': project[1],
                'srcDir': project[2],
                'incDir': project[3],
                'langs': project[4]
            }
        }
        projects = {**projects, **data}
        i += 1
    i = 0
    pprint(head='start')
    try:
        if args[2] == 'lint':
            taskName = 'lint' # Used if things go wrong
            while i < projectCt:
                project = projects[projectNames[i]]
                pprint(project['projIni']['']['name'], action='lint')
                # 0 = project INI, 2 = source directory
                lint(project['projIni'], project['srcDir'])
                i += 1
        else: # compiling instead
            # Get project source directories for internal dependency inclusion
            localIncPaths = []
            while i < projectCt:
                project = projects[projectNames[i]]
                localIncPaths += [os.path.join(project['srcDir'],
                    project['projIni']['']['name'],
                    project['projIni']['source']['sourcedir'])]
                i += 1
            i = 0
            while i < projectCt:
                # Set up all project variables:-
                project = projects[projectNames[i]]
                # Applicable code languages in project
                pLangs = project['langs']
                # 'executable', 'shared', or 'static'
                pFormat = project['projIni']['output']['type']
                # list of libraries to link
                pLibs = LIBS[:] # Duplicate array
                if 'depends' in project['projIni']['']:
                    # Include all dependencies in library list
                    _libs = []
                    if ',' in project['projIni']['']['depends']:
                        _libs += project['projIni']['']['depends'].split(',')
                    else:
                        _libs += [project['projIni']['']['depends']]
                    if os.name == 'nt':
                        j = 0
                        _libsCt = len(_libs)
                        while j < _libsCt:
                            _libs[j] = _libs[j].replace('sfml-', 'sfml')
                            j += 1
                    pLibs += _libs
                # Full path for output binary, including name
                _name = project['projIni']['output']['name']
                if os.name != 'nt' and pFormat != 'executable':
                    _name = 'lib' + _name
                pOutPath = os.path.join(project['projIni']['output']['path'],
                    _name)
                # Language-agnostic location for object code
                pObjPath = os.path.join(project['projIni']['output']['path'],
                    'code', projectNames[i])
                if not os.path.exists(pObjPath):
                    if os.name == 'nt':
                        # Ya gotta keep 'em separated
                        if 'c' in pLangs or 'c++' in pLangs:
                            os.makedirs(os.path.join(pObjPath, 'c'))
                        if 'd' in pLangs:
                            os.makedirs(os.path.join(pObjPath, 'd'))
                    else:
                        os.makedirs(pObjPath)
                # Direct path to source code
                pSrcPath = os.path.join(project['srcDir'],
                    project['projIni']['']['name'],
                    project['projIni']['source']['sourcedir'])
                # Paths for C(++) #includes and D imports
                pIncPaths = [project['projIni']['source']['includedir'
                    ].replace('/', os.sep), project['incDir'].replace('/',
                    os.sep)] + INCDIRS + localIncPaths
                pObjGlob = os.path.join(pObjPath, '**', '*' + OBJEXT)
                libDepsPath = ''
                if os.name == 'nt':
                    # Manually include external dependencies, since Windows
                    # leaves us on our own with that
                    libDepsPath = '.\\deps\\lib'
                    if IS64BIT:
                        libDepsPath += '64'
                    else:
                        libDepsPath += '32'
                    if DEBUG:
                        libDepsPath += '\\debug'
                    else:
                        libDepsPath += '\\release'
                    if os.path.isdir(libDepsPath):
                        allDeps = os.listdir(libDepsPath)
                        for dep in allDeps:
                            if dep.lower().endswith('.dll'):
                                shutil.copy2(libDepsPath + '\\' + dep,
                                    project['projIni']['output']['path'])
                for lang in pLangs:
                    # Compile all C code
                    if lang == 'c':
                        flags = CFLAGS[:] # dup() array
                        if os.name == 'nt':
                            # Path must end with a backslash for CL.EXE
                            # Separate C(++) code from D code because of .obj
                            flags += [COUTFLAG + pObjPath + '\\c\\']
                        else:
                            flags += [COUTFLAG, pObjPath]
                        for incDir in pIncPaths:
                            if os.name == 'nt':
                                flags += [CINCFLAG + incDir]
                            else:
                                flags += [CINCFLAG, incDir]
                        if os.name == 'nt':
                            # MT = multithreaded app
                            # MD = multithreaded library
                            # d suffix = debugging
                            if DEBUG:
                                if pFormat == 'executable':
                                    flags += ['/MTd']
                                elif pFormat == 'shared':
                                    flags += ['/MDd']
                            else:
                                if pFormat == 'executable':
                                    flags += ['/MT']
                                elif pFormat == 'shared':
                                    flags += ['/MD']
                        sources = getSources(pSrcPath, ['c'])
                        for source in sources:
                            com = [CC] + flags
                            if os.name != 'nt':
                                com += [COUTFLAG, os.path.join(pObjPath,
                                    os.path.basename(source) + OBJEXT)]
                            com += [source]
                            # [2:] removes "./"
                            pprint(source[2:], action='c')
                            try:
                                run(' '.join(com), shell=True, check=True,
                                    stdout=PIPE)
                            except CalledProcessError as ex:
                                lines = ex.stdout.decode().splitlines()
                                for line in lines:
                                    print('ERROR: ' + line)
                                raise Exception('Compilation unit failed ' +
                                    'with command ' + color('', fg='white') +
                                    color(' '.join(com), fg='white'))
                    # Compile all project C++ code
                    elif lang == 'c++':
                        flags = CPPFLAGS[:] # Duplicate array
                        if os.name == 'nt':
                            # Path must end with a backslash for CL.EXE
                            # Separate C(++) code from D code because of .obj
                            flags += [COUTFLAG + pObjPath + '\\c\\']
                        for incDir in pIncPaths:
                            if os.name == 'nt':
                                flags += [CINCFLAG + incDir]
                            else:
                                flags += [CINCFLAG, incDir]
                        if os.name == 'nt':
                            # See notes above for flag meanings
                            if DEBUG:
                                if pFormat == 'executable':
                                    flags += ['/MTd']
                                elif pFormat == 'shared':
                                    flags += ['/MDd']
                            else:
                                if pFormat == 'executable':
                                    flags += ['/MT']
                                elif pFormat == 'shared':
                                    flags += ['/MD']
                        sources = getSources(pSrcPath, ['c++'])
                        for source in sources:
                            com = [CXX] + flags
                            if os.name != 'nt':
                                com += [COUTFLAG, os.path.join(pObjPath,
                                    os.path.basename(source) + OBJEXT)]
                            com += [source]
                            # [2:] removes "./"
                            pprint(source[2:], action='c++')
                            try:
                                run(' '.join(com), shell=True, check=True,
                                    stdout=PIPE)
                            except CalledProcessError as ex:
                                lines = ex.stdout.decode().splitlines()
                                for line in lines:
                                    print('ERROR: ' + line)
                                raise Exception('Compilation unit failed ' +
                                    'with command ' + color('', fg='white') +
                                    color(' '.join(com), fg='white'))
                    # Compile all project D code
                    elif lang == 'd':
                        # Separate D code from C(++) because of .obj
                        flags = DFLAGS
                        if os.name == 'nt':
                            flags += [DOUTFLAG + pObjPath + '\\d\\']
                        else:
                            flags += [DOUTFLAG + pObjPath]
                        if pFormat == 'shared':
                            flags += ['-shared']
                        for incDir in pIncPaths:
                            flags += [DINCFLAG + incDir]
                        sources = getSources(pSrcPath, ['d'])
                        for source in sources:
                            # Ignore these, only DMD cares about them
                            # They overwrite each other anyway
                            if source.endswith('package.d'):
                                continue
                            com = [DC, source] + flags
                            pprint(source[2:], action='d') # [2:] removes "./"
                            try:
                                run(' '.join(com), shell=True, check=True,
                                    stdout=PIPE)
                            except CalledProcessError as ex:
                                lines = ex.stdout.decode().splitlines()
                                for line in lines:
                                    print('ERROR: ' + line)
                                raise Exception('Compilation unit failed ' +
                                    'with command ' + color('', fg='white') +
                                    color(' '.join(com), fg='white'))
                # Link the project
                com = [LINK] + glob.glob(pObjGlob, recursive=True)
                # Append a file extension if needed
                if os.name == 'nt':
                    if pFormat == 'executable':
                        pOutPath += '.exe'
                    elif pFormat == 'shared':
                        pOutPath += '.dll'
                        # Windows needs this
                        com += ['/DLL']
                    elif pFormat == 'static':
                        pOutPath += '.lib'
                    # Give the output path to the linker
                    com += [LINKOUTFLAG + pOutPath]
                else:
                    if pFormat == 'shared':
                        pOutPath += '.so'
                        com += ['-shared']
                    elif pFormat == 'static':
                        pOutPath += '.a'
                    com += [LINKOUTFLAG, pOutPath]
                # Add common linker flags
                com += LINKFLAGS
                if libDepsPath != '':
                    # This is for external dependency linkage
                    com += [LINKDIRFLAG + libDepsPath]
                # Add build directory to lib search paths
                com += [LINKDIRFLAG + project['projIni']['output']['path']]
                for libPath in LIBDIRS:
                    # Add common lib search paths
                    com += [LINKDIRFLAG + libPath]
                # Add external dependency libs
                for lib in pLibs:
                    if os.name == 'nt':
                        # On Windows, boost is compiled funny. Check that
                        if lib.startswith('boost'):
                            com += [LINKLIBFLAG + lib + BOOST_SUF +
                                '.lib']
                        else:
                            com += [LINKLIBFLAG + lib + '.lib']
                    else:
                        com += [LINKLIBFLAG + lib]
                pprint(project['projIni']['output']['name'], action='link')
                # Link!
                try:
                    run(' '.join(com), shell=True, check=True,
                        stdout=PIPE)
                except CalledProcessError as ex:
                    lines = ex.stdout.decode().splitlines()
                    for line in lines:
                        print('ERROR: ' + line)
                    raise Exception('Compilation unit failed ' +
                        'with command ' + color('', fg='white') +
                        color(' '.join(com), fg='white'))
                i += 1
    except Exception as ex:
        pprint('Exception in ' + taskName + ': ' + color('{0}'.format(ex),
            style='bold'))
        pprint(head='fail')
        return -1
    pprint(head='pass')
    pprint()
    return 0

if __name__ == '__main__':
    from sys import argv, exit
    def _boot():
        try:
            ret = main(argv)
            if ret < 0:
                ret -= 2
            return ret
        except Exception as ex:
            pprint('Exception thrown: {0}'.format(ex))
            raise ex
            return -2
        except:
            from sys import exc_info
            pprint('Rogue exception:', exc_info()[0])
            return -1
    exit(_boot())
