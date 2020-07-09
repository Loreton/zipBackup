#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 06-07-2020 19.46.57
#

import sys; sys.dont_write_bytecode=False
import os
import argparse
# import subprocess, shlex
import pdb
import json
# import hashlib
from pathlib import Path

#
##############################################################
# - Parse Input
##############################################################
def ParseInput():
    ####################################
    # # _fileCheck()
    ####################################
    def check_dir(path):
        p = Path(path)
        if p.is_dir():
            return str(p.resolve())
        else:
            print('    [Ln] - Input arg ERROR: dir: {p} is not valid.'.format(**locals()))
            sys.exit(1)


    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='ebooks management')

    parser.add_argument('--source-dir', required=False, default='/mnt/k/Filu/LnDisk', metavar='', type=check_dir,
                            help='specify source parent directory')
    parser.add_argument('--dest-dir',  required=False, default='/mnt/c/Filu_C/LnDisk', metavar='', type=check_dir,
                            help='specify destination parent directory for zip_file')
    parser.add_argument('--dirs', required=False, default=['Loreto', 'Lesla'], metavar='', nargs='*',
                            help="specify [source-dir]/children directory name(s) to be zipped")
    parser.add_argument('--zip-type', required=False, choices=['zip', '7z'], default='zip', metavar='',
                            help="specify type of compression program [zip|7z]")
    parser.add_argument('--deep-level', required=False, default=0, metavar='', type=int,
                            help='how many levels of sub-dirs...')
    parser.add_argument('--crypt',  action='store_true', help='specify if zip file must be crypted.')
    parser.add_argument('--debug',  action='store_true', help='display debug data.')
    parser.add_argument('--go',           action='store_true', help='specify if command must be executed. (dry-run is default)')
    parser.add_argument('--display-args', action='store_true', help='Display input parameters')

    args = parser.parse_args()

    if args.display_args:
        import json
        json_data = json.dumps(vars(args), indent=4, sort_keys=True)
        print('input arguments: {json_data}'.format(**locals()))
        sys.exit(0)

    return  args

