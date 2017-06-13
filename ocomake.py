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
        import os
        if os.name == 'nt':
            from subprocess import run, PIPE
            run('chcp 65001', shell=True, check=True, stdout=PIPE)
        print('\n\u00D4\u00C7\u00F4Make Engine Buildtool')
        print('Part of the \u00D4\u00C7\u00F4 Working Set Toolchain')
        print('Copyright \u00A9 2017 Trinity Software. All rights reserved.\n')
        argc = len(args)
        
    except Exception as ex:
        raise ex
        return -2
    except:
        from sys import exc_info
        print('Rogue exception:', exc_info()[0])
        return -1
    return 0



## =========================== B O O T S T R A P =========================== ##
## Application bootstrapper, guarding against code execution upon import.
if __name__ == '__main__':
    from sys import argv, exit
    exit(main(argv))
