#!/usr/bin/env python

prog_name = 'PySol Fan Club edition'

import os

dirs_list = []
files_list = []
for root, dirs, files in os.walk('dist'):
    if files:
        files_list.append(root)
    dirs_list.append(root)

exec(compile(open(os.path.join('pysollib', 'settings.py')).read(), os.path.join('pysollib', 'settings.py'), 'exec'))
prog_version = VERSION

out = open('setup.iss', 'w')

print('''
[Setup]
AppName=%(prog_name)s
AppVerName=%(prog_name)s v.%(prog_version)s
DefaultDirName={pf}\\%(prog_name)s
DefaultGroupName=%(prog_name)s
UninstallDisplayIcon={app}\\pysol.exe
Compression=lzma
SolidCompression=yes
SourceDir=dist
OutputDir=.
OutputBaseFilename=PySolFC_%(prog_version)s_setup

[Icons]
Name: "{group}\\%(prog_name)s"; Filename: "{app}\\pysol.exe"
Name: "{group}\\Uninstall %(prog_name)s"; Filename: "{uninstallexe}"
Name: "{userdesktop}\\%(prog_name)s"; Filename: "{app}\\pysol.exe"
''' % vars(), file=out)

print('[Dirs]', file=out)
for d in dirs_list[1:]:
    print('Name: "{app}%s"' % d.replace('dist', ''), file=out)

print(file=out)
print('[Files]', file=out)
print('Source: "*"; DestDir: "{app}"', file=out)
for d in files_list[1:]:
    d = d.replace('dist\\', '')
    print('Source: "%s\\*"; DestDir: "{app}\\%s"' % (d, d), file=out)


