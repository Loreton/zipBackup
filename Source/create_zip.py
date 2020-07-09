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
# -
# 1. crea il nome dello zip file
# 2. Sale indietro di un livello nella source directory
# 3. esegue lo zip sul source_dir.name
# ###########################################################################
def create_zip(source_dir, dest_dir, recursive=False, comp_level=0):
    _dir2zip=source_dir.name
    _parent_dir=source_dir.parent
    if fCRYPT:
        val=getPw()

    zip_filename=str(dest_dir / _dir2zip.replace(' ', '_')) + '.zip'
    os.chdir(_parent_dir)


    exclude_list=excludeList('*.p12 *.pdf *.zip *.ffs_db')
    exclude_list=excludeList('*.zip *.ffs_db')
    exclude_list=''

    if recursive:
        recurse='-r'
    else:
        recurse=''

    if ' ' in _dir2zip: _dir2zip='"{_dir2zip}"'.format(**locals())

    if fCRYPT:
        if not hasattr(getPw, 'my_pw'):
            getPw()
        pw=getPw.my_pw
        en_crypto='-eP{pw}'.format(**locals())
        de_crypto='-P{pw}'.format(**locals())



    base_cmd='zip -FS {en_crypto}'.format(**locals())
    cmd='{base_cmd} {recurse} {exclude_list} {zip_filename} {_dir2zip}'.format(**locals())
    print('dir: {0:<50} file: {zip_filename}'.format(str(source_dir), **locals()))
    curr_dir=Path().absolute()
    if fDEBUG:
        print()
        print('     current directory: {curr_dir}:'.format(**locals()))
    executeCommand(' [Ln] -', cmd)

    # - TESTzip file
    cmd='unzip -t {de_crypto} {zip_filename}'.format(**locals())
    executeCommand(' [Ln] -', cmd)
    print('         integrity:', 'OK')

