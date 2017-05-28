#!/usr/bin/env python3
# -*- coding: utf-8; mode: Python; indent-tabs-mode: nil; c-basic-offset: 4 -*-
#
# Copyright (C) 2017 Trinity Software, LLC. All rights reserved.
#
# This document contains proprietary information of TRINITY SOFTWARE and/or its
# licenced developers and are protected by national and international copyright
# laws. They may not be disclosed to third parties or copied or duplicated in
# any form, in whole or in part, without the prior written consent of
# Trinity Software, LLC.
#



## ============================ F U N C T I O N ============================ ##
## void modVersion(string, string)
##
## TITLE:       Modify version strings in a header file.
## DESCRIPTION: This modifies all of the version string #defines it can find in
##              a specified text file, incrementing a given level and resetting
##              all of the levels below it to zero. For example, specifying
##              a minor version level will increment the minor version by 1 and
##              reset the release and build versions to 0; the major version
##              will remain the same.
##
## PARAMETER: File path to the configuration header (usually C code) to modify.
## PARAMETER: The level to target for modification. Possible values are:
##              - 'major'
##              - 'minor'
##              - 'release'
##              - 'build'
def modVersion(path, level):
	f = open(path, 'r')
	from os import linesep
	lines = f.read(0x7FFFFFFF).splitlines()
	f.close()
	replaced = False
	from re import compile
	sPatt = compile(r'^(\s*\#define\s+)(|([A-Z_][A-Z0-9_]*))' +
		r'(_VERSION_STRING\s+")([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)"')
	nPatt = compile(r'^(\s*\#define\s+)(|([A-Z_][A-Z0-9_]*))' +
		r'(_VERSION_)(MAJOR|MINOR|RELEASE|BUILD)(\s+)([0-9]+)')
	linesLen = len(lines)
	i = 0
	foundString = False
	foundMajor = False
	foundMinor = False
	foundRelease = False
	foundBuild = False
	while i < linesLen:
		sMatch = sPatt.search(lines[i])
		if sMatch == None:
			nMatch = nPatt.search(lines[i])
			if nMatch == None:
				i += 1
				continue
			curLevel = nMatch.group(5).lower()
			number = int(nMatch.group(7), 10)
			if level == 'major':
				if curLevel != 'major':
					number = 0
				else: # Must be 'major' then
					number += 1
			if level == 'minor':
				if curLevel != 'major' and curLevel != 'minor':
					number = 0
				elif curLevel == level:
					number += 1
			if level == 'release':
				if curLevel == 'build':
					number = 0
				elif curLevel == level:
					number += 1
			if level == 'build':
				if curLevel == level:
					number += 1
			if curLevel == 'major':
				foundMajor = True
			elif curLevel == 'minor':
				foundMinor = True
			elif curLevel == 'release':
				foundRelease = True
			elif curLevel == 'build':
				foundBuild = True
			lines[i] = (nMatch.group(1) + nMatch.group(2) + nMatch.group(4) +
				nMatch.group(5) + nMatch.group(6) + str(number))
		else:
			foundString = True
			vMajor = int(sMatch.group(5), 10)
			vMinor = int(sMatch.group(6), 10)
			vRelease = int(sMatch.group(7), 10)
			vBuild = int(sMatch.group(8), 10)
			if level == 'major':
				vMajor += 1
				vMinor = 0
				vRelease = 0
				vBuild = 0
			elif level == 'minor':
				vMinor += 1
				vRelease = 0
				vBuild = 0
			elif level == 'release':
				vRelease += 1
				vBuild = 0
			elif level == 'build':
				vBuild += 1
			lines[i] = (sMatch.group(1) + sMatch.group(2) + sMatch.group(4) +
				str(vMajor) + '.' + str(vMinor) + '.' + str(vRelease) + '.' +
				str(vBuild) + '"')
		i += 1
	f = open(path, 'w')
	f.write('\n'.join(lines))
	f.close()
	if foundString == False:
		print('WARNING: Did not find any instances of a version string!')
	if foundMajor == False:
		print('WARNING: Did not find any instances of a major version number!')
	if foundMinor == False:
		print('WARNING: Did not find any instances of a minor version number!')
	if foundRelease == False:
		print('WARNING: Did not find any instances of a release version ' +
			'number!')
	if foundBuild == False:
		print('WARNING: Did not find any instances of a build version number!')



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
		print('\nProject Version Autoincrement Utility')
		print('Part of the ÔÇô Working Set Toolchain')
		print('Copyright © 2017 Trinity Software. All rights reserved.\n')
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
			if isfile(args[3]) == False:
				raise Exception('The specified config header was not found.')
			if(args[2] != 'major'
			and args[2] != 'minor'
			and args[2] != 'release'
			and args[2] != 'build'):
				raise Exception('Invalid version level specified.')
			modVersion(args[3], args[2])
		elif args[1] == 'help':
			if argc > 2:
				i = 2
				while i < argc:
					print('Unknown help option "%s"' % args[i])
					i += 1
				print('\nUsage:-\n')
				print('    $ python3 versionmod.py increment ', end='')
				print('<versionlevel> <config header>\n')
	except Exception as ex:
		raise ex
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
