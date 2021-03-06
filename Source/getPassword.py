#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys;sys.dont_write_bytecode=True
import os
import hashlib
# value=hashlib.md5(b'string').hexdigest()
myMD5='e925a6f02ff738b7a780b9592bae0af8' # see LP [LnZip Backup Directory]
myMD5_test='098f6bcd4621d373cade4e832627b4f6'
myMD5_ciao='6e6bc4e49dd477ebc98ef4046c067b5f'

def getPassword(myMD5):
    var_passw=os.environ.get('getPassword.my_pw')
    if var_passw:
        return var_passw

    if hasattr(getPassword, 'my_pw'):
        return getPassword.my_pw

    choice = input('enter password ->: ').strip()
    md5_val=hashlib.md5(choice.encode()).hexdigest()
    if md5_val in [myMD5]:
        setattr(getPassword, 'my_pw', choice)
        os.environ['getPassword.my_pw']=choice
        return choice
    else:
        print("Password errata")
        sys.exit(1)


