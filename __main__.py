#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 12-07-2020 19.41.55
#

import sys, os; sys.dont_write_bytecode=True
# import os
# import argparse
# import subprocess, shlex
import pdb
from pathlib import Path
import tempfile
import types

# value=hashlib.md5(b'string').hexdigest()
myMD5='e925a6f02ff738b7a780b9592bae0af8' # see LP [LnZip Backup Directory]
myMD5_test='098f6bcd4621d373cade4e832627b4f6'
myMD5_ciao='6e6bc4e49dd477ebc98ef4046c067b5f'

from Source.ParseInput import ParseInput
# from Source.ParseInput_prev import ParseInput
from LnLib.zipClass import LnZipClass
# from LnLib.ReadConfigurationFile import readConfigFile
from LnLib.yamlLoader_V2 import loadYamlFile
from LnLib.LnColor import LnColor; C=LnColor()

import pdb
if __name__ == '__main__':
    global fEXECUTE, fCRYPT
    prj_name=Path(sys.argv[0]).resolve().parent.stem
    config=loadYamlFile(f'conf/{prj_name}.yml', fPRINT=False)
    configVars=config.pop('VARS')
    # pdb.set_trace()
    # sections=list(config)
    # sections.remove('VARS')
    args, dbg=ParseInput(config, color=C)
    fEXECUTE=dbg.go

    # if dbg.action:
    #     # pdb.set_trace()
    #     ns=types.SimpleNamespace(**config[inpArgs.config_section])
    #     crypt=ns.crypt; delattr(ns, 'crypt')
    #     md5=ns.md5; delattr(ns, 'md5')
    # else:
    #     ns=types.SimpleNamespace()
    #     ns.root_dir=inpArgs.root_dir
    #     ns.target_dir=inpArgs.target_dir
    #     ns.single_file=inpArgs.single_file
    #     ns.sub_dirs=inpArgs.sub_dirs
    #     ns.include=inpArgs.include
    #     ns.exclude=inpArgs.exclude



    fCRYPT=args.crypt

    if fCRYPT:
        getPassword()

    root_dir=Path(args.root_dir)
    if fEXECUTE:
        target_dir=Path(args.target_dir) if args.target_dir else root_dir.parent
    else:
        target_dir=tempfile.gettempdir()

    if args.filename:
        dir_name=root_dir.stem
        zip_name=Path(f'{target_dir}/{dir_name}.zip')
        myZip=LnZipClass(zip_name, mode='w', secret_password=secret_password)
        myZip.addFolder(
                    root_dir,
                    dir_name,
                    include=args.include,
                    exclude=args.exclude)
        myZip.close()

    else:
        LnZipClass.oneZipPerFolder(
                    root_dir,
                    target_dir,
                    sub_dirs=args.sub_dirs,
                    include=args.include,
                    exclude=args.exclude)

