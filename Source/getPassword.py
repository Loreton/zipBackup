#!/usr/bin/python
# -*- coding: utf-8 -*-

def getPw():
    if hasattr(getPw, 'my_pw'):
        return getPw.my_pw

    choice = input('enter password').strip()
    md5_val=hashlib.md5(choice.encode()).hexdigest()
    if md5_val in [myMD5, myMD5_test, myMD5_ciao]:
        setattr(getPw, 'my_pw', choice)
        return choice
    else:
        print("Password errata")
        sys.exit(1)


