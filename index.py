#!/usr/bin/env python3
#
# This document contains proprietary information of TRINITY SOFTWARE and/or its
# licenced developers and are protected by national and international copyright
# laws. They may not be disclosed to third parties or copied or duplicated in
# any form, in whole or in part, without the prior written consent of
# Trinity Software, LLC.
#



## ============================ F U N C T I O N ============================ ##
## void incrMajor(string)
##
## TITLE:       Increment major version number
## DESCRIPTION: Increments the major version number by 1, resetting the minor,
##              release, and build numbers to 0.
##
## PARAMETER: file path to the configuration header (usually C code) to modify.
def incrMajor(path):
	f = open(path, 'r')
	from os import linesep
	lines = f.read(0x7FFFFFFF).split(linesep)
	f.close()
	replaced = False
	from re import search
	for line, i in enumerate(lines):
		sMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_STRING(\s+)"([0-9]+)(\.[0-9]+\.[0-9]+\.[0-9]+")',
			line)
		nMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_MAJOR(\s+)([0-9]+)')
		if sMatch == None and nMatch == None:
			continue
		vMajorS = None
		vMajorN = None
		if sMatch != None:
			replaced = True
			vMajorS = int(sMatch.group(4))
			lines[i] = (sMatch.group(1) + sMatch.group(2) + '_VERSION_STRING' +
				sMatch.group(3) + '"' + str(vMajorS + 1) + sMatch.group(5))
		if nMatch != None:
			replaced = True
			vMajorN = int(nMatch.group(4))
			lines[i] = (nMatch.group(1) + nMatch.group(2) + '_VERSION_MAJOR' +
				nMatch.group(3) + str(vMajorN + 1))
		if vMajorS != vMajorN:
			print('WARNING: Discrepancy in major version definitions')
	f = open(path, 'w')
	f.write(lines.join(linesep))
	f.close()
	if replaced == False:
		print('WARNING: No version info definitions were found')



## ============================ F U N C T I O N ============================ ##
## void incrMinor(string)
##
## TITLE:       Increment minor version number
## DESCRIPTION: Increments the minor version number by 1, resetting the release
##              and build numbers to 0.
##
## PARAMETER: file path to the configuration header (usually C code) to modify.
def incrMinor(path):
	f = open(path, 'r')
	from os import linesep
	lines = f.read(0x7FFFFFFF).split(linesep)
	f.close()
	replaced = False
	from re import search
	for line, i in enumerate(lines):
		sMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_STRING(\s+"[0-9]+\.)([0-9]+)(\.[0-9]+\.[0-9]+")',
			line)
		nMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_MINOR(\s+)([0-9]+)')
		if sMatch == None and nMatch == None:
			continue
		vMajorS = None
		vMajorN = None
		if sMatch != None:
			replaced = True
			vMajorS = int(sMatch.group(4))
			lines[i] = (sMatch.group(1) + sMatch.group(2) + '_VERSION_STRING' +
				sMatch.group(3) + '"' + str(vMajorS + 1) + sMatch.group(5))
		if nMatch != None:
			replaced = True
			vMajorN = int(nMatch.group(4))
			lines[i] = (nMatch.group(1) + nMatch.group(2) + '_VERSION_MINOR' +
				nMatch.group(3) + str(vMajorN + 1))
		if vMajorS != vMajorN:
			print('WARNING: Discrepancy in minor version definitions')
	f = open(path, 'w')
	f.write(lines.join(linesep))
	f.close()
	if replaced == False:
		print('WARNING: No version info definitions were found')



## ============================ F U N C T I O N ============================ ##
## void incrRelease(string)
##
## TITLE:       Increment release version number
## DESCRIPTION: Increments the release version number by 1, resetting the build
##              version to 0.
##
## PARAMETER: file path to the configuration header (usually C code) to modify.
def incrRelease(path):
	f = open(path, 'r')
	from os import linesep
	lines = f.read(0x7FFFFFFF).split(linesep)
	f.close()
	replaced = False
	from re import search
	for line, i in enumerate(lines):
		sMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_STRING(\s+"[0-9]+\.[0-9]+\.)([0-9]+)(\.[0-9]+")',
			line)
		nMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_RELEASE(\s+)([0-9]+)')
		if sMatch == None and nMatch == None:
			continue
		vMajorS = None
		vMajorN = None
		if sMatch != None:
			replaced = True
			vMajorS = int(sMatch.group(4))
			lines[i] = (sMatch.group(1) + sMatch.group(2) + '_VERSION_STRING' +
				sMatch.group(3) + '"' + str(vMajorS + 1) + sMatch.group(5))
		if nMatch != None:
			replaced = True
			vMajorN = int(nMatch.group(4))
			lines[i] = (nMatch.group(1) + nMatch.group(2) + '_VERSION_RELEASE'
				+ nMatch.group(3) + str(vMajorN + 1))
		if vMajorS != vMajorN:
			print('WARNING: Discrepancy in release version definitions')
	f = open(path, 'w')
	f.write(lines.join(linesep))
	f.close()
	if replaced == False:
		print('WARNING: No version info definitions were found')



## ============================ F U N C T I O N ============================ ##
## void incrBuild(string)
##
## TITLE:       Increment build version number
## DESCRIPTION: Increments the build version number by 1.
##
## PARAMETER: file path to the configuration header (usually C code) to modify.
def incrBuild(path):
	f = open(path, 'r')
	from os import linesep
	lines = f.read(0x7FFFFFFF).split(linesep)
	f.close()
	replaced = False
	from re import search
	for line, i in enumerate(lines):
		sMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_STRING(\s+"[0-9]+\.[0-9]+\.[0-9]+\.)([0-9]+)"',
			line)
		nMatch = search(r'^(\s*#define\s+)(|[A-Z_][A-Z0-9_]*)' +
			r'_VERSION_MAJOR(\s+)([0-9]+)')
		if sMatch == None and nMatch == None:
			continue
		vMajorS = None
		vMajorN = None
		if sMatch != None:
			replaced = True
			vMajorS = int(sMatch.group(4))
			lines[i] = (sMatch.group(1) + sMatch.group(2) + '_VERSION_STRING' +
				sMatch.group(3) + '"' + str(vMajorS + 1) + '"')
		if nMatch != None:
			replaced = True
			vMajorN = int(nMatch.group(4))
			lines[i] = (nMatch.group(1) + nMatch.group(2) + '_VERSION_BUILD' +
				nMatch.group(3) + str(vMajorN + 1))
		if vMajorS != vMajorN:
			print('WARNING: Discrepancy in build version definitions')
	f = open(path, 'w')
	f.write(lines.join(linesep))
	f.close()
	if replaced == False:
		print('WARNING: No version info definitions were found')



## ============================ F U N C T I O N ============================ ##
## integer main(string[])
##
## TITLE:       Main
## DESCRIPTION: Application entry point.
##
## PARAMETER: list of command-line arguments, starting with the script name.
##
## RETURNS: Integer exit code; handed back to the operating system.
def main(args):
	try:
		import colour
		argc = len(args)
		if argc == 1:
			raise Exception('No command provided. Run ' +
				colour.bold('index.py help') + ' for a list of commands')
		if args[1] == 'increment':
			if argc < 3:
				raise Exception('No version level specified.')
			if argc < 4:
				raise Exception('No config header file specified.')
			from os.path import isfile
			if not isfile(args[3]):
				raise Exception('The specified config header was not found.')
			if args[2] == 'major':
				incrMajor(args[3])
			elif args[2] == 'minor':
				incrMinor(args[3])
			elif args[2] == 'release':
				incrRelease(args[3])
			elif args[2] == 'build':
				incrBuild(args[3])
			else:
				raise Exception('Invalid version level specified.')
	except Exception as ex:
		print('Exception raised:', ex)
		return -2
	except:
		print('Rogue exception:', sys.exc_info()[0])
		return -1
	return 0



## =========================== B O O T S T R A P =========================== ##
## Application bootstrapper, guarding against code execution upon import.
if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
