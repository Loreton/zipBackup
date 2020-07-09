#!/usr/bin/python
# -*- coding: utf-8 -*-
# .................-*- coding: latin-1 -*-
# ................-*- coding: iso-8859-15 -*-
#!/usr/bin/python -O

def excludeList(extensions):
    exclude_list=''
    for ext in extensions.split():
        exclude_list+=' -xr!{ext}'.format(**locals())
    return exclude_list


# ###########################################################################
# Dopo vari test per capire il processo più veloce
# ho stabilito di usare zero compression
# Quindi non serve avere più step con diversi file da escludere
# -
# 1. crea il nome dello zip file
# 2. Sale indietro di un livello nella source directory
# 3. esegue lo zip sul source_dir.name
# ###########################################################################
def create_7zip(source_dir, dest_dir, cryptPw='', recursive=False, comp_level=0):
    _dir2zip=source_dir.name
    _parent_dir=source_dir.parent


    zip_filename=str(dest_dir / _dir2zip.replace(' ', '_')) + '.7z'
    os.chdir(_parent_dir)

    # comp='7za u -uq0 -mx5'
    base_cmd='7za u -uq0 -mx{comp_level} {cryptPw}'.format(**locals())

    # - Step 1 - (exclude already compressed files)
    exclude_list=excludeList('*.p12 *.pdf *.zip *.ffs_db')
    exclude_list=excludeList('*.zip *.ffs_db')
    exclude_list=''

    if recursive:
        recurse=''
    else:
        recurse='-x!*/' # NON FUNZIONA
        recurse=''

    if ' ' in _dir2zip: _dir2zip='"{_dir2zip}"'.format(**locals())

    cmd='{base_cmd} {recurse} {exclude_list} {zip_filename} {_dir2zip}'.format(**locals())
    curr_dir=Path().absolute()
    if fDEBUG:
        print()
        print('     current directory: {curr_dir}:'.format(**locals()))
    executeCommand(' [Ln] -', cmd)

    # runCommand(' [Ln] -', cmd)
