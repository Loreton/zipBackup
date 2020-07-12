#!/usr/bin/python
# -*- coding: utf-8 -*-

# value=hashlib.md5(b'string').hexdigest()
myMD5='e925a6f02ff738b7a780b9592bae0af8' # see LP [LnZip Backup Directory]
myMD5_test='098f6bcd4621d373cade4e832627b4f6'
myMD5_ciao='6e6bc4e49dd477ebc98ef4046c067b5f'

def getPw(myMD5):
    if hasattr(getPw, 'my_pw'):
        return getPw.my_pw

    choice = input('enter password').strip()
    md5_val=hashlib.md5(choice.encode()).hexdigest()
    if md5_val in [myMD5]:
        setattr(getPw, 'my_pw', choice)
        return choice
    else:
        print("Password errata")
        sys.exit(1)


