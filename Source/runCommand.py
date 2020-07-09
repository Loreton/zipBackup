#!/usr/bin/python
# -*- coding: utf-8 -*-
# .................-*- coding: latin-1 -*-
# ................-*- coding: iso-8859-15 -*-
#!/usr/bin/python -O

# modified: LnVer_2017-08-08_16.21.46
#   python -m compileall .
#   zip -r ../kittyfromWinScp.zip *.*


def runCommand(msg, command):
    if fDEBUG:
        print(msg, command)
        print('splitted:', shlex.split(command))
    process = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.decode('UTF-8').readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def executeCommand(msg, command):
    if fDEBUG:
        print(msg, command)
        print('splitted:', shlex.split(command))
    if fEXECUTE:
        try:
            byteOutput = subprocess.check_output(shlex.split(command), timeout=1000)
            result=byteOutput.decode('UTF-8').rstrip()
        except subprocess.CalledProcessError as e:
            if e.returncode == 12:
                if fDEBUG:
                    print(" zip has nothing to do")
            else:
                print("Error during command execution:")
                output=e.output.decode('UTF-8')
                print("cmd:       ", e.cmd)
                print("returncode:", e.returncode)
                print("output:    ", output)
                for line in output.split('\n'):
                    print(line)
                sys.exit(1)
