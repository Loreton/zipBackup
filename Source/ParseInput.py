#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-07-2020 16.59.17
#

import sys; sys.dont_write_bytecode=False
import os
import argparse
import pdb
import json
from pathlib import Path
from LnLib.LnColor import LnColor; C=LnColor()
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

    # ---------------------------------------------------
    # LN: required=True e metavar='' da errore di parsing
    # ---------------------------------------------------
    parser = argparse.ArgumentParser(description='create zip file')
    filename_group=parser.add_mutually_exclusive_group(required=True)
    filename_group.add_argument('--filename', metavar='', help='target zip filename', default=None)
    filename_group.add_argument('--auto-filename', action='store_true',
            help="use subfolder namt as zip filenam.")


    parser.add_argument('--root-dir', required=True, metavar=':', type=check_dir,
            help='specify source parent directory')
    parser.add_argument('--target-dir',  required=False, default=None, metavar=':', type=check_dir,
            help='specify destination parent directory for zip_file. Default=root_dir.parent')
    parser.add_argument('--sub-dirs', required=False, default=['*'], metavar='', nargs='*',
            help="specify children directory name(s) to be zipped. Default=all")
    parser.add_argument('--include', required=False, default=['*'], metavar='', nargs='*',
            help="pattern(s) match for include. Default:[**/*]")
    parser.add_argument('--exclude', required=False, default=[], metavar='', nargs='*',
            help="pattern(s) match for exclude. Default=: []")



    parser.add_argument('--crypt',        action='store_true', help='specify if zip file must be crypted.')
    parser.add_argument('--verbose',      type=int, choices=[0,1,2,3], help='display debug data.')
    parser.add_argument('--go',           action='store_true', help='specify if command must be executed. (dry-run is default)')
    parser.add_argument('--display-args', action='store_true', help='Display input parameters')

    args = parser.parse_args()

    if args.display_args:
        import json
        json_data = json.dumps(vars(args), indent=4, sort_keys=True)
        print('input arguments: {json_data}'.format(**locals()))
        sys.exit(0)

    return  args

