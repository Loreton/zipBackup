#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 14-07-2020 17.02.24
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
from Source.getPassword import getPassword
# from Source.ParseInput_prev import ParseInput
from LnLib.zipClass import LnZipClass
# from LnLib.ReadConfigurationFile import readConfigFile
from LnLib.yamlLoader_V2 import loadYamlFile
from LnLib.yamlLoader_V2 import processYamlData
from LnLib.LnColor import LnColor; C=LnColor()
from LnLib.LnLogger import setLogger
from LnLib import LnPathMonkeyFunctions

import pdb
if __name__ == '__main__':
    global fEXECUTE, fCRYPT
    prj_name=Path(sys.argv[0]).resolve().parent.stem
    config=loadYamlFile(f'conf/{prj_name}.yml', resolve=True, fPRINT=False)
    args, log, dbg=ParseInput(config['sections_dirs'], color=C)

    if log.log:
        del log.log
        # -------------------------------
        # - Logger Initialitazion
        # -------------------------------
        log_file = f'/tmp/{prj_name}.log'
    else:
        log_file=None
        # params=dict(
        #     log_modules=log.log_modules,
        #     fullpath_module=log.disp_fullpath_module
        #     )

        # xx=vars(log)
    # pdb.set_trace()
    lnLogger = setLogger(filename=log_file, **(log.__dict__))

    lnLogger.debug3('input   arguments', vars(args))
    lnLogger.debug3('logging arguments', vars(log))
    lnLogger.debug3('debug   arguments', vars(dbg))
    lnLogger.debug3('configuration data', config)
    # -------------------------------
    # sys.exit()

    LnPathMonkeyFunctions.LnMonkeySet(lnLogger)
    fEXECUTE=dbg.go
    fCRYPT=args.crypt

    if fCRYPT:
        secret_password=getPassword(args.md5)
    else:
        secret_password=None


    root_dir=Path(args.root_dir)
    if fEXECUTE:
        target_dir=Path(args.target_dir) if args.target_dir else root_dir.parent
    else:
        target_dir=tempfile.gettempdir()

    # pdb.set_trace()
    if args.filename:
        dir_name=root_dir.stem
        zip_name=Path(f'{target_dir}/{dir_name}.zip')
        myZip=LnZipClass(zip_name, mode='w', fUPDATE=args.update, secret_password=secret_password, logger=lnLogger)
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
                    secret_password=secret_password,
                    include=args.include,
                    exclude=args.exclude,
                    fUPDATE=args.update,
                    logger=lnLogger)

