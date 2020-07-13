#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 13-07-2020 15.24.27
#

# https://pymotw.com/3/argparse # molto interessante

import sys; sys.dont_write_bytecode=True
import os
import pdb; # https://docs.python.org/3/library/pdb.html
import json
import argparse
# import types



def yellow(text):
    if Color: text=Color.getYellow(text)
    return text

def green(text):
    if Color: text=Color.getGreen(text)
    return text

def cyanH(text):
    if Color: text=Color.getCyanH(text)
    return text

def common_options(subparsers):

    # -- add common options to all subparsers
    for name, subp in subparsers.choices.items():
        # print(name)
        # print(subp)

        # --- common

        # subp.add_argument('--crypt',        action='store_true', help='specify if zip file must be crypted.')
        subp.add_argument('--go', action='store_true', help='load data. default is --dry-run')
        subp.add_argument('--display-args', action='store_true', help='Display input paramenters')
        subp.add_argument('--debug', action='store_true', help='display paths and input args')
        subp.add_argument('--log', action='store_true', help='Activate log.')
        subp.add_argument('--log-level', type=str, default='info', choices=['critical','error','warning','info','debug1','debug2','debug3'], help='specify log level.')
        subp.add_argument('--log-console', action='store_true', help='Activate log and write to console too.')

        subp.add_argument('-log-disp-date', action='store_false', help='NO date in log entry.')
        subp.add_argument('+log-disp-date', action='store_true', help='write date in log entry.')

        subp.add_argument('-log-disp-time', action='store_false', help='NO time in log entry.')
        subp.add_argument('+log-disp-time', action='store_true', help='write time in log entry.')

        subp.add_argument('-log-disp-fullpath-module', action='store_false', help='write just function name in log entry.')
        subp.add_argument('+log-disp-fullpath-module', action='store_true', help='write fullpath module in log entry.')

        subp.add_argument('--log-rotation-filesize', action='store_true', help='write fullpath module in log file.')
        subp.add_argument('--log-rotation-nfiles', type=int, default=0, help='max number of files for rotation.')
        subp.add_argument('--log-modules',
                                    metavar='',
                                    required=False,
                                    default=[],
                                    nargs='*',
                                    help="""Activate log.
    E' anche possibile indicare una o più stringhe separate da BLANK
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName.
    Es: --log-module nudule1 module2 module3
        """)




##############################################################
# - Parse Input
##############################################################
def ParseInput(configFile, color=None):
    global Color
    Color=color
    ####################################
    # # _fileCheck()
    ####################################
    def check_dir(path):
        from pathlib import Path
        p = Path(path)
        if p.is_dir():
            return str(p.resolve())
        else:
            print('    [Ln] - Input arg ERROR: dir: {p} is not valid.'.format(**locals()))
            sys.exit(1)

    # =============================================
    # = Parsing
    # LN: required=True e metavar='' da errore di parsing
    #   formatter_class=argparse.MetavarTypeHelpFormatter
    #   formatter_class=argparse.RawDescriptionHelpFormatter - DEFAULT
    #   formatter_class=argparse.RawTextHelpFormatter
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    # parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    parser = argparse.ArgumentParser(description='create zip file', formatter_class=argparse.RawTextHelpFormatter)

    # parser = argparse.ArgumentParser(description='')
    # dest=action mi permette di avere args.action che contiene il subparser scelto.
    subparsers = parser.add_subparsers(title="primary commands", dest='action', help='commands')


    # - configuration parser
    config_parser  = subparsers.add_parser ("config", formatter_class=argparse.RawTextHelpFormatter,
        help="arguments will be taken from configuration file section")
    config_parser.add_argument('--section', required=False, choices=configFile.keys(), default=None, metavar='',
        help=f'Section of configuration file {list(configFile.keys())}'+ cyanH(''))


    # - manually input  parser
    input_parser = subparsers.add_parser ("input", formatter_class=argparse.RawTextHelpFormatter,
        help="arguments will be taken from input line")
    input_parser.add_argument('--root-dir', required=True, metavar=':', type=check_dir,
            help='specify source parent directory')
    input_parser.add_argument('--target-dir',  required=True, default=None, metavar=':', type=check_dir,
            help='specify destination parent directory for zip_file. Default=root_dir.parent')

    input_parser.add_argument('--filename', metavar='', default=None,
        help='''target zip filename.
    If not specified filename will be the foder name of root_dir argument.''')
    input_parser.add_argument('--sub-dirs', required=True, default=[], metavar='', nargs='*',
            help="specify children directory name(s) to be zipped or '*' for all")
    input_parser.add_argument('--include', required=False, default=['*'], metavar='', nargs='*',
            help="pattern(s) match for include. Default:[**/*]")
    input_parser.add_argument('--exclude', required=False, default=[], metavar='', nargs='*',
            help="pattern(s) match for exclude. Default=: []" )


    input_parser.add_argument('--crypt',        action='store_true', help='specify if zip file must be crypted.')
    input_parser.add_argument('--single-file',  action='store_true',
        help='''Create a single zip file.
    Default creates one zip per subfolder.''' + green(''))


    # - common options
    common_options(subparsers)


    args = parser.parse_args()
    if args.log_console or args.log_modules or args.log_level:
        args.log=True
    # print (args); sys.exit()

    # separazione degli args di tipo debug con quelli applicativi
    dbg=argparse.Namespace()
    log=argparse.Namespace()
    '''
    il processo che segue è per evitare:
       RuntimeError: dictionary changed size during iteration
    '''
    keys=list(args.__dict__.keys())
    _dargs=args.__dict__
    for key in keys:
        val=getattr(args, key)
        if key in ['log']:
            setattr(log, key, val)
        elif key.startswith('log_'):
            setattr(log, key[4:], val)
        elif key in ['go', 'debug']:
            setattr(dbg, key, val)
        else:
            continue

        delattr(args, key)

    if args.action=='config':
        # copia la section del file di configurazione
        app=argparse.Namespace(**configFile[args.section])
    else:
        # copia tutti gli args rimasti
        app=args

    app.action=args.action


    if args.display_args:
        del args.display_args
        import json
        json_data = json.dumps(vars(app), indent=4, sort_keys=True)
        print('application arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(log), indent=4, sort_keys=True)
        print('logging arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(dbg), indent=4, sort_keys=True)
        print('debugging arguments: {json_data}'.format(**locals()))
        sys.exit(0)

    return app, log, dbg


