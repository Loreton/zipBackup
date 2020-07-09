#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-07-2020 16.12.12
#

import sys, os; sys.dont_write_bytecode = False
# import os
# import argparse
# import subprocess, shlex
# import pdb
from pathlib import Path

# value=hashlib.md5(b'string').hexdigest()
myMD5='e925a6f02ff738b7a780b9592bae0af8' # see LP [LnZip Backup Directory]
myMD5_test='098f6bcd4621d373cade4e832627b4f6'
myMD5_ciao='6e6bc4e49dd477ebc98ef4046c067b5f'

from Source.ParseInput import ParseInput
from LnLib.zipClass import LnZipClass
# from Source.createZip import createZip


# call:
#      --dirs Loreto  --deep 1 --crypt --go

if __name__ == '__main__':
    global fEXECUTE, fDEBUG, fCRYPT
    inpArgs=ParseInput()

    fEXECUTE=inpArgs.go
    fDEBUG=inpArgs.debug
    fCRYPT=inpArgs.crypt

    root_dir=Path(inpArgs.root_dir)
    target_dir=Path(inpArgs.target_dir) if inpArgs.target_dir else root_dir.parent

    # req_dirs=['LnStart']
    # req_dirs=['LnStart', 'Loreto', 'Lesla']
    req_dirs=inpArgs.sub_dirs
    sys.exit()

    if req_dirs:
        for _name in req_dirs:

            source_path=Path(main_source_dir / _name)
            out_path=Path(main_dest_dir / _name)

            if inpArgs.deep_level==0:
                zipFunc(source_path, out_path, recursive=True)

            elif inpArgs.deep_level==1:
                # zipFunc(source_path, out_path, recursive=False)
                sub_dirs=[x for x in source_path.iterdir() if x.is_dir()]
                for _dir in sub_dirs:
                    if _dir:
                        zipFunc(_dir, out_path, recursive=True)

            else:
                print(' [Ln] - Not yet implemented!')
    else:
        pass

